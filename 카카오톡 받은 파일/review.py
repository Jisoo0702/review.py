from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import openpyxl
import time
import math

# 화면이 다 로딩될 동안 대기하는 시간
PAUSE_TIME = 1 #sleep(1)

class Review:
    def __init__(self):
        # 리뷰는 상세페이지의 하단에 있고, 각 상품별 상세페이지는 동적페이지이므로 셀레늄을 이용하여 크롤링해야함
        # 크롬브라우저를 셀레늄을 이용여 크롤링하기 위한 선언
        # self.driver = webdriver.Chrome()
        # 리뷰 개수
        self.review_count = 0
        # 현재의 리뷰페이지 번호
        self.cur_page_num = 1

    # 리뷰 데이터 추출
    def extract(self, driver, url):
        driver.get(url)

        # 엑셀에 저장해보자
        workbook = openpyxl.load_workbook("Review_Format.xlsx")
        worksheet = workbook.active

        # 상품리뷰 개수를 가져오기 위해 '상품리뷰(xxx)'(review_count_element.text[5:-1])을 추출하여
        review_count_element = driver.find_element_by_xpath("//*[@id=\"productReview\"]/div/div[1]/h2")
        # review_cnt 변수에 리뷰개수를 저장
        review_cnt_str = review_count_element.text[5:-1]
        # 천단위 숫자 구분 표시(,) 는 제거후 숫자타입으로 변환
        # 리뷰가 없으면 pass
        if review_cnt_str == '':
            return None
        review_cnt = int(review_cnt_str.replace(',',''))
        # nextpage가 없을때까지 무한루프
        while True:
            # 셀레늄을 이용하여 상품리뷰데이터를 평점, ID, 리뷰게시일, 리뷰제목, 리뷰내용 별로 읽어옴
            review_rate = driver.find_elements_by_class_name("starRate")       # 평점
            review_user = driver.find_elements_by_class_name("user")           # 사용자 ID
            review_date = driver.find_elements_by_class_name("date")           # 리뷰게시일자
            review_title = driver.find_elements_by_class_name("reviewBody")     # 리뷰제목
            review_body = driver.find_elements_by_class_name("reviewContent")   # 리뷰내용

            review_list_count = len(review_title)

            # 매 리뷰페이지마다 5개씩의 리뷰를 누적 저장
            self.review_count = self.review_count + review_list_count
            for i in range(0, review_list_count):
                # 추출한 것(리뷰평점, ID, 제목, 내용)을 액셀에 저장
                worksheet.append([review_rate[i + 1].text, review_user[i].text,
                                  review_date[i].text, review_title[i].text.strip().split('\n')[0],
                                  review_body[i].text])

            try:
                # 최초 수집한 상품리뷰개수(review_cnt)와 크롤링해온 리뷰수(self.review_count)가 같으면 더이상 crawling 안함
                if review_cnt <= self.review_count:
                    # 리뷰 개수 초기화
                    self.review_count = 0
                    break
                # 만약 현재 리뷰페이지가 10페이지 단위(10,20,30..)이면 화살표페이지 버튼클릭
                elif (self.cur_page_num % 10) == 0:
                    # xpath에서 사용하는 페이지번호는 (1 ~ 10) 임. 따라서 self.cur_page_num이 11이면 다시 1로 초기화
                    self.cur_page_num = 1
                    # xpath에서 사용하는 화살표버튼은 페이지번호 1 ~ 20번(리뷰개수 100) 까지는 2 이고, 21번 부터는 3 임
                    if self.review_count <= 100:
                        arrowpage_btn = driver.find_element_by_xpath("//*[@id=\"reviewPage\"]/a[2]")
                    else:
                        arrowpage_btn = driver.find_element_by_xpath("//*[@id=\"reviewPage\"]/a[3]")
                    driver.execute_script("arguments[0].click();", arrowpage_btn)
                    time.sleep(PAUSE_TIME)
                    print("Navigating to Next Page = %d" %self.cur_page_num)
                # 아니면 다음페이지 버튼 누르면서 계속 crawling 함
                else:
                    self.cur_page_num = self.cur_page_num + 1
                    # 다음 페이지 누르는 버튼은 '리뷰페이지' 말고 'Q&A페이지'도 동일클래스를 사용하고 있어 xpath를 이용하여 다음페이지 클릭
                    nextpage_btn = driver.find_element_by_xpath("//*[@id=\"reviewPage\"]/ol/li[" + str(self.cur_page_num) + "]/a")
                    driver.execute_script("arguments[0].click();", nextpage_btn)
                    time.sleep(PAUSE_TIME)
                    print("Navigating to Next Page = %d" %self.cur_page_num)
            except (TimeoutException, WebDriverException) as e:
                print("Last page reached")
                break

        # 액셀 파일에 저장
        product_name = driver.find_elements_by_class_name("productName")
        # 상품명을 파일명으로 사용시 특수문자는 에러가 발생하므로 상품명에서 특수문자 제거
        file_name = ''.join(char for char in product_name[0].text if char.isalnum())
        workbook.save("Review_Crawling_%s.xlsx" % file_name)
        print("파일 저장 완료 : Review_Crawling_%s.xlsx" % file_name)

        return None

    # 리뷰 페이지 다운 - 사용안함
    def proc(self, url):
        self.driver.get(url)

        data = {
            'review': self.extract("reviewList")
        }

        return data
    # 리뷰 페이지 다운 - 사용안함
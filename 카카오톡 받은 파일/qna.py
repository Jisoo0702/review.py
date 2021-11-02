from selenium import webdriver
import pandas as pd

df = pd.DataFrame(data=[], columns=['답변상태', '문의제목', '문의내용', '작성자', '작성날짜'])

path = 'chromedriver.exe'
driver = webdriver.Chrome(path)
driver.implicitly_wait(3)
driver.get('https://shopping.interpark.com/product/productInfo.do?prdNo=7613757916&dispNo=008022001')


def crawl(driver2, datas, k):
    status = driver2.find_elements_by_class_name('status')
    title = driver2.find_elements_by_class_name('questionTitle')
    content = driver2.find_elements_by_class_name('questionContent')
    author = driver2.find_elements_by_class_name('author')
    datetime = driver2.find_elements_by_class_name('datetime')

    for i in range(k):
        tmp = []
        tmp.append(status[i+3].text)
        tmp.append(title[i].text)
        tmp.append(content[i].text)
        tmp.append(author[i+2].text)
        tmp.append(datetime[i*2].text)

        tmp = pd.DataFrame(data=[tmp], columns=datas.columns)
        datas = pd.concat([datas, tmp])

    print(str(k) + '개 문의 수집 완료')

    return datas


data = crawl(driver, df, 10)
print(data)
driver.close()

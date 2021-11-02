from selenium import webdriver

driver = webdriver.Chrome('./chromedriver')
driver.get("http://shopping.interpark.com")

for i in range(13):
    if i < 10:
        url="http://shopping.interpark.com/best/main.do?cateNo=0{0}&rankDtlKind=0{0}_000_0000&type=0".format(i)
        driver.get(url)
        driver.implicitly_wait(5)
        for recommend in driver.find_elements_by_css_selector('#recommendListId'):
            print(recommend.text)

    else:
        url="http://shopping.interpark.com/best/main.do?cateNo={0}&rankDtlKind={0}_000_0000&type=0".format(i)
        driver.get(url)
        driver.implicitly_wait(5)
        for recommend in driver.find_elements_by_css_selector('#recommendListId'):
                print(recommend.text)

url="http://shopping.interpark.com/best/main.do?cateNo=&rankDtlKind=&type=4"
driver.get(url)
driver.implicitly_wait(5)
for recommend in driver.find_elements_by_css_selector('#recommendListId'):
    print(recommend.text)
from selenium import webdriver
import requests
import time
import numpy as np
import pandas as pd
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome('C:\chromedriver')

# 카테고리 선택 코드 삽입
url="http://shopping.interpark.com/best/main.do?cateNo=08&rankDtlKind=08_000_0000&type=0"
driver.get(url)
driver.implicitly_wait(5)

#100 순위만 가져오므로
for i in range(1,101):
    driver.find_element_by_xpath('//*[@id="recommendListId"]/li['+str(i)+']/div[2]/a').send_keys(Keys.ENTER)
    time.sleep(2)
    driver.switch_to.window(driver.window_handles[-1])

#내용 저장하는 코드 내용 삽입

    driver.close()
    driver.switch_to.window(driver.window_handles[0])
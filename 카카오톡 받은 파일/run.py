from app.spiders.category import Category
import time
from selenium import webdriver
import requests
import time

driver = webdriver.Chrome('chromedriver')

def category_run():
    cat = Category()

    for i in range(13):
        if i < 10:
            url="http://shopping.interpark.com/best/main.do?cateNo=0{0}&rankDtlKind=0{0}_000_0000&type=0".format(i)
            cat.proc(url)
            time.sleep(1)

        else:
            url="http://shopping.interpark.com/best/main.do?cateNo={0}&rankDtlKind={0}_000_0000&type=0".format(i)
            cat.proc(url)
            time.sleep(1)
            
    url="http://shopping.interpark.com/best/main.do?cateNo=&rankDtlKind=&type=4"
    cat.proc(url)
    time.sleep(1)


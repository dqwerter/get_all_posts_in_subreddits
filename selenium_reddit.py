from selenium import webdriver
import time
from random import random

driver = webdriver.Chrome(executable_path='/Users/wangqin/code/PycharmProjects/weibo_covid19/chromedriver')
driver.get("https://www.reddit.com/r/COVID19")


# SCROLL_PAUSE_TIME = 2
#
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")
#
# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#
#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME * random())
#
#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height

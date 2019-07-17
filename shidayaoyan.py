from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import requests
import os
import math
import re
import platform
from lxml import etree
from datetime import datetime
count = 0
chrome_driver_path ="chromedriver.exe"

headers = {'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
main_page_url = 'http://piyao.sina.cn'
requests.headers = headers
try:
    r = requests.get(main_page_url)
except requests.exceptions.RequestException as e:
        print('链接异常，请检查网络')
        print(e)
        quit()

if(r.status_code!=200):
        print('http状态码错误')
        quit()
chrome_options = Options()
chrome_options.add_argument('--disable-gpu')
driver = webdriver.Chrome(chrome_options=chrome_options, \
            executable_path= chrome_driver_path)
driver.get(main_page_url)
time.sleep(3)

# 获取页面初始高度
js = "return action=document.body.scrollHeight"
height = driver.execute_script(js)

# 将滚动条调整至页面底部
driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
time.sleep(5)

#定义初始时间戳（秒）
t1 = int(time.time())

#定义循环标识，用于终止while循环
status = True

# 重试次数
num=0

while count<10:
	# 获取当前时间戳（秒）
    t2 = int(time.time())
    # 判断时间初始时间戳和当前时间戳相差是否大于30秒，小于30秒则下拉滚动条
    if t2-t1 < 30:
        new_height = driver.execute_script(js)
        if new_height > height :
            time.sleep(1)
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            # 重置初始页面高度
            height = new_height
            # 重置初始时间戳，重新计时
            t1 = int(time.time())
            count = count +1
    elif num < 3:                        # 当超过30秒页面高度仍然没有更新时，进入重试逻辑，重试3次，每次等待30秒
        time.sleep(3)
        num = num+1
        count = count +1
    else:    # 超时并超过重试次数，程序结束跳出循环，并认为页面已经加载完毕！
        print("滚动条已经处于页面最下方！")
        status = False
        # 滚动条调整至页面顶部
        driver.execute_script('window.scrollTo(0, 0)')
        break
        
mostgood = []
text = []
good = []
time = []
time_str = driver.find_elements_by_xpath('//div[@class="zy_day"]/div[@class="day_date"]')
for k,date in enumerate(time_str,start = 1):
    text_str = driver.find_elements_by_xpath('//div[@class="zy_day" and position()=%d]/div[@class="day_date"]/following-sibling::ul//div[@class="left_title"]'%k)
    good_str = driver.find_elements_by_xpath('//div[@class="zy_day" and position()=%d]/div[@class="day_date"]/following-sibling::ul//div[@class="left_btns"]/div[@class="like_text"]'%k)
    for i in text_str:
        text.append(i.text)
    for j in good_str:
        good.append(j.text)
    time.append(date.text)
good_and_text = zip(good,text,time)
mostgood = sorted(good_and_text, key=lambda x : x[0],reverse = True)
print("新浪十大谣言：")
for x in mostgood[:10]:
    print("点赞数：",x[0],'\t',x[2],'\t',x[1])
driver.quit()
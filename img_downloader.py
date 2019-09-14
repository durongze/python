from selenium import webdriver
import time
import urllib
import urllib3
import autogui
import pyautogui
import time
import os
import re

# 爬取页面地址
url = 'http://ss.xxxx.com/gopreview?ssid=13482506&dxid=000013735928&d=7f54d8e847769480804c65be4e5d379d7d7ac24ca4e37d5e4e1f3e0a0411adbf7dbd77850359ec318de2c1583e184fbf7ee0d7625dc5975f137776a9a62bb479b0cb93188d84e84870c00ae2b6f195e9519bbe7ef2b1d935d47fb14e619e2f9fa8cecce651f1bd0136c94e7583add95a8e867bf5ac27649ae17308bb4cfb11c26591cb330ed531242bc5d3468b8d446a154f331f3ee7a9fbd7bcf05b3989e30de0229cfba4342708b8a71ce53a8a4743898ff967fea927edef51c17236d01d90'

xpath_btn='/html/body/div[2]/div/p[2]/a'
# 目标元素的xpath
xpath = '//*[@id="flip"]/div/div'
# 启动Firefox浏览器
driver = webdriver.Ie()

# 最大化窗口，因为每一次爬取只能看到视窗内的图片
driver.maximize_window()

# 记录下载过的图片地址，避免重复下载
img_url_dic = {''}

# 浏览器打开爬取页面
driver.get(url)
driver.switch_to_frame('_right')
# 模拟滚动窗口以浏览下载更多图片
pos = 0
m = 0  # 图片编号
g_base_url=''
all_page=[]
for i in range(10):
    pos += i * 500  # 每次下滚500
    js = "document.documentElement.scrollTop=%d" % pos
    driver.execute_script(js)
    time.sleep(1)
    for element in driver.find_elements_by_xpath(xpath):
        if m > 282:
            break
        if element == None:
            continue
        input = element.find_element_by_class_name('readerImg')
        if input == None:
            continue
        if not g_base_url in img_url_dic:
            img_url = g_base_url
        else:
            img_url = input.get_attribute('src')
        # 保存图片到指定路径
        if img_url != None and not img_url in img_url_dic:
            #img_url_dic[img_url] = ''
            if g_base_url in img_url_dic:
                g_base_url = img_url[:-13]
            for i in range(272):
                m += 1
                print('{:0>6d}'.format(m))
                img_url = g_base_url + '{:0>6d}'.format(m)
                img_url += '?zoom=0'
                print(img_url)
                all_page.append(img_url)

m=0
btn_xpath='/html/body/img'
for page in all_page:
    m += 1
    if m < 176:
        continue
    ext='png'
    filename = str(m) + '.' + ext
    # 保存图片数据
    driver.get(page)
    for element in driver.find_elements_by_xpath(btn_xpath):
        img_src = element.get_attribute('src')
        data = urllib.request.urlopen(img_src).read()
        f = open('./van/' + filename, 'wb')
        f.write(data)
        f.close()
        driver.close()
driver.close()

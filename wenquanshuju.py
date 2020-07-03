import urllib3
import urllib
from selenium import webdriver
import time
import urllib
import urllib3
import autogui
import pyautogui
import time
import os
import re
import random
from pathlib import Path
import execjs

http = urllib3.PoolManager()
agent_list = [
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
"Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
"Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
"Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11"
]


def gen_remote_url(base_url, page_no):
    print('{:0>6d}'.format(page_no))
    img_url = base_url + '{:0>6d}'.format(page_no)
    img_url += '?zoom=0'
    return img_url


def gen_local_path(base_dir, page_no, ext):
    file_name = '{:0>6d}'.format(page_no) + '.' + ext
    file_name = base_dir + '\\' + file_name
    return file_name


def download_img(img_url, file_name):
    r = http.request('GET', img_url)
    data = r.data
    f = open(file_name, 'wb+')
    f.write(data)
    f.close()


'img.onload = function(){ let baseSrc = document.querySelector("#pagebox div"); console.log(baseSrc.getAttribute("src")); }'

def download_book(book_url, item_xpath, download_dir):
    driver = webdriver.Chrome()
    driver.get(book_url)
    i = 0
    for element in driver.find_elements_by_xpath(item_xpath):
        i = i + 1
        if i < 1:
            continue
        file_name = gen_local_path(download_dir, i, 'png')
        if Path(file_name).exists():
            print("exist :%s" % file_name)
            continue
        print(element.get_attribute('innerHTML'))
        img_src = element.get_attribute('src')
        opener = urllib.request.build_opener()
        opener.addheaders = user_agent
        data = urllib.request.urlopen(img_src).read()
        f = open(file_name, 'wb')
        f.write(data)
        f.close()
        driver.close()


btn_xpath = '//*[@id="pagebox"]/div'
base_url = 'https://wqbook.wqxuetang.com/read/pdf/8888888888'
download_dir = 'E:\\webdown\\van'

if __name__ == "__main__":
    user_agent = random.choice(agent_list)
    download_book(base_url, btn_xpath, download_dir)

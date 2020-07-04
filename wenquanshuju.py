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
import html
import re
from bs4 import BeautifulSoup
from os.path import basename, splitext
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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


def call_js_func(js_func, data, key):
    js_ctx = execjs.compile(js_func)  # 加载JS文件
    print("还不能使用 js 访问 python中的元素")
    return js_ctx.call('get_item_src')  # 调用js方法  第一个参数是JS的方法名，后面的data和key是js方法的参数


def find_target_items(text):
    p=re.compile(r'[<](.*?)[>]', re.S)
    matches = re.findall(p, text)
    images = []
    for match in matches:
        print (match)
        if match.find('img') == 0:  # 包含html代码，img在字符串首位
            soup = BeautifulSoup("<"+match+">")
            img = soup.find_all('img')
            src=img[0].get('src')
            images.append(src)
        #else:
            # images.append(match)  # 不包含html代码
    return images

def element_click(browser, element):
    try:
        ActionChains(browser).double_click(element).perform()
        WebDriverWait(browser, 8, 0.5, ignored_exceptions=EC).until(element.is_displayed())
        print('success')
    except Exception as e:
        print('fail')


def write_element(data, file_name):
    f = open(file_name, 'wb')
    f.write(data)
    f.close()


def get_page_link(driver, element):
    items = []
    element_click(driver, element)
    element_html = element.get_attribute('innerHTML')
    items.append(element_html)
    images = find_target_items(element_html)
    return images


def write_page_data(img_src, file_name):
    opener = urllib.request.build_opener()
    opener.addheaders = user_agent
    data = urllib.request.urlopen(img_src).read()
    f = open(file_name, 'wb')
    f.write(data)
    f.close()


def get_book_pages(book_url, item_xpath, js_func_str, download_dir):
    driver = webdriver.Chrome()
    driver.get(book_url)
    element_list = driver.find_elements_by_xpath(item_xpath)
    all_pages = []
    all_items = []
    for element in element_list:
        element_click(driver, element)
        element_html = element.get_attribute('innerHTML')
        all_items.append(element_html)
        images = find_target_items(element_html)
        all_pages = all_pages + images
    i = 0
    for page in all_pages:
        file_name = gen_local_path(download_dir, i, 'png')
        write_page_data(page, file_name)
        i = i + 1
    return all_pages

def download_book(book_url, item_xpath, js_func_str, download_dir):
    driver = webdriver.Chrome()
    driver.get(book_url)
    element_list = driver.find_elements_by_xpath(item_xpath)
    i = 0
    for element in element_list:
        i = i + 1
        if i < 1:
            continue
        file_name = gen_local_path(download_dir, i, 'png')
        if Path(file_name).exists():
            print("exist :%s" % file_name)
            continue
        element_click(driver, element)
        # element.screenshot(file_name)
        element_html = element.get_attribute('innerHTML')
        print("====== ========\n ", element_html)
        images = find_target_items(element_html)
        img_src = images[0]
        if img_src is None:
            print("error page idx :%s" % i)
            continue
        # img_src = element.get_attribute('src')
        # img_src = call_js_func(js_func_str, element.get_attribute('innerHTML'), "src")
        # img_src = driver.execute_script(js_func_str, element_html, "src")
        opener = urllib.request.build_opener()
        opener.addheaders = user_agent
        data = urllib.request.urlopen(img_src).read()
        f = open(file_name, 'wb')
        f.write(data)
        f.close()
    driver.close()


btn_xpath = '//*[@class="page-img-box"]'
base_url = 'https://wqbook.wqxuetang.com/read/pdf/11111111111'
download_dir = 'E:\\webdown\\van'

if __name__ == "__main__":
    user_agent = random.choice(agent_list)
    js_func_str = 'function get_item_src(){  return console.log("data"); }'
    js_str = 'arguments[0].getAttribute(arguments[1], 4)'
    #download_book(base_url, btn_xpath, js_str, download_dir)
    all_pages = get_book_pages(base_url, btn_xpath, js_str, download_dir)
    print(all_pages)


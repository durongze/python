import requests
import re
import json
import sys
from contextlib import closing
from pyquery import PyQuery as pq
from requests import RequestException

site_url = 'http://www.xxx.com'
class anysafer():
    def __init__(self):
        self.getHtmlHeaders={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q = 0.9'
        }

        self.downloadVideoHeaders={
            'Origin': site_url,
            'Referer': site_url,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        }

    #一般这里得到的网页源码和F12查看看到的不一样，因为F12开发者工具里的源码经过了浏览器的解释
    def getHtml(self,url):
        try:
            response = requests.get(url=url, headers=self.getHtmlHeaders)
            if response.status_code == 200:
                return response.text
        except RequestException:
            print('请求Html错误:')

    def parseHtml(self,html):
        #用pq解析得到视频标题
        Books = []
        doc = pq(html)
        ResClass = doc('#lanmuLayout > div > span > a').pop(1)
        #BodyTitle = doc('#bodyLayout > div > div > h2').text()
        BodyClass = doc('#bodyLayout > div > div > ul > li')
        BookList = BodyClass('a').items()
        for Element in BookList:
            if (Element.attr('title')):
                Books.append({'title': Element.attr('title'), 'url': site_url + Element.attr('href')})
        return Books

    def parseDownUrl(self, bookUrl):
        doc = pq(self.getHtml(bookUrl))
        downUrl = doc('#adform > ul > li > a').attr('href')
        downDoc = pq(self.getHtml(site_url + downUrl))
        realUrl = downDoc('#adform > ul > li > a').attr('href')
        return site_url + realUrl

    def download(self,video):
        urlList = video
        for bookUrl in urlList:
            url = self.parseDownUrl(bookUrl['url'])
            with open(bookUrl['title'], "wb") as f:
                print(bookUrl, url)
                f.write(requests.get(url=url, headers=self.downloadVideoHeaders, stream=True, verify=False).content)

        #closing适用于提供了 close() 实现的对象，比如网络连接、数据库连接
        # with closing(requests.get(video['url'], headers=self.downloadVideoHeaders, stream=True, verify=False)) as res:
        #     if res.status_code == 200:
        #         with open(filename, "wb") as f:
        #             for chunk in res.iter_content(chunk_size=1024):
        #                 if chunk:
        #                     f.write(chunk)

    def run(self,url):
        self.download(self.parseHtml(self.getHtml(url)))

if __name__ == '__main__':
    prefix_url = site_url;
    classRes = ['yishu']
    for idx in range(classRes.__len__()):
        video_url=prefix_url + '/' + classRes[idx]
        print(sys._getframe().f_code.co_name, video_url)
        anysafer().run(video_url)

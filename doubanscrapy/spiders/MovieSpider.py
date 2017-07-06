import scrapy
import requests
import time
from bs4 import BeautifulSoup
import urllib.request
import re

from doubanscrapy.items import MovieItem
from scrapy.loader import ItemLoader

headers = {
    "Host": "www.douban.com",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.6",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Connection": "keep-alive"
}


def login():
    login_str = u'登录'
    data = {
        # 'ck':'GiW5',
        'source': 'None',
        'redir': 'https://movie.douban.com/',
        'form_email': 'gao__fan@126.com',
        'form_password': 'gao910228',
        # 'captcha_solution':captcha_solution,
        # 'captcha_id':captcha_id,
        'login': login_str
    }
    loginUrl = 'https://www.douban.com/accounts/login'
    session = requests.session()
    html = session.get(loginUrl, headers=headers).text
    soup = BeautifulSoup(html, "html.parser")
    imageSrc = soup.find('img', id='captcha_image')
    captchaAddr = None
    if imageSrc is not None:
        captchaAddr = imageSrc['src']
    # captchaAddr = soup.find('img', id='captcha_image')['src']
    if captchaAddr is not None:
        urllib.request.urlretrieve(captchaAddr, "captcha.jpg")
        print(captchaAddr)
        reCaptchaID = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captchaID = re.findall(reCaptchaID, html)
        captcha = input('please input the captcha:')
        data['captcha-solution'] = captcha
        data['captcha-id'] = captchaID
    session.post(loginUrl, headers=headers, data=data)
    print(data)
    print(session.cookies.items())
    return session


class MovieSpider(scrapy.Spider):
    name = 'moviespider'

    def __init__(self, name=None, **kwargs):
        super().__init__(name=None, **kwargs)
        self.requestUrl = 'https://movie.douban.com/j/search_subjects'
        self.pageLimit = 20
        self.params = {'type': 'movie', 'tag': '热门', 'sort': 'recommend', 'page_limit': self.pageLimit}
        self.pageStart = 0

    def start_requests(self):
        session = login()
        tmpContinue = True
        UserAgent = [
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36']
        agentInidex = 1
        while True:
            try:
                self.params['page_start'] = self.pageStart * self.pageLimit
                headers['User-Agent'] = UserAgent[1-agentInidex]
                agentInidex = 1 - agentInidex
                response = session.get(self.requestUrl, params=self.params, headers=headers)

                if response is not None and response.status_code == 200:
                    items = response.json()['subjects']
                    for item in items:
                        yield scrapy.Request(item.get('url'), callback=self.parse)
                else:
                    continue
            except Exception:
                pass
            self.pageStart += 1
            time.sleep(90)

        print('stop scrap')

    def parse(self, response):
        try:
            l = ItemLoader(item=MovieItem(), response=response)
            l.add_value('name',
                        response.css('div#content h1 [property="v:itemreviewed"]::text').extract_first().strip())
            year = response.css('div#content h1 span.year::text').extract_first()
            if year.startswith('('):
                year = year[1:-1]
            l.add_value('year', year)

            newStrL = []
            for val in response.css('div#info::text').extract():
                newStr = val.strip().strip('/')
                if newStr != '':
                    newStrL.append(newStr)
                    if len(newStrL) == 2:
                        break

            if len(newStrL) == 2:
                l.add_value('region', newStrL[0].split('/'))
                l.add_value('language', newStrL[1].split('/'))

            l.add_value('duration', response.css('div#info [property="v:runtime"]::attr(content)').extract_first())
            l.add_value('types', response.css('div#info [property="v:genre"]::text').extract())
            l.add_value('directors', response.css('div#info [rel="v:directedBy"]::text').extract())
            l.add_value('actors', response.css('div#info [rel="v:starring"]::text').extract())
            l.add_value('runtime', response.css('div#info [property="v:initialReleaseDate"]::text').extract())
            l.add_value('detailurl', response.url)
            l.add_value('IMDburl', response.css('div#info [rel="nofollow"]::attr(href)').extract())
            l.add_value('stars', response.css('strong[property="v:average"]::text').extract_first())
            return l.load_item()
        except Exception:
            pass

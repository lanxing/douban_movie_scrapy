# douban_movie_scrapy

---
模拟豆瓣登录，如果登录过程中需要输入验证码，自动下载验证码(captcha.jpg)，然后手动输入验证码，登陆后获取session，用session请求豆瓣电影列表数据，然后利用爬虫爬取电影详情页面数据，最后把电影基本信息存储在本地MySql中.

---
#### 系统要求
+ peewee(http://docs.peewee-orm.com/en/latest/)
+ requests(http://docs.python-requests.org/en/master/)
+ python3.5+
+ scrapy(https://scrapy.org/)

---
#### 使用
1. git clone https://github.com/lanxing/douban_movie_scrapy.git
2. 进入model模块，调用Model.py中的createTable函数创建本地数据库,注意修改db的username和password
3. 执行scrapy crawl moviespider

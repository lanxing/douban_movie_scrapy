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

---
#### 其他
1. 示例只爬取豆瓣热门电影(https://movie.douban.com/explore#!type=movie&tag=%E7%83%AD%E9%97%A8&sort=recommend&page_limit=20&page_start=300)
2. 通过抓包会发现该页面点击更多时调用(https://movie.douban.com/j/search_subjects?page_start=0&tag=%E7%83%AD%E9%97%A8&sort=recommend&type=movie&page_limit=20)接口来获取电影列表,因此只需要修改page_start即可获取电影列表。
3. 当拉取数据过于频繁时，豆瓣会对请求进行限制，重定向到一个验证请求不是机器人的页面，需要重新输入验证码，所以为了防止ip被限制，爬虫每分钟请求一次数据，一次请求20条

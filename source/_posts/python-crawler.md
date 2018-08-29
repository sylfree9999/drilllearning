---
title: python-crawler
date: 2018-08-14 17:01:54
tags: [python, practice]
---

## XPath

### 路径表达式
	*	nodename选取此节点的所有子节点
	*	/从根节点选取
	*	//从匹配的当前节点选择文档中的节点，而不考虑他们的位置
	*	. 选取当前节点
	*	.. 选取当前节点的父节点
	*	@选取属性

```xml
<?xml version="1.0"?>
<bookstore>
	<book>
		<title lang="eng">Harry Potter</title>
		<price>29.99</price>
	</book>
	<book>
		<title lang="eng">Learn XML</title>
		<price>75</price>
	</book>
</bookstore>
```
<!--more-->
例子
	*	bookstore 选取bookstore元素的所有子节点
	*	/bookstore 选取根元素bookstore
	*	/bookstore/book 选取属于bookstore的子元素的所有book元素
	*	//book 选取所有book元素，而不管它们在文档中的位置。
	*	bookstore//book 选择属于bookstore元素的后代的所有book元素
	*	//@lang 选取名为lang的所有属性

谓语
	*	嵌在[]中用来查找某个特定节点或包含某个指定值得节点。
	*	/bookstore/book[1] 第一个book元素
	*	/bookstore/book[last()] 最后一个book元素
	*	/bookstore/book[position()<3] 选择前2个
	*	//title[@lang] 选择所拥有有名为lang的属性的title元素
	*	/bookstore/book[price>35.00]

## 正则表达式

基本匹配规则
	*	[0-9] 任意一个数字，等价\d
	*	[a-z] 任意一个小写字母
	*	[A-Z]任意一个大写字母
	*	[^0-9] 匹配非数字，等价\D
	*	\w 等价[a-z0-9_]，字母数字下划线
	*	\W 等价对\w取非
	*	. 任意字符
	*	[] 匹配内部任意字符或子表达式
	*	[^] 对字符集合取非
	*	* 匹配前面的字符或者子表达式0次或多次
	*	+ 匹配前一个字符至少1次
	*	？ 匹配前一个字符0次或1次
	*	^ 匹配字符串开头
	*	$ 匹配字符串结束	*	

## 用selenium模拟用户打开浏览器然后抓数据
### 包含如果网页有惰性加载的情况，需要scroll到页面最底部
```python
from selenium import webdriver
import time

browser = webdriver.Chrome()
browser.set_page_load_timeout(30)
browser.get('http://www.17huo.com/search.html?sq=2&keyword=%E7%BE%8A%E6%AF%9B')
page_info = browser.find_element_by_css_selector('body > div.wrap > div.pagem.product_list_pager > div')
# print(page_info.text)
pages = int((page_info.text.split('，')[0]).split(' ')[1])
for page in range(pages):
    if page > 2:
        break
    url = 'http://www.17huo.com/?mod=search&sq=2&keyword=%E7%BE%8A%E6%AF%9B&page=' + str(page + 1)
    browser.get(url)
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)   # 不然会load不完整
    goods = browser.find_element_by_css_selector('body > div.wrap > div:nth-child(2) > div.p_main > ul').find_elements_by_tag_name('li')
    print('%d页有%d件商品' % ((page + 1), len(goods)))
    for good in goods:
        try:
            title = good.find_element_by_css_selector('a:nth-child(1) > p:nth-child(2)').text
            price = good.find_element_by_css_selector('div > a > span').text
            print(title, price)
        except:
            print(good.text)
```


## 保存图片

### 用Requests
```python
import requests
from PIL import Image
from io import BytesIO

r = requests.get('https://images.unsplash.com/photo-1504714146340-959ca07e1f38?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=2c5ef407d31cf63f60bd7782132ee877&auto=format&fit=crop&w=925&q=80')
image = Image.open(BytesIO(r.content))
image.save('scenary.png')

#原始数据处理,例stream数据，一点点读出来，而不是一次性读出来
r = requests.get('https://images.unsplash.com/photo-1504714146340-959ca07e1f38?ixlib=rb-0.3.5&ixid=eyJhcHBfaWQiOjEyMDd9&s=2c5ef407d31cf63f60bd7782132ee877&auto=format&fit=crop&w=925&q=80', stream = True)
with open('scenary2.png', 'wb+') as f:
    for chunk in r.iter_content(1024):
        f.write(chunk)

```

## Scrapy
### Architecture Overview
{%asset_img scrapy_architecture_02.png %}
	1. Engine从Spider那里拿到初始Url
	2. Engine把Requests丢给Scheduler,Scheduler返回下一个需要爬的requests
	3. Scheduler生成下一个Requests
    4. Engine把新的Requests丢给Downloader，让其下载页面
    5. Downloader下载完（生成Response）后返回给Engine
    6. Engine把这个Response丢给Spider让他处理
    7. Spider把Response变成你定义规则的Scraped Items，如果有新的需要爬的，重新传给Engine
    8. Engine把Scraped Items传给Item Pipelines,在ItemPipelines里面可以保存到数据库，对数据清洗等等。然后Engines再问Schedule是否还有需要Requests的东西
    9. 从Step1循环，直至没有新的Requests

### User Login
#### 注意点一，start_requests()方法必须返回一个iterable.
Scrapy calls it only once, so it is safe to implement `start_requests()` as a generator.

#### 注意点二，用FormRequest可以通过HTTP POST方式发送数据

```python
return [FormRequest(url="http://www.example.com/post/action",
                    formdata={'name': 'John Doe', 'age': '27'},
                    callback=self.after_post)]
```

#### 注意点三，FormRequest.from_response()可以模拟用户登陆
```python
import scrapy

class LoginSpider(scrapy.Spider):
    name = 'example.com'
    start_urls = ['http://www.example.com/users/login.php']

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'john', 'password': 'secret'},
            callback=self.after_login
        )

    def after_login(self, response):
        # check login succeed before going on
        if "authentication failed" in response.body:
            self.logger.error("Login failed")
            return

        # continue scraping with authenticated session...
```

#### 注意点四，scrapy.FormRequest的meta作用，是向response传递数据

#### 注意点五，dont_filter=True意味着如果需要多次提交表单，且url一样，那么就让爬虫继续爬，否则爬虫会有去重机制不会再爬这个页面

示例：登陆然后爬数据

例：
```python
import scrapy
from PIL import Image
from urllib.request import urlretrieve


class MovieCommentSpider(scrapy.Spider):
    name = 'movie_comment'
    allowed_domains = ['accounts.douban.com', 'douban.com']
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0"
    }

    def start_requests(self):
        return [scrapy.FormRequest("https://accounts.douban.com/login"
                                  , headers=self.headers
                                  , meta={"cookiejar": 1},
                                  callback=self.parse_before_login)]

    def parse_before_login(self, response):
        captcha_id = response.xpath('//input[@name="captcha-id"]/@value').extract_first()
        captcha_image_url = response.xpath('//img[@id="captcha_image"]/@src').extract_first()
        if captcha_image_url is None:
            formdata = {
                "source": "index_nav",
                "form_email": "************@yahoo.com.cn",
                "form_password": "***************",
            }
        else:

            save_image_path = "D:\\captcha.jpeg"
            # 将图片验证码下载到本地
            urlretrieve(captcha_image_url, save_image_path)
            # 打开图片，以便我们识别图中验证码
            try:
                im = Image.open('captcha.jpeg')
                im.show()
            except:
                pass
            # 手动输入验证码
            captcha_solution = input('**********Please input capture:*************')
            formdata = {
                "source": "None",
                "redir": "https://www.douban.com",
                "form_email": "******************@yahoo.com.cn",
                # 此处请填写密码
                "form_password": "*****************",
                "captcha-solution": captcha_solution,
                "captcha-id": captcha_id,
                "login": "登录",
            }

        # 提交表单
        return scrapy.FormRequest.from_response(response
                                                , meta={"cookiejar": response.meta["cookiejar"]}
                                                , headers=self.headers
                                                , formdata=formdata
                                                , callback=self.parse_after_login)

    def parse_after_login(self, response):
        '''
        验证登录是否成功
        '''
        account = response.xpath('//a[@class="bn-more"]/span/text()').extract_first()
        if account is None:
            print("Login Failed")
        else:
            print("Login Success,Current account is {0}".format(account))

```
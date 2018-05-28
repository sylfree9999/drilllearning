---
title: Flask 一些概念
date: 2018-04-17 15:32:39
tags: [flask, concept]
---

## URL重定向行文

```python
@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'
```

注意`@app.route('/projects/')`最末尾的`/`，看起来如同一个文件夹。
**访问一个没有斜杠结尾的URL时，Flask会自动进行重定向，帮你在尾部加上一个斜杠**

但是`@app.route('/about')`尾部没有斜杠，如果你在浏览器里面输入了`localhost:2000/about/`， 会出现<span style="color: red">404错误</span>	

## url_for（）用于生成制定函数的url

url_for()会为你处理特殊字符的转义以及Unicode数据

```python
>>> from flask import Flask, url_for
>>> app = Flask(__name__)
>>> @app.route('/')
... def index(): pass
...
>>> @app.route('/login')
... def login(): pass
...
>>> @app.route('/user/<username>')
... def profile(username): pass
...
>>> with app.test_request_context():
...  print url_for('index')
...  print url_for('login')
...  print url_for('login', next='/')
...  print url_for('profile', username='John Doe')
...
/
/login
/login?next=/
/user/John%20Doe
```

## flask blueprint

flask blueprint用于模块化代码， 如果没有蓝图，那么一个blog系统（分前端和后端）

```python
from flask import Flask, render_template, reque
```
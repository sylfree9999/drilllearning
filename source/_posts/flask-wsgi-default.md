---
title: Flask wsgi 套路文件
date: 2018-05-22 11:51:16
tags: [flask, practice]
---

套路文件

```python
#!/usr/bin/env python3

import sys
from os.path import abspath
from os.path import dirname

# set current directory as working directory
sys.path.insert(0, abspath(dirname(__file__)))

# import app.py (flask 启动文件)
import app

# MUST HAVE an application
application = app.app
```

对于gunicorn+搭配supervisord部署
`cat /etc/supervisor/conf.d/todo.conf`
在此文件中更改
```
[program:todo]
command = /usr/local/bin/gunicorn wsgi --bind 0.0.0.0:80 --pid /tmp/todo.pid
directory = /todo
autostart = true
```

然后
```
sudo supervisorctl restart todo
```
或者
```
sudo service supervisor restart
```
默认的日志错误文件在
```
cat /var/log/supervisor/todo-stderr---supervisor-WX7Fbz.log
```
---
title: Session Cookie
date: 2018-05-22 16:12:41
tags: [concept]
---

Session 和 Cookie的出现都是为了保存状态， 因为浏览器是无状态的

## Cookie 是保存在客户端的，如果服务器的response里面有set_cookie,则客户端的服务器就会存这个值

## Cookie里面不能直接存敏感的值，所以有了Session, 服务器维护Session和Cookie的Mapping关系，但是
<span style="color:red">Session也是可以存在客户端的</span>


比方说
``` python
@main.route("/login", methods=['POST'])
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.index'))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        return redirect(url_for('.profile'))
```

{% asset_image 20180522162224.png %}

不过比较好的方法是放在服务器中防止客户端丢失数据，比方说存储在服务的mongodb
---
title: HTML GET请求自动添加参数列表
date: 2018-03-15 11:09:03
tags: [HTML]
---

```html
<form action="/action" method="get">
<textarea name="message"></textarea>
        <input name="author">
        <!-- /?message=输入的内容 -->
        <button type="submit">GET 提交</button>
</form>
<form action="/" method="post">
        <textarea name="message"></textarea>
        <button type="submit">POST 提交</button>
</form>
```

对于GET请求，GET提交之后，浏览器会在`host:port[action]?author=xx&message=xx`, 例如
`localhost:3000/action?author=spencer&message=test`
---
title: windows身份验证
date: 2018-03-22 11:11:57
tags: [Asp.Net, concept, practice]
---

### IPrincipal & IIdentity

IPrincipal定义用户对象的基本功能
IIdentity定义标识对象的基本功能

### Windows Authentication 过程

IIS传递给Asp.Net一个Windows Token, 用这个Token创建一个`WindowsIdentity`对象,然后根据`WindowsIdentity`创建`WindowsPrincipal`对象，之后将这个对象赋值给`HttpContext.User`

```
token = context.WorkerRequest.GetUserToken()
```

### Form Authentication 过程

通过用户名和密码创建一个包含`FormsAuthenticationTicket`的登陆`Cookie`, ASP.NET 解析登陆的`Cookie`然后创建一个`GenericPrincipal`对象,这个对象包含`FormsIdentity`,之后把这个Principal对象赋值给`HttpContext.User`


REF:
[细说ASP.NET Windows身份认证](https://www.cnblogs.com/fish-li/archive/2012/05/07/2486840.html)
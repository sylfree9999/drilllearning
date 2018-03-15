---
title: nginx location匹配
date: 2018-03-14 19:20:31
tags: [nginx, concept]
---

转载补充自http://seanlook.com/2015/05/17/nginx-location-rewrite/

```nginx
location  = / {
  # 精确匹配 / ，主机名后面不能带任何字符串
  [ configuration A ]
}

location  / {
  # 因为所有的地址都以 / 开头，所以这条规则将匹配到所有请求
  # 但是正则和最长字符串会优先匹配
  [ configuration B ]
}

location ^~ /images/ {
  # 匹配任何以 /images/ 开头的地址，匹配符合以后，停止往下搜索正则，采用这一条。
  [ configuration D ]
}

location ~* \.(gif|jpg|jpeg)$ {
  # 匹配所有以 gif,jpg或jpeg 结尾的请求
  # 然而，所有请求 /images/ 下的图片会被 config D 处理，因为 ^~ 到达不了这一条正则
  [ configuration E ]
}

```
* 以```=```开头表示精确匹配
如A中只匹配根目录结尾的请求，后面不能带任何字符串
* ```^~```开头表示uri以某个常规字符串开头，<span style="color: red">**不是正则匹配**</span>
* ```~```开头表示区分大小写的正则匹配
* ```~*```开头表示不区分大小写的正则匹配
* ```/```通用匹配， 如果没有其他匹配，任何请求都会匹配到
* 前缀匹配时，nginx不对url做编码，因此请求```/static/20%/aa```, 可以被规则 ```^~ /static/ /aa``` 匹配到


多个 location 配置的情况下匹配顺序为：
*  首先精确匹配 `=`
*  其次完整路径
*  其次前缀匹配  `^~`
*  其次按文件中顺序的正则匹配
*  匹配不带任何修饰的前缀匹配
*  最后 `/` 通用匹配
*  当有匹配成功的时候，停止匹配，按当前匹配规则处理请求

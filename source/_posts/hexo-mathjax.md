---
title: Hexo Mathjax设置
date: 2019-04-08 18:46:36
tags: [hexo]
---

转自ShallowLearner https://www.jianshu.com/p/7ab21c7f0674

## 问题
hexo自带的hexo-renderer-marked渲染工具会将特殊的Markdown转换成相应的html标签，所以会有可能出错

```stylus
::after {
    content: " ";
    position: absolute;
    -webkit-border-radius: 50%;
    border-radius: 50%;
    background: #fc625d;
    width: 12px;
    height: 12px;
    top: 0;
    left: 20px;
    margin-top: 13px;
    -webkit-box-shadow: 20px 0px #fdbc40, 40px 0px #35cd4b;
    box-shadow: 20px 0px #fdbc40, 40px 0px #35cd4b;
    z-index: 3;
  }
```



## 解决方法
* 更换hexo markdown渲染引擎为hexo-renderer-kramed
  ``` shell
  npm uninstall hexo-renderer-marked --save
  npm install hexo-renderer-kramed --save
  ```

* 解决行内公式的渲染 
  找到`node_modules\kramed\lib\rules\inline.js`
  把`escape`和`em`变量修改为 

  ```javascript
  //  escape: /^\\([\\`*{}\[\]()#$+\-.!_>])/,
  escape: /^\\([`*\[\]()#$+\-.!_>])/
  //  em: /^\b_((?:__|[\s\S])+?)_\b|^\*((?:\*\*|[\s\S])+?)\*(?!\*)/,
  em: /^\*((?:\*\*|[\s\S])+?)\*(?!\*)/
  
  ```

* 重新启动hexo  

  ```shell
  hexo clean
  hexo generate
  ```

* 在主题中开启mathjax开关

  进入主题目录
  找到`_config.yml`
  更改mathjax默认的false为true

  ```yaml
  # MathJax Support
  mathjax:
  enable: true
  per_page: true
  ```
  在Front-matter里打开Mathjax开关

  ```yaml
  ---
  title: index.html
  date: 2016-12-28 21:01:30
  tags:
  mathjax: true
  --
  ```
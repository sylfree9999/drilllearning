---
title: rshiny-concept
date: 2018-04-18 11:29:21
tags: [R, shiny, concept]
---

## Shiny Scope

### Per-session objects

```R
# server.R

shinyServer(func = function(input, output){
		startTime <- Sys.time()
	})
```

`func` is called each time a web brower is pointed to the Shiny application = is called once for each session.

所有在func里面的东西是每个session单独实例化的。这包括`input`和`output`。
每个session有自己的`input`和`output`,只在func中可见。 每个session也会有自己的startTime。

### Objects 所有session可见

适用于需要使用大数据，或者不需要`input`和`output`的工具函数的情况。
只需要把objects定义在shinyServer之外+inside server.R文件即可。

```R

# objects visible across all sessions
bigDataSet <- read.csv('bigdata.csv')

# objects visible across all sessions
utilityFunc <- function(x){

}

shinyServer(function(input,output){

})
```

如果要修改共享objects，**需要使用<<-运算符，<-只针对本地变量**

### Global Objects

Objects defined in `global.R`. 与`所有Session可见Objects`相似，但是不同的是，它同时对于`ui.R`可见。 这是因为他们被加载到了R session的全局环境中。所有的Shiny app的R代码都是运行在这个全局环境或者其子环境中。

实际应用中，这个并不常见。**`ui.R`中的代码只会被执行一次，就是当Shiny app启动时。然后它会生成html 文件，缓存然后传给与其相连的浏览器**。 这种所发当设置一些共享配置的时候可能比较有用。
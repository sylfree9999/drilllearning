---
title: 同步、异步、回调、阻塞、非阻塞、线程、进程、协程
date: 2018-05-14 17:08:40
tags: [concept]
---
作者：Manjusaka
链接：https://www.zhihu.com/question/266222348/answer/304632928
来源：知乎
著作权归作者所有。商业转载请联系作者获得授权，非商业转载请注明出处。

##同步阻塞：

举一点不严谨的例子吧你现在要买一本《人体艺术导论》，但是奶茶东缺货。
最开始你一直刷新页面，等着书到货了，这是**同步阻塞**。

##同步非阻塞
你觉得这样太浪费时间了。你就去去汤不热看点照片压压惊，然后时不时的去刷一下图书状态是否有货，这是同步非阻塞。

##异步阻塞
好了，你最后成功买到《人体艺术导论》这本书。
某一天，你想去再去买一本《知乎撕逼指南》，抱歉你运气很差，还是没货了那么现在你觉得不断的刷是否有货太傻了
你现在奶茶东上设置了一下，当有货的时候给你响起 FBI Warning 的闹钟。
好了，你现在一直等着闹钟的想起，这叫异步阻塞。

##异步非阻塞
你还是觉得，我怎么能这么傻于是你去干点奇遇事情，等闹钟响起的时候，你就下单。这叫异步非阻塞OK，明白了 前面四个概念么？

都是在奶茶东买书，
基本版的奶茶东，同步，我们只能手动去不断查询书是否有货
设置闹钟后的奶茶东，异步，奶茶东可以在有货的时候主动通知我们
**阻塞**，在书籍有货之前，我们都没法干其余的事情
**非阻塞**，在书籍有货之前，我们可以干其余的事情

##回调
好了，现在你觉得自己下单太傻了，你在奶茶东上做了更进一步的设置。当这本书有货的时候，帮我下单。这就是回调

好了，进程，线程，协程
你现在要买十本书，每本书都可能没货，现在你觉得这个工作太繁琐了
你开了十家公司，每个公司分别帮你购买一本书，公司->进程
你开了一家公司，公司里找了十个人，每个人帮你购买一本书，人->线程
你开了一家公司，找了一个人，用十个手机，每个手机帮你购买一本书，手机->协程

##并发并行
并发和并行是相对的一个概念
并发：交替做不同事的能力
并行：同时做不同事的能力

举个例子，回到买书的问题，有个妹子，找你想让你帮忙买四本书，
你找了两个人，一个人买两本书，对于买书的人而言，购买两本书的操作交互进行，这是并发。
对你而言，你将四本书分别交给两个人同时购买，这是并行。
对于妹子而言，你一个人交替购买四本书，这是并发。

事件循环是什么？前面不是说了么你购买书，想收到有货通知，想有货自动下单，但是你自己不知道怎么搞定，你把这个事情交给奶茶东。奶茶东->事件循环
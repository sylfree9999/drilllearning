---
title: Linux 小概念
date: 2018-04-17 10:34:43
tags: [linux, concept]
---

## & 后台执行

如果在界面输入 `./test.sh &`会
*	在终端显示进程号2333
*	test.sh的结果会输出到终端
*	输入 `Ctrl+C`, 会发出`SIGINT`信号，**程序会继续运行**
*	但是关掉session之后， 程序会收到`SIGHUP`信号，**程序关闭**

## nohup

如果在界面输入`nohup ./test.sh`
*	前台没有出现进程号
*	有一个“忽略输入，输出到nohup.out”的提示
*	test.sh里面的结果也没有输出到前台上
*	输入`Ctrl+C`,**进程关闭**
*	关掉session之后，**进程仍然存在**

<span style="color: red">所以一般都是nohup与&共同使用，这样可以让程序同时免疫SIGINT和SIGHUP信号</span>

## () 开新的子进程shell执行

单独踢到后台&，如果当前命令界面关掉，这个命令界面执行的所有命令都会被关掉
开新的子进程就不会

`(python3 server.py >> output.txt & )`

## touch

`touch x.txt`
如果x.txt存在就更新修改时间
如果x.txt不存在就创建文件

## history/grep

`history` 查看历史命令
`grep` 查找

`history | grep touch` 把历史记录里所有的touch拿出来
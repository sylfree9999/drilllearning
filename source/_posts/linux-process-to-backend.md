---
title: linux-process-to-backend
date: 2018-03-28 19:18:47
tags: [linux, concept]
---

[Ref: Linux 技巧：让进程在后台可靠运行的几种方法](https://www.ibm.com/developerworks/cn/linux/l-cn-nohup/)

如果SSH登陆了远程Linux服务器，经常为Connection Timeout, 这样会自动kill掉正在运行的任务。
如何让命令提交后不受本地关闭终端窗口/网络断开连接的干扰？

## nohup/setsid/&

当用户注销logout或者网络断开时终端会收到`HUP`(hangup) 信号从而关闭所有子进程。
因此为解决这个问题：
要么让进程忽略HUP信号
要么让进程运行在新的会话里从而成为不属于此终端的子进程

1. nohup， 让进程忽略HUP信号

nohup，标准输出和标准错误缺省会被重定向到nohup.out文件中。
一般我们可在结尾加上`&`来将命令同时放入后台运行

```
[root@pvcent107 ~]# nohup ping www.ibm.com &
[1] 3059
nohup: appending output to `nohup.out'
[root@pvcent107 ~]# ps -ef |grep 3059
root      3059   984  0 21:06 pts/3    00:00:00 ping www.ibm.com
root      3067   984  0 21:06 pts/3    00:00:00 grep 3059
[root@pvcent107 ~]#

```

2. setsid

如果进程不属于接受HUP信号的终端的子进程，就要用setsid.

```
[root@pvcent107 ~]# setsid ping www.ibm.com
[root@pvcent107 ~]# ps -ef |grep www.ibm.com
root     31094     1  0 07:28 ?        00:00:00 ping www.ibm.com
root     31102 29217  0 07:29 pts/4    00:00:00 grep www.ibm.com
[root@pvcent107 ~]#

```

注意的是我们的进程31094其父进程为1（`即为init进程ID`），**并不是当前终端的进程ID**

3. &

将`&`也放入`()`,所提交的作业不会出现在作业列表中，就是无法通过jobs来查看。
subshell示例:

```
[root@pvcent107 ~]# (ping www.ibm.com &)
[root@pvcent107 ~]# ps -ef |grep www.ibm.com
root     16270     1  0 14:13 pts/4    00:00:00 ping www.ibm.com
root     16278 15362  0 14:13 pts/4    00:00:00 grep www.ibm.com
[root@pvcent107 ~]#
```

新提交的进程父ID为1（init进程ID）
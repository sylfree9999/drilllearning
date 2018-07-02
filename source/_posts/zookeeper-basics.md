---
title: zookeeper-basics
date: 2018-06-27 11:17:29
tags: [linux, zookeeper, pratice]
---

## 概念

zookeeper是一个分布式协调服务
提供的服务涵盖：主从协调、服务器节点动态上下线、统一配置管理、分布式共享锁、统一名称服务...

zookeeper可靠性很高，本身内部就是个集群，只要集群里面有半数以上的结点存活就可以提供服务

本质上zookeeper就只有两个功能：
1，管理（存储，读取）用户提交的数据；
2，并为用户程序提供数据节点监听服务；

## 安装
tar -zxvf zookeeper.XXX.tar.gz
nano conf/zoo.cfg
add
bin/zkServer.sh start


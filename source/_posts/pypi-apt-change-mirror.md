---
title: Pypi apt-get 更换镜像
date: 2018-05-22 15:12:14
tags: [linux, practice]
---

### Pypi

*	临时使用
```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple some-package
```

*	设默认

没有的话就创建一个以下文件，把 `index-url`改成tuna,例如
	*	Linux: `~/.config/pip/pip.conf`
	*	Windows 10: `%APPDATA%\pip\pip.ini`
	*	Mac OS: `$HOME/Library/Application Support/pip/pip.conf`
```
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
```

如果pip和pip3并存，只需要修改`~/.pip/pip.conf`


### Apt-get

Ubuntu的软件源配置文件为`/etc/apt/sources.list`
*	给系统的list备份
*	整个修改sources.list的文件为下文档：

```
# 默认注释了源码镜像以提高 apt update 速度，如有需要可自行取消注释
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-updates main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-backports main restricted universe multiverse
deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-security main restricted universe multiverse

# 预发布软件源，不建议启用
# deb https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
# deb-src https://mirrors.tuna.tsinghua.edu.cn/ubuntu/ xenial-proposed main restricted universe multiverse
```

*	修改完毕记得 `sudo apt-get update`
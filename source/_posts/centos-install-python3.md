---
title: CentOS Install Python3, pip3 and Coexist Python2
date: 2018-04-16 17:58:25
tags: [linux, practice]
---

## Install Python3

```linux
$ sudo yum groupinstall "Development Tools"

$ sudo yum -y install zlib*

$ sudo mkdir /usr/local/python3 # 创建安装目录

# 下载 Python 源文件
$ wget --no-check-certificate https://www.python.org/ftp/python/3.6.0/Python-3.6.0.tgz
# 注意：wget获取https的时候要加上：--no-check-certificate

$ tar -xzvf Python-3.6.0.tgz # 解压缩包

$ cd Python-3.6.0 # 进入解压目录

$ sudo ./configure --prefix=/usr/local/python3 # 指定创建的目录

$ sudo make

$ sudo make install

```

## Python2 Python3 共存

创建python3软链接
这样可以用`python`命令使用Python2， `python3`来使用Python3

```linux
$ sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python3
```

## 默认使用Python3

先将现有的python备份， 用`which python`来看：

```linux
$ which python
/usr/bin/python

$ cd /usr/bin
$ sudo mv python python.bak
```

然后创建软链接

```linux
$ sudo ln -s /usr/local/python3/bin/python3 /usr/bin/python
```
这样默认的python版本就替换成Python3了

另外由于yum使用Python2,替换后python3可能无法正常工作，所以修改yum配置文件

```linux
sudo vi /usr/bin/yum
```
将第一行从 `#!/usr/bin/python`改为`#!/usr/bin/python2.7`

## Install Pip3

```linux
# 下载源代码
$ wget --no-check-certificate https://github.com/pypa/pip/archive/9.0.1.tar.gz

$ tar -zvxf 9.0.1 -C pip-9.0.1    # 解压文件

$ cd pip-9.0.1

# 使用 Python 3 安装
$ python3 setup.py install
```

创建软链接

```linux
$ sudo ln -s /usr/local/python3/bin/pip /usr/bin/pip3
```

升级pip

```linux
$ pip install --upgrade pip
```
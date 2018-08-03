---
title: python-file
date: 2018-08-03 20:05:57
tags: [python, concept]
---

## 文件读写操作

### 读文件
#### 方法一
```python
# 默认是只读
file1 = open("test.txt")
# w是全部重写，a是append到最后
file2 = open("output.txt","w")

while True:
	line = file1.readline()
	file2.write('"' + line + '"' + ".")
	if not line:
		break

file1.close()
file2.close()
```
读文件有3种方法：
1，read()将文本文件所有行读到一个字符串中
2，readline()是一行行读
3，readlines()是将文本文件中所有行读到一个List中，文本文件每一行是list的一个元素。

#### 方法二
文件迭代器
```python
file2 = open("output.txt","w")
for line in open("test.txt"):
	file2.write('"' + line + '"' + ".")
file2.close()
```

#### 方法三
文件上下文管理器
```python
#用with.open自带关闭文本的功能
with open('somefile.txt','r') as f:
	data = f.read()
	for line in f:
		#处理每一行

```

## 二进制文件读写
python默认读取的都是文本文件。要是想要读取二进制文件，需要把刚刚的"r"/"w"改成"rb"

任何非标准的文本文件（Python2-ASCII, Python3-unicode）你就需要用二进制读入这个文件，然后再有`.decode('...')`的方法来解码这个二进制文件
```python
f = open('ABC.jpg','rb')
u = f.read().decode('ABC')
```
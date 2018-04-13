---
title: python open() 文件操作
date: 2018-04-13 15:41:53
tags: [python, concept]
---

open()打开一个文件并返回一个`file`对象

```python
open('log.txt', 'a', encoding='utf-8')
```


```python
open(name, mode, buffering=1, encoding=None, errors=None, newline=None, closefd=True, opener=None)
```

* name: 要访问的文件名称
* mode:	决定打开文件的模式：
	
	模式	|	描述
	---	|	---
	r	|	默认方式， 只读， 文件指针在文件开头
	w	|	写入，如果文件存在覆盖，不存在创建
	a 	|	打开文件追加，如果文件存在文件指针放在文件结尾，不存在创建
	x	|	exclusive creation, fail if file already exists
	b 	|	二进制格式
	t	|	文本格式(默认)	
	+	|	打开文件读写
	

* buffering： buffering=0,不会寄存; buffering=1,寄存; buffering>1, 表示寄存区的缓冲大写; buffering<0,寄存区缓冲大小为系统默认
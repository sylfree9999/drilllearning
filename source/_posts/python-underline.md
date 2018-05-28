---
title: Python 单下划线，双下划线变量
date: 2018-05-22 10:21:17
tags: [python, concept]
---

### 单下划线开头

*	常用于模块中
*	单下划线开头`_xx`变量和函数被默认认为内部函数，treated as `private` by a programmer. 即如果用`from module import *`时，这部分的变量和函数不会被导入，但是可以通过**module._xx**来访问

### 单下划线结尾

*	通常与Python关键词区分开来，比方说一个Python关键词为cls，我也需要定义一个cls，可以写成cls_

### 双下划线开头

* 	This is not a convention. It has a specific meaning to the interpreter.
* 	Python Name Mangling
* 	__spam(2 leading underline and **at most one trailing underline**) will be replaced with `_classname__spam`, where `classname` is the current class name.
*	If you create a subclass of `A`, say `B` then you can't easily override `A's` __method_name

```Python
>>> class A(object):
		def _internal_use(self):
			pass
		def __method_name(self):
			pass
>>> dir(A())
['_A__method_name',...,'_internal_use']
```	

### 双划线开头，双划线结尾
*	Python自己的`魔术`对象, used by Python itself. 比方说__init__, __del__, __add__, __getitem__ 以及全局的__file__, __name__等。 不要试图重写他们
---
title: Python 可变参数，关键字参数
date: 2018-03-15 11:13:36
tags: [python, concept]
---

+ 可变参数\*args
	+ 变的是个数
	+ 在函数调用的时候自动组装为一个tuple
	+ 传入的时候直接传值即可

+ 关键字参数\*\*kwargs
	+ 在函数调用的时候自动组装为一个dictionary
	+ 传入的时候必须是以含参数名的形式传递

```python
def func(a, b, c=0, *args, **kwargs):
	print ('a=', a, 'b=', b, 'c=', c, 'args=', args, 'kwargs=', kwargs)
 
if __name__ == '__main__':
	func(1,2,3,spence,shao,name='spence',gender='male')
 
>>>a=1,b=2,c=3,args=(spence,shao),kwargs={'name':'spence','gender':'male'}
```
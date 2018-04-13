---
title: python class
date: 2018-04-13 17:16:07
tags: [python, concept]
---

## class继承

```python
class Animal(Object)：
	def cry(self):
		print("Animal shouts")

class Dog(Animal):
	def cry(self):
		print("Wang wang")

>>> dog = Dog()
>>> dog.cry() //覆盖了父类Animal的cry()方法
Wang wang

```

## class访问限制

私有变量，可以把属性的名称前加上**两个**下划线`__`

```python
class Student(object):
	def __init__(self, name, score):
		self.__name = name
		self.__score = score

	def get_name(self):
		return self.__name
```

但是以`__`开头`__`结尾的，是<span style="color: red; font-weight: bold;">特殊变量</span>, 特殊变量可以直接访问，不是private变量

如果变量名前面只有**一个**下划线`_`，这样的实例变量外部可以访问，但是by convention, 虽然可以方位，但请把我视为私有变量，不要随意访问

**注意！！！**

```python
>>> bart = Student('Bart Simpson', 59)
>>> bart.get_name()
'Bart Simpson'
>>> bart.__name = 'New Name' # 这里设置__name变量, 是相当于新加了一个__name变量，而真正的变量已经被Python解释器变为_Student__name
>>> bart.__name
'New Name'
>>> bart.get_name() # get_name()内部返回self.__name
'Bart Simpson'
```

## 获得一个对象的所有属性和方法

```python
>>> dir('ABC')
['__add__', '__class__',..., '__subclasshook__', 'capitalize', 'casefold',..., 'zfill']
>>> len('ABC') #内部相当于调用了该对象的__len__()方法
3
>>> 'ABC'.__len__()
3
```

## 实例属性和类属性

实例绑定属性通过`self`变量：

```python
class Student(object):
    def __init__(self, name):
        self.name = name

s = Student('Bob')
s.score = 90
```

类属性直接在类下面定义,这个属性可以被所有类的实例访问到

```python
class Student(object):
    name = 'Student'

>>> s = Student() # 创建实例s
>>> print(s.name) # 打印name属性，因为实例并没有name属性，所以会继续查找class的name属性
Student
>>> print(Student.name) # 打印类的name属性
Student
>>> s.name = 'Michael' # 给实例绑定name属性
>>> print(s.name) # 由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
Michael
>>> print(Student.name) # 但是类属性并未消失，用Student.name仍然可以访问
Student
>>> del s.name # 如果删除实例的name属性
>>> print(s.name) # 再次调用s.name，由于实例的name属性没有找到，类的name属性就显示出来了
Student
```

## @staticmethod和@classmethod

一般是用类方法需要先实例化一个对象再调用方法
但是使用了@staticmethod以及@classmethod，可以直接`类名.方法名()`调用

它们的区别：
*	@classmethod处理仅跟这个类相关的方法，跟instance无关。当@classmethod被调用的时候，是把这个class作为第一个参数传进去，而不是这个类的实例。也就是说你可以直接在这个@classmethod里面用类属性，而非从一个类实例里面使用


*	@staticmethod，当调用这个方法的时候，我们**甚至不用把类传进去**，也就是说我们可以把这个方法放到类里面，但是这个方法其实根本不需要这个类或者实例，比方说设置一些环境参数，更改别的类的属性之类的。

```python

class Kls(object):
    def __init__(self, data):
        self.data = data
 
    def printd(self):
        print(self.data)
 
    @staticmethod
        def smethod(*arg):
            print('Static:', arg)
 
    @classmethod
        def cmethod(*arg):
            print('Class:', arg)

>>> ik = Kls(23)
>>> ik.printd()
23
>>> ik.smethod()
Static: ()
>>> ik.cmethod()
Class: (<class '__main__.Kls'>,)
>>> Kls.printd()
TypeError: unbound method printd() must be called with Kls instance as first argument (got nothing instead)
>>> Kls.smethod()
Static: ()
>>> Kls.cmethod()
Class: (<class '__main__.Kls'>,)

```
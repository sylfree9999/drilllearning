---
title: python-oop
date: 2018-08-02 16:40:55
tags: [python, concept]
---

## 创建类
1，类中函数的第一个参数必须是self,它是为了指代它所存在的类
2，构造函数用__init__表示
```python
#创建类
class Foo:

	name = 'Jan'
	#类里面的函数,类中第一个参数必须是self，指代本类的东西
	def bar(self):
		pass

	def hello(self, name):
		print('self name {0}'.format(self.name)) #指Jan
		print('I am {0}'.format(name))

	def __init__(self): #其职责就是在模型创建初期完成一些动作
		self.name = "Jan2"

obj=Foo()
obj.bar()
obj.hello('july')

obj1 = Foo()
obj2 = Foo()
```

## 访问限制
1，直接在构造函数中用self.xx赋值会导致xx外界也能访问
2，`self.__name = name`,这样写就是告诉python `__name`不能被外界访问
3，如果既要保证安全，又要能被外部更改呢？用getter+setter
```python
class Student:
	def __init__(self,name,age):
		self.name = name #用self赋值在类中别的方法也能直接访问的到
		self.age = age
		self.__name2 = name
		self.__age = age
	
	def detail(self):
		print(self.name)
		print(self.age)
		print(self.__name)
		print(self.__age)

	def get_name(self):
		return self.__name

	def set_name(self,name):
		self.__name = name

LiLei = Student('LiLei',12)
LiLei.age = 20 #外界可以更改，访问age
Lilei.__age = 20 #不能被更改
```

## 继承
```python
class PrimaryStudent(Student):
	def lol(self):
		print("lalalala")

class CpllegeStudent(Student):
	#这里改写了父类的构造函数
	def __init__(self,name,age,gender):
		self.__name = name
		self.__age = age
		self.__gender = gender

	def gender_detail(self):
		print(self.__gender)

obj1 = PrimaryStudent('向往',7)
obj1.lol()
obj1.detail()#继承爸爸的方法
```

## python 类属性和实例属性

```python
class A():
	a = 10
# scenario1
obj1 = A()
obj2 = A()
print(obj1.a,obj2.a,A.a)

# scenario2
obj1.a += 2
print(obj1.a,obj2.a,A.a)

# scenario3
A.a += 3
print(obj1.a,obj2.a,A.a)
```

情形1的结果是：`10 10 10`；
情形2的结果是：`12 10 10`；
情形3的结果是：`12 13 13`；

**为什么呢？**
在python中， `A`属于类对象，`obj1`属于实例对象，从对象的角度上来说，`A`与`obj1`是两个无关的对象，但是，Python通过下面的查找树建立了对象`A`与实例对象`obj1`,`obj2`之间的关系

```
		A
		|
	---------
	|		|
	obj1	obj2	
```
当调用`A.a`的时候，直接从`A`获取属性`a`
在scenario1中调用`obj1.a`,python按照从`obj1`到`A`的顺序自下到上查找属性`a`
注意的是**在这个时候，`obj1`是没有属性`a`的**，所以python到Class `A`中找，找到并返回

在scenario2中`obj1.a += 2`包含了**属性获取以及属性设置**两个操作
属性的获取和上面一样，按照查找规则进行，即这个时候找到了类`A`的属性`a`
但是当进行属性的设置时，**`obj1`这个实例对象没有属性`a`，因此会自身动态添加一个属性`a`**
自此，类`A`和实例`obj1`都有自己的一个属性

那么，在scenario3中，再次调用`obj1.a`的时候，按照**就近原则**，找到的时实例对象的`a`，所以返回12，对于`obj2.a`由于一开始没有自己的实例对象`a`,所以返回的时类`A`的`a`，也就是13

可以验证，如果手动删除`obj1.a`，那么当再次调用`obj1.a`的时候，返回的会是13
```python
del obj1.a
print(obj1.a)
```
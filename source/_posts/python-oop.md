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
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
4，python中，如果变量名类似`__x__`,以双下划线开头和结尾的，是特殊变量，特殊变量可以直接访问，不是private变量
5，如果变量名是以一个下划线开头的`_x`，这样的实例变量外部是可以访问的，但是按照约定俗称的规定，这类变量**虽然可以访问，但是请视为私有变量，不要随意访问**
```python
class Student:
	def __init__(self,name,age):
		self.name = name #用self赋值在类中别的方法也能直接访问的到
		self.age = age
		self.__name = name
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

class CollegeStudent(Student):
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

## python 装饰器
1，主要用于AOP
2，简单版，等同于`use_logging(foo())`
```python
def use_logging(func):

    def wrapper():
        logging.warn("%s is running" % func.__name__)
        return func()
    return wrapper

@use_logging
def foo():
    print("i am foo")

foo()
```
3，带业务函数参数\*args,\*\*kwargs
```python
def wrapper(*args, **kwargs):
        logging.warn("%s is running" % func.__name__)
        return func(*args, **kwargs)
    return wrapper
```
4，装饰器本身带参数
这种写法本质上就是把原本real_decorator这个装饰器再在外面包一层装饰器
```python
def makeHtmlTag(tag,*args,**kwds):
    def real_decorator(fn):
        css_class = " class '{0}'".format(kwds["css_class"]) if "css_class" in kwds else ""

        def wrapped(*args, **kwds):
            return "<"+tag+css_class+">"+fn(*args,**kwds)+"</"+tag+">"
        return wrapped
    return real_decorator

@makeHtmlTag(tag="b", css_class="bold_css")
@makeHtmlTag(tag="i", css_class="italic_css")
def hello(*s,**kwds):
    return "hello world!{0}{1}".format(s,kwds)

print(hello('spencer','shao',name="ss",surname="shao"))
#结果为：<b class 'bold_css'><i class 'italic_css'>hello world!('spencer', 'shao'){'name': 'ss', 'surname': 'shao'}</i></b>
```
5，类装饰器
注意，这里调用顺序会先是decorator的init函数，

```python
class makeHtmlTagClass(object):
	def __init__(self, tag, css_class=""):
		print("inside makeHtmlTagDecorator.__init.__()")
		self._tag = tag
		self._css_class = " class '{0}'".format(css_class) if css_class != "" else ""

	def __call__(self, fn):
		def wrapped(*args, **kwargs):
			print("inside makeHtmlTagDecorator.__call__()")
			return "<"+self._tag+self._css_class+">"+fn(*args,**kwargs)+"</"+self._tag+">"
		return wrapped


@makeHtmlTagClass(tag="b", css_class="bold_css")
@makeHtmlTagClass(tag="i", css_class="italic_css")
def hello(name):
	return "Hello, {}".format(name)
print("Finished decorating hello()")

print(hello("Baby"))

#输出结果顺序为：
#inside makeHtmlTagDecorator.__init.__()
#inside makeHtmlTagDecorator.__init.__()
#Finished decorating hello()
#inside makeHtmlTagDecorator.__call__()
#inside makeHtmlTagDecorator.__call__()
#<b class 'bold_css'><i class 'italic_css'>Hello, Baby</i></b>

```
6，装饰器副作用
原本的函数变成了一个wrapper函数，所以会丢失原本函数的一些元信息，比方说__name__, \_\_doc__之类 
这个时候可以用Python的functools
```python
from functools import wraps
def hello(fn):
	@wraps(fn)
	def wrapper():
		print("Hi,{0}".format(fn.__name__))
		fn()
		print("Bye,{0}".format(fn.__name__))
	return wrapper

@hello
def foo():
	print("Foo")

foo()
```

## __slots__

1，可以限制class实例能够添加哪些属性
2，\_\_slots__只对当前类的实力起作用，对继承的子类不求作用

## property

## 类的特殊方法和定制

### __str__
1，返回用户看到的字符串
2，convert an object to a string
3，与toString()十分类似，也可以override这个方法
 
```python
class MyClass:
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return "Hello" + self.name

print(MyClass('Tome')) # Hello Tome 
# 如果没有def __str__，则默认打印的是<__main__.MyClass object at 0x109afb190>
```

### str()与repr()
1，Example of str()
```python
s = 'Hello, Geeks.'
print str(s)
print str(2.0/11.0)
```
output:
```
Hello, Geeks.
0.181818181818
```

2，Example of repr()
```python
s = 'Hello, Geeks.'
print repr(s)
print repr(2.0/11.0)
```
output:
```
'Hello, Geeks.'
0.18181818181818182
```

3，Difference:
	** str() is used for creating output for end users/ repr() is mainly used for debugging and development
	** repr() shows a representation that has all information about the object/ str() is sued to show a representation that is useful for printing the object
	** Both of them can be overriden for any class and there are minor differences.If both are defined, function defined in __str__ is used.


### __iter__
1，如果一个类想要被用于`for ... in`循环，就必须实现一个`__iter__()`方法，该方法返回一个迭代对象，在`def __iter__(self)`里实力本身就是迭代对象，所以返回自己`self`即可，主要是在`__next__`里面写逻辑，知道遇到`StopIteration`错误时退出循环

```python
class Fib100:
	def __init__(self):
		self._1, self._2 = 0, 1

	def __iter__(self):
		return self

	def __next__(self):
		self._1, self._2 = self._2, self._1 + self._2
		if self._1 > 100:
			raise StopIteration()
		return self._1

for i in Fib100():
	print(i)
```

### __getitem__
1，如果想实现下标访问，就需要实现`__getitem__`
```python
class Fib(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a

f = Fib()
f[0]
```

### __call__
```python
class MyClass:
	def __call__(self):
		print("U can call cls() directly")

cls = MyClass()
cls()

print(callable(cls))
print(callable(max))
```

## 元类MetaClass
1，python是动态语言，是在运行时编译的
2，用`type`动态生成一个类,第二个参数是继承自什么，一定要显式写成元组类型
```python
def init(self, name):
	self.name = name

def say_hello(self):
	print('Hello {0}'.format(self.name))

Hello = type('Hello',(object, ), dict(__init__ = init, hello = say_hello))

h = Hello('Tom')
h.hello()
```
3，metaclass就是为了控制类的创建过程，就是告诉用户我这个class有哪些方法，存在attrs的表里面，attrs就是函数和方法的一个表
```python
def add(self, value):
	self.append(value)

class ListMetaClass(type):
	def __new__(cls, name, bases, attrs):
		attrs['add'] = add
		attrs['name'] = 'Jerry'
		return type.__new__(cls, name, bases, attrs)

class MyList(list, metaclass = ListMetaClass):
	pass

mli = MyList()
mli.add(1)
mli.add(2)

print(mli.name) # Jerry
print(mli) # [1,2]

```
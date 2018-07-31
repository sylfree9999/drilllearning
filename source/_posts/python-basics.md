---
title: python-basics
date: 2018-07-31 10:05:37
tags: [python, concept]
---
PYTHON 3.6

## 字符串换行
1，字符串中末尾加"\"最终会打印出一行
2，字符串换行方法一加\n
3，字符串换行方法二用多行写法
```python
str = 'abcd' \
		'efgh'
# 结果是abcdefgh
print(str)

#结果是Hello
#world
str = 'Hello\nworld!'
print(str)

#结果是Hello
#world
str = """Hello
world!
"""
```
## 单引号与双引号
1，单引号里可以直接写双引号
2，双引号里可以直接写单引号
3，单/双引号里面要单/双引号，则需要转义

<!--more-->

```python
# abc"123"efg
print('abc"123"efg')
# abc'123'efg
print("abc'123'efg")
# abc'123'efg
print('abc\'123\'efg')
# abc"123"efg
print("abc\"123\"efg")
```

## 常见字符串处理
1，取出空格及特殊符号strip,lstrip,rstrip
2，复制字符串：str1 = str2
3，连接字符串
	str2 += str1
	new_str = str2 + str1
4，查找字符串：pos = str1.index(str2)
5，比较字符串：str1 == str2/str1 < str2
6，字符串长度：len(str)
7，大小写转换：
	u_str = str.upper()
	l_str = str.lower()
8，首字母大写：str.capitalize();string.capword(str)
9，分割与合并字符串：split,splitlines,join
10，类型转换：int，float转换
11，格式化字符串
12，不能修改字符串
```python
import string

s = 'abc'
#报错
s[0] = 'd'

#去除空格
 s = ' abcd efg '
 print(s.strip()) #返回的是新的字符串
 print(s.lstrip())
 print(s.rstrip())

# 字符串的连接
s1 = 'abc'
s2 = 'def'
print(s1 + "\n" + s2)

# 位置比较
s_1 = 'abcdefg'
s_2 = 'abdeffxx'
print(s_1.index('bcd')) # 1
print(s_2.index('bcd')) # Exception

# 空字符串 不能写成 == False，不等于None
# 空字符串在内存中还是被分配了对象的
# 
s = ''
if not s:
	print('Empty')

# 字符串的分割和连接
s = 'abc,def,ghi'
splitted = s.split(',')
print(typeof(splitted)) #<class 'list'>
print(splitted)#['abc','def','ghi']

s="""abc
def
ghi
"""
s_1 = s.splitted('\n')
s_2 = s.splitlines()
print(s_1)
print(s_2)

# 字符串的连接
s = ['abc','def','ghi']
print(''.join(s))
print('-'.join(s)) # abc-def-ghi

#常用判断
print('1234abcd'.isalnum())
print('\t12ab'.isalnum())#False
print('abcd'.isalpha())
print('12345'.isdigit())
print('  '.isspace())

#数字到字符串
print(str(5))
print(str(5.))
print(str(5.12345))
#字符串到数字
print(int('1234'))
print(float('1234.56'))
print((int('ffff',16)) #16进制的ffff转成10进制
```

## 条件判断
```python
# None的判断
x = None
if not x:
	print('None')
else:
	print('Not None')

if x is None:
	print('None')

# for
for i in range(start,end,step):
	print(i)  
```

## 函数
```python
#默认参数
def func(x,y = 500):
	return x+y
print(func(100)) # 600


def func(p):
	print('x=',p['x'])
	print('y=',p['y'])

print(func({'x':100,'y':200}))


#可变参数，*告诉pytnhon后面都放到这个numbers数组
#这样写有一个问题，你传进去的可变tuple每个元素是没有名字的，你除非知道他们的索引才能用
def func(name,*numbers):
	print(numbers[0])
	print(numbers[3])
	print(type(numbers)) #Tuple
# tuple = 只读数组
func('tom',1,2,3,4,"Hello")

#可变参数方法二, **代表key/values的字典
def func(name,**kvs):
	print(type(kvs)) #<class 'dict'>
	print(kvs)#{'uk':'London','china':'Beijing'}
func('Tom',china="Beijing",uk="London")

def func(a,b,c,*,china,uk):
	print(china,uk)

func(1,2,3,china='BJ',uk='LD')

# 函数可以作为参数
def sum(x,y,p=None):
	s = x+y
	if p:
		p(s)
	return s

sum(100,200,print)
```

## 变量
**经常会碰到这样的错误：
local variable 'a' referenced before assignment**

```python
a = 3
def func():
	print(a)
	a = a+1 #这一句会报错
func()
```
<span style="color: red">a=3定义了全局变量a，作用域从定义处到代码结束，在a=3以下的函数中是可以引用全局变量a的，但是如果要修改函数中与全局变量同名的变量，在函数中的该变量就会变成局部变量，在修改之前对该变量的引用就会引发为定义的错误,**所以，哪个函数需要修改全局变量，就需要在这个函数中声明一下，但是有一个函数不需要声明，就是主函数**</span>

```c#
a = 3
def func():
	global a
	print(a)
	a = a+1 #这一句会报错
func()

if __name__ == "__main__":
    print (a)  # 2
    a = a + 1
    Fuc()
    print (a)  # 3
```

**********************练习***********************

1，求100以内的素数
```python
#找素数,1不是素数，最小的质数/素数为2
#素数的概念，除了1和它本身外，不能被其他自然数整除
primeArray = []
def findPrimeNumber(num):
    for i in range(2,num+1):
        if i ==2:
            primeArray.append(i)
        else:
            for j in range(2,i+1):
                if i%j == 0:
                    break
                else:
                    primeArray.append(i)

findPrimeNumber(5)
print(primeArray)
```

2，冒泡排序
```python
#冒泡排序
def bubbleSort(array):
    for i in range(len(array)-1,0,-1):
        for j in range(i):
            if array[j] > array[j+1]:
                temp = array[j]
                array[j] = array[j+1]
                array[j+1] = temp
        print(array)

bubbleSort([54,26,100,17,77])
```
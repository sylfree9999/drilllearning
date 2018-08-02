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

## AND/OR
1，AND/OR**不一定只会返回True/False**
2，**AND** return the first Falsey value if there are any, else return the last value in the expression
3，**OR** return the first Truthy value if there are any, else return the last value in the expression

```python
[] and [] + [1,2] # returns []
#Spotted,[] and [] + [1,2] is actually this: [] and ([] + [1,2]),你必须把后面的+[1,2]与前面的[]看作是一个整体

[] + [1,2] # returns [1,2]

10 or 7 - 2 # returns 10,同理，10 or (7 - 2)要看成这种形式
```


## 循环for/else
<span style="color: red">`for` loop也有一个`else`</span>
`else` 是在loop正常结束后执行的，也就是说这个loop没有`break`

下面这个是一个基本的
```python
for item in container:
	if search_something(item):
		#Found it!
		process(item)
		break
	else:
		#Didn't find anything
		not_found_in_container()
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

##**********************练习***********************

1，求100以内的素数
```python
#找素数,1不是素数，最小的质数/素数为2
#素数的概念，除了1和它本身外，不能被其他自然数整除

def findPrimeNumber(num):
    for i in range(1,num+1):
        if i > 1:
            for j in range(2,i):
                if i%j == 0:
                    break
            else:
                 print(i)

findPrimeNumber(100)
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

## 容器
1，list列表，索引从0开始，列表的数据项不需要具有相同的类型
2，tuple元组，只读列表
3，dist字典
4，set集合，是一个无序不重复的数组

5，not XX 和 is None不是一回事，not XX代表其还是在内存分配空间了的
6，切片，切出一个子数组
7，生成器，只有用到的时候才去计算，不用的时候不算,用next/for来循环,非常省内存
8，迭代器，如果是Iterable,则可以用for来循环，如果是Iterator则说明是生成器

```python
#list/tuple基本操作
li = [1,2,3,'tete',[1,2,3],{1:'one',2:'two'}]
print(type(li))# class list

# 元素访问
print(li[0])
#倒数第一个元素
print(li[-1])

# 查找元素位置
print(li.index('tete')) #3
print(li.index([1,2,3])) #4
print(li.index(-1)) # error

# 添加元素
l_a = [1,2]
l_a.append(4)
l_a.append(5)
#如果想要一次性加多个元素进去，就需要用extend,否则如果用append，会把其作为一个list，添加到原list中
l_b = [6,7,8]
l_a.extend(l_b)

# 删除元素
del(li[-1]) # del(list[index])

# 判断容器是否为空

l_a = []
if not l_a:
	print('Empty') # print this
if l_a is None:
	print('None')

# 遍历
for i in li:
	print(i)
for i in range(len(li)):
	print(li[i])

# 元组
t = (1,2,3,'456')
t[0]='a' # error,不可以修改

# 字典
d = {'a':1,'b':2,1:'one',2:'two'}
print(d[1]) #根据key来做访问
# 判断元素是否存在，是判断key是否存在
print('c' in d) # false
print(1 in d) # true
# 添加
# 删除
del(d[2])
# 遍历
for key in d:
	print(d[key])

for key, value in d.items():
	print(key,value)

keys = d.keys()
print(keys)

# set
s_a = set([1,2,2,3,4,5,6])
s_b = set([4,5,6,7,8])
print(s_a)# {1,2,3,4,5,6}

# 判断元素是否存在
print(5 in s_a)
# 并集
print(s_a | s_b) #{1，2，3，4，5，6，7，8}
print(s_a.union(s_b))
# 交集
print(s_a & s_b)
print(s_a.intersection(s_b)) #生成一个新的set {4，5，6}
# 差集(a - a&b )
pprint(s_a - s_b)
print(s_a.difference(s_b)) #{1,2,3}
# 对称差(A|B) - (A&B)，把两个集合相同的元素去除
print(s_a ^ s_b)
print(s_a.symmetric_diff(s_b)) #{1,2,3,7,8}
# 添加
s_a.add('x')
s_a.update([4,5,60,70])
# 删除，因为set没有索引，要直接删值
s_a.remove(70)
# 遍历
for i in s_a:
	print i

# 切片[start:end:step] >= start * < end
li = list(range(10)) #[0,1,2,3,4,5,6,7,8,9]
print(li[2:5]) # [3,4,5]
print(li[:4]) # [0,1,2,3]
print(li[0:10:3])#[0,3,6,9]
print(li[5:-2])#[5,6,7]
print(li[9:0:-1])#[9,8,7,6,5,4,3,2,1]
print(li[9::-1])#[9,8,7,6,5,4,3,2,1,0]

# 列表推导
#生成10个偶数
li = [i*2 for i in range(10)]

#二维数组浅拷贝
li_2d = [[0]*3]*3
print(li_2d)
li_2d[0][0] = 100
print(li_2d)#这样写会每个元素的首元素变成100，因为*3这样写是浅拷贝，每个引用的是同一个空间

#二维数组深拷贝
li_2d = [[0]*3 for i in range(3)]
li_2d[0][0] = 100

s = {x for x in range(10) if x%2 == 0}
print(s) #s=set

d = {x:x%2 == 0 for x in range(10)}
print(d)#d=dict


# 生成器
square_generator = (x*x for x in range(50000))
print(next(square_generator))
for i in range(10):
	print(next(square_generator))

# 迭代器
from collections import Iterable
from collections import Iterator

print(isinstance([1,2,3],Iterable)) #true
print(isinstance([1,2,3],Iterator)) #false
print(isinstance({},Iterable))#true
#

```

##**********************练习***********************
```python
#任意给定一个值，在一个数组中找到两个数，相加=给定值，返回这两个数的索引，如果没有，返回-1

def find_two_sums(ls, target):
    for i in range(len(ls) - 1):
        for j in range(i+1, len(ls)):
            if ls[i] + ls[j] == target:
                return i, j

    return -1, -1


print(find_two_sums([1, 3, 2, 6, 18, 4, 2], 3))

#螺旋矩阵，给定一个m*n要素的矩阵，按照螺旋顺序，返回该矩阵的所有要素

#方法一，我自己写的一个笨方法，只用到上面学的内容，应该是符合所有常识人理解
matrix2 = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]

def myspiralmatrix(matrix):
	if len(matrix) < 1:
		return []
	#宽
    m = len(matrix[0])
    #长
    n = len(matrix)
    matrix3 = matrix
    ls = []

    #以横着读一批+竖着第一批作为一批，最多只有可能走m/n遍就能遍历完
    if m >= n:
        t = n
    else:
        t = m

    for tt in range(1, t + 1):

    	# 如果是奇数次遍历，那么就是顺时针读
        if tt % 2 != 0:
        	#横：读出matrix第一个元素的所有值
            ls.extend(matrix3[0][:m])
            #竖：除了matrix第一个元素之外，遍历剩下n-1个元素，只读出来第m-1个
            for k in range(1, n):
                ls.append(matrix3[k][m - 1])

            #重置数组，将下回要遍历的数组宽，长都-1，重新生成新的数组
            m = m - 1
            n = n - 1
            tmp = matrix3
            matrix3 = []
            for em in range(1, n + 1):
                matrix3.append(tmp[em][:m])

        # 如果是偶数次遍历，那么就是逆时针读        
        else:
            # 逆序打印这个时候matrix的最后一行
            ls.extend(matrix3[n - 1][m::-1])
            # 逆序竖着打印除了最后一行元素之后的所有元素的第一个元素
            for i in range(n - 1, 0, -1):
                ls.append(matrix3[i - 1][0])
            #重置数组，将下回要遍历的数组宽，长都-1，重新生成数组
            m = m - 1
            n = n - 1
            tmp = matrix3
            matrix3 = []
            for em in range(0, n):
                matrix3.append(tmp[em][1:])
    return ls


print(mySpiralOrder(matrix2))

#方法二，LeetCode上面某个大神的写法：
# 这里第一个matrix and是为了保证当所有元素都pop掉后，会返回一个空matrix,不会再做后面的pop和递归操作
# matrix.pop()的操作是直接改在matrix上的，所以后面的递归是基于新的matrix上面
# 后面的递归spiralOrder([*zip(*matrix)][::-1])生成的是一个剔除原先第一行元素后逆序的matrix

def spiralOrder(matrix):
    return matrix and [*matrix.pop(0)] + spiralOrder([*zip(*matrix)][::-1])



#用栈实现队列：支持push(element),pop()和top()方法。pop和top都应该返回第一个元素的值


#矩阵转换，给定矩阵A，令矩阵B里每个元素B[i][j]的值等于A[0][0]到A[i][j]子矩阵元素的和
# 除了第一行和第一列，其余B矩阵里面所有的元素都可以表示为
# B[i][j] = B[i][j-1] + B[i-1][j] - B[i-1][j-1] + A[i][j]

def matrixTransform(A):
    B = A
    for i in range(1,len(A[0])):
        B[0][i] += B[0][i-1]
    for i in range(1,len(A),1):
        B[i][0] += B[i-1][0]

    for i in range(1,len(A),1):
        for j in range(1, len(A[0]), 1):
            B[i][j] += B[i-1][j] + B[i][j-1] - B[i-1][j-1]
    return B


```

## 容器补充知识点
1，`*list`的含义， `*` operator unpacks an argument list. It allows you to call a function with the list items as individual arguments.
	For instance, if `sys.argv` is ["./foo", "bar", "quux"], `main(*sys.argv)` = `main("./foo","bar","quux")`
2，`zip` takes `n` number of iterables and returns list of tuples. `ith` element of the tuple is created using the `ith` element from each of the iterables.
```python
list_a = [1, 2, 3]
list_b = [4, 5, 6]

zipped = zip(a, b) # Output: Zip Object. <zip at 0x4c10a30>

len(zipped) # TypeError: object of type 'zip' has no len()

zipped[0] # TypeError: 'zip' object is not subscriptable

list_c = list(zipped) #Output: [(1, 4), (2, 5), (3, 6)]

list_d = list(zipped) # Output []... Output is empty list becuase by the above statement zip got exhausted.

```

```python
matrix2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]
print(*matrix2) # [1, 2, 3, 4] [5, 6, 7, 8] [9, 10, 11, 12] 这里不是一个list，是三个list对象
print([*zip(matrix2)]) #[([1, 2, 3, 4],), ([5, 6, 7, 8],), ([9, 10, 11, 12],)]
print([*zip(list(matrix2))]) #[([1, 2, 3, 4],), ([5, 6, 7, 8],), ([9, 10, 11, 12],)] 与上面相同，因为list(matrix2)还是只有一个对象
print([zip(*matrix2)]) # [<zip object at 0x00935350>]
print([*zip(*matrix2)]) #[(1, 5, 9), (2, 6, 10), (3, 7, 11), (4, 8, 12)]
```

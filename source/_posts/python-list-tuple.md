---
title: Python List and Tuple, Dict and Set
date: 2018-03-15 11:20:11
tags: [python, concept]
---

**Python 3**

**list与tuple都是有序列表**

### LIST

```python
p = ['asp', 'php']
 
s = ['python', 'java', p, 'angular']
```

如果想要拿到php，可以写成`s[2][1]`,因此s可以看作为二维数组

### TUPLE
**tuple一旦初始化就不能修改，这里的不能修改指的是tuple中的每个元素的指向不变**
```python
classmates=('Jane', 'Anna', 'Ed')
```
现在这个classmates就无法更改，没有append(),insert()可以调用

但是有时候却能看见给tuple添加元素的操作：
```python
def two(**s):
    print('s is ', s)
    t = ()
    for i in s.values():
        t += (i,) #这里tuple竟然可以添加元素
    print(t)
 
dic = dict(
    d1=1,
    d2=2,
    d3=3
)
 
if __name__ == '__main__':
    two(**dic) #输出为tuple(1, 2, 3)
```
<span style="color: red">**当执行上面的操作的时，其实stucture is changed. 即你每新增一个新的，其实是一个新的Object.**</span>
比如：
```python
>>> tup = (1, 2, 3)
>>> id(tup)
140153476307856
>>> tup += (4, 5)
>>> id(tup)
140153479825840
```
而如果是list的话：
```python
>>> lst = [1, 2, 3]
>>> id(lst)
140153476247704
>>> lst += [4, 5]
>>> id(lst)
140153476247704
```

[Ref link](https://drillearningss.wordpress.com/2018/01/04/python-list-and-tuple/)

如果想要定义一个只有一个参数的tuple,**不能写成**
```python
>>> t = (1)
 
>>> t
```
**因为这个时候t是数字1，（）这个时候当作数学括号来解析**
需要写成
```python
>>> t = (1, )
 
>>> t
 
(1, )
```

### DICT

使用键值对存储, 且dict的**key是不可变对象**

```python
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95
```

为避免key不存在报错：

```python
>>> 'Thomas' in d
False

>>> d.get('Thomas') //返回None
>>> d.get('Thomas', -1)

```

<span style="color: red">注意，dict的添加就是直接赋值就好了，例如
`d['newkey']='newvalue'`</span>

### SET

Set也是一组Key的集合，但不存储value，且Key也不能重复。

```python
>>> s = set([1,2,3])
>>> s
{1,2,3}
```

**注意传入的参数`[1,2,3]`是一个list，而显示的`{1,2,3}`只是告诉你这个set内部有1，2，3这3个元素，显示的顺序也不表示set是有序的**

重复元素再set中会自动被过滤掉

```python
>>> s = set([1,1,2,2,3,3,])
>>> s
{1,2,3}
>>> s.add(4)
>>> s
{1,2,3,4}
>>> s.remove(4)
>>> s
{1,2,3}
```

**SET可以看成无序且无重复元素的集合，因此两个set可以做数学意义上的交集、并集等操作**

```python
>>> s1 = set([1,2,3])
>>> s2 = set([2,3,4])
>>> s1 & s2
{2,3}
>>> s1 | s2
{1,2,3,4}
```
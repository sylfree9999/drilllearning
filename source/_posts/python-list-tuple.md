---
title: Python List and Tuple
date: 2018-03-15 11:20:11
tags: [python, concept]
---

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
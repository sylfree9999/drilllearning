---
title: python slice iterator generator
date: 2018-04-12 16:21:44
tags: [python, concept]
---

## Slice切片

取list/tuple/字符串中的部分元素即切片

#### list

```python
>>> L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
>>> L[0:3] //从索引0的位置开始取，直到索引3，但是不包含索引3，也可以写成L[:3]
['Michael', 'Sarah', 'Tracy']
>>> L[1:3]
['Sarah', 'Tracy']
>>> L[-2:] //取倒数两个
['Bob', 'Jack']
>>> L[-2:-1]
['Bob']
```

#### tuple

```python
>>> (0, 1, 2, 3, 4, 5)[:3]
(0, 1, 2)
```

#### string

```python
>>> 'ABCDEFG'[:3]
'ABC'
>>> 'ABCDEFG'[::2]
'ACEG'
```


## 迭代

python中`for`循环可以作用在所有可以迭代的对象上面，与有没有下标无关

```python
>>> d = {'a': 1, 'b': 2, 'c': 3}
>>> for key in d:
...     print(key)
...
a
c
b

>>> for value in d.values() //默认情况下dict迭代是的key, 可以用value来迭代
>>> for k, v in d.items()
```

如何判断是否是可迭代的对象：

```python
>>> from collections import Iterable
>>> isinstance('abc', Iterable) # str是否可迭代
True
```

如果在`for`循环里面同时引用两个变量：

```python
>>> for x, y in [(1, 1), (2, 4), (3, 9)]:
...     print(x, y)
...
1 1
2 4
3 9
```

## List Comprehensions 列表生成式

```python
>>> [x * x for x in range(1, 11) if x % 2 == 0]
[4, 16, 36, 64, 100]
```

也可以使用两层循环

```python
>>> [m + n for m in 'ABC' for n in 'XYZ']
['AX', 'AY', 'AZ', 'BX', 'BY', 'BZ', 'CX', 'CY', 'CZ']
```

## Generator 生成器

不是一次性生成所有的list,而是一边循环一边计算，从而节省大量的空间

*	生成器就是把列表生成式从[]to()

```python
>>> L = [x * x for x in range(10)]
>>> L
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
>>> g = (x * x for x in range(10))
>>> g
<generator object <genexpr> at 0x1022ef630>
>>> next(g) //不常用
0
>>> g = (x * x for x in range(10)) 
>>> for n in g: //一般是用这样的形式来拿取生成器里面的值
...     print(n)
... 
0
1
4
9
16
25
36
49
64
81
```

*	也可以是用`yield`来生成

```python
def fib(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b //如果是print b则不是生成器了
        a, b = b, a + b
        n = n + 1
    return 'done'
```

```python
>>> for n in fib(6):
...     print(n)
...
1
1
2
3
5
8

```

## Iterator 迭代器

`for` 除了可以作用于集合类型如： `list	tuple	dict	set	str`
还可作用于`generator`

这些可以直接作用于`for`循环的对象称为可迭代对象 `Iterable`

```python
>>> from collections import Iterable
>>> isinstance([], Iterable)
True
```
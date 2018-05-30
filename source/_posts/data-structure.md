---
title: 数据结构简概
date: 2018-05-28 10:54:55
tags: [concept]
---

学习萧大神笔记：

## 时间复杂度

*	O(1)
	常数复杂度，例如取数组第1000000个元素
	**字典和集合的存取都是O(1)**
	**数组的存取是O(1)**

	O(1)与O(n)的区别：
	O(1)的时间是确定的，O(n)是随着时间增大而增大
	O(1)是随着数据规模的增长而增长

*	O(lgN)
	对数复杂度
	例如一个**有序数组**，二分法查找

*	O(n)
	线性复杂度
	例如有一个数组，以遍历方式在其中查找元素

*	O(nlgN)
	例如求两个数组的交集，其中A是有序数组，B不是有序数组
	A数组每一个元素都要在B数组中进行查找
	因为每次查找用二分法的复杂度是lgN，那么n个数据就是nLgN

*	O(n^2)
	平方复杂度
	求两个无序数组的交集

## 常用数据结构
*	数组
	连续的一块内存
	存取元素的时间是O(1),因为是连续的内存，只要计算出内存地址就可以迅速拿到数据，这里的存取是指替换掉原来的元素
	插入、删除是O(n)，因为插入之后的元素都要往后挪

*	链表
	手拉手的盒子，一个盒子只能访问左右手的盒子
	以下标方式读取元素的时间是O(n)，因为要一个个搜过去
	插入、删除是O(1)，只要更改链表的指向就可
	栈和队列是链表的改良
	队列 先进先出
	栈	先进后出

*	字典(哈希表 对象 关联数组 Map 都是字典)
	想要像数组一样可以拿取数据都是O(1),但是数组都是用数字来取数据，想要也能用字符串来取数据
	把字符串转为数字作为下标存储在数组中
	字符串转化为数字的算法是O(1)
	所有字典的存取操作也都是O(1)
	除非对数据有顺序要求，否则字典永远都是最佳选择
	字符串转化为数字的算法：
		1. 确定数据规模，这样可以确定容器数组的大小 =  Size
		2. 把字符当作N进制数字得到结果：
			'gua' = g * 1+u * 10+1 * 100 = n
			n % Size作为字符串在数组中的下标
			通常Size会选一个素数，素数也叫做质数，指在大于1的整数中只能被1和它本身整除的数，比如2、3、5、7、11、43、109
		3. 如果下标冲突（即碰撞）的时候，有标准解决碰撞的方法，比方说用HashTable
			它的原理是我在数组中存的不是数据，而是一个链表
			当Hash值相同的时候，就放在这个链表里面

*	搜索树
	用于作搜索用，比方说二叉搜索树，左边的节点总是小于中间的节点，右边的节点总是大于中间的节点
	这样搜索最小的 ，只要搜索最左边那一条线就可以了
	时间复杂度跟二叉搜索一样，都取决于你这棵树的高度O(lgN)

	平衡树的意思就是当树的高度差超过1的时候，会重新定义根节点，把原来的树进行旋转

*	图

*	Python List
	存取是O(1)
	插入删除也是O(1)

	当它最初申请的数组空间用完了以后，它会申请一个更大的数组空间，然后把原来的数组空间copy到新申请的大数组空间中

	所以有时候看会有时间断层

	Python list有两个部件：
		数组		存储数据在链表中的地址
		链表		实际存储数据


```python
# HashTable Data Structure
class HashTable(object):
    def __init__(self):
        self.table_size = 11
        self.table = [0]*self.table_size

    # 这个魔法方法来实现in/not in语法
    def __contains__(self, item):
        return self.has_key(item)

    def has_key(self, key):
        index = self._index(key)
        v = self.table[index]

        if isinstance(v, list):
            for kv in v:
                if kv[0] == key:
                    return True
        return False

    def _index(self, key):
        return self._hash(key) % self.table_size

    def _hash(self, s):
        n = 0
        f = 1
        for i in s:
            n += ord(i) * f
            f *= 10
        return n

    def add(self, key, value):
        index = self._index(key)
        self._insert_at_index(index, key, value)

    def _insert_at_index(self, index, key, value):
        v = self.table[index]
        data = [key, value]
        if isinstance(v, int):
            self.table[index] = [data]
        else:
            self.table[index].append(data)

    def get(self, key, default_value = None):
        index = self._index(key)
        v = self.table[index]
        if isinstance(v, list):
            for kv in v:
                if kv[0] == key:
                    return kv[1]
        return default_value


def test():
    import uuid
    names = [
        'ss',
        'drill',
        'name',
        'python',
        'web',
        'Banana',
        'Apple',
        'Computer',
        'Android',
        'Mobile'
    ]
    ht = HashTable()
    for key in names:
        value = uuid.uuid4()
        ht.add(key, value)
        print('add 元素', key, value)
    for key in names:
        v = ht.get(key)
        print('get 元素', key, v)


if __name__ == '__main__':
    test()
```

如果这个素数设置的够小，你就能看到有些item存的是一个list
{% asset_image 20180528160417.png %}
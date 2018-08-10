---
title: python-third-packages
date: 2018-08-09 11:30:32
tags: [python, concept]
---
## 数值计算numpy
1，numpy的ndarray是一个多维数组对象，该对象由两部分组成：
	1，实际的数据
	2，描述这些数据的元数据，比方说数据是如何排列的，结构是什么样
	3，很多时候我们只修改的是元数据，而不更改实际数据
2，numpy能够直接对数组和矩阵进行操作，不需要写python，所以会比较快
3，numpy基本索引和切片：
<!--more-->
```python
import numpy as np

# 数组乘法/减法，对应元素相乘/相减
arr = np.array([[1.0,2.0,3.0],[4.,5.,6.]])
print(arr * arr)
print(arr - arr)

# 标量操作作用在数组的每个元素上
arr = np.array([[1.0,2.0,3.0],[4.,5.,6.]])
print(1/arr)
print(arr**0.5) #开根号

# 通过索引访问二维数组某一行或某个元素
arr = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
print(arr[2])#打印出第三个元素
print(arr[0][2])#打印出第一个元素中的第三个元素
print(arr[0, 2]) # 普通Python数组不能用。

# 对更高维数组的访问和操作
arr = np.array([[[1, 2, 3], [4, 5, 6]], [[7, 8, 9], [10, 11, 12]]])
print (arr[0])  # 结果是个2维数组
print (arr[1, 0]) # 结果是个2维数组
old_values = arr[0].copy()  # 复制arr[0]的值
arr[0] = 42 # 把arr[0]所有的元素都设置为同一个值
print (arr)
arr[0] = old_values # 把原来的数组写回去
print (arr)
```
4，numpy boolean索引
```python
import numpy as np
import numpy.random as np_random

print ('使用布尔数组作为索引')
name_arr = np.array(['Bob', 'Joe', 'Will', 'Bob', 'Will', 'Joe', 'Joe'])
rnd_arr = np_random.randn(7, 4) # 随机7*4数组
print (rnd_arr)
print (name_arr == 'Bob') # 返回布尔数组，元素等于'Bob'为True，否则False。
print (rnd_arr[name_arr == 'Bob'])# 利用布尔数组选择行
print (rnd_arr[name_arr == 'Bob', :2]) # 增加限制打印列的范围
print (rnd_arr[-(name_arr == 'Bob')])# 对布尔数组的内容取反
mask_arr = (name_arr == 'Bob') | (name_arr == 'Will') # 逻辑运算混合结果
print (rnd_arr[mask_arr])
rnd_arr[name_arr != 'Joe'] = 7  # 先布尔数组选择行，然后把每行的元素设置为7。
print (rnd_arr)
```
5，numpy的花式索引
```python
#比方说我想要索引在第5，第3，第1位的元素
a = [1,2,3,4,5]
b = a[[5,3,1]] #即可

import numpy as np

print ('Fancy Indexing: 使用整数数组作为索引')
arr = np.empty((8, 4))
for i in range(8):
    arr[i] = i
print (arr)
print (arr[[4, 3, 0, 6]]) # 打印arr[4]、arr[3]、arr[0]和arr[6]。
print (arr[[-3, -5, -7]]) # 打印arr[3]、arr[5]和arr[-7]行
arr = np.arange(32).reshape((8, 4))  # 通过reshape变换成二维数组
print (arr[[1, 5, 7, 2], [0, 3, 1, 2]]) # 打印arr[1, 0]、arr[5, 3]，arr[7, 1]和arr[2, 2]
print (arr[[1, 5, 7, 2]][:, [0, 3, 1, 2]])  # 1572行的0312列
print (arr[np.ix_([1, 5, 7, 2], [0, 3, 1, 2])]) # 可读性更好的写法
```

6，numpy的ndarray数组转置和轴对换
```python
import numpy as np

print("矩阵的乘积，(axb)*(cxd)=(a'xd')，要求b=c")
arr1 = [[1,2,3],[4,5,6]]
arr2 = [[4,5],[6,7],[8,9]]
# print(np.dot(arr1,arr2))

print("高维矩阵轴变换")
arr3 = np.arange(16).reshape((2,2,4))
print(arr3)
# 决定总共有多少列取决于原来的A[x][y][z]的z，最大层有几个元素取决于原来的x，所以如果轴变换为（2，1，0）那么最终由两列，四个最大层元素。把结构画好了以后再转换就会很快
# print(np.ndim(arr3))
print(arr3.transpose((2,1,0)))
```

7，numpy where条件过滤
```python
import numpy as np
import numpy.random as np_random

print("where")
cond = np.array([True,False,True,True,False])
cond_1 = np.array([True,False,True,True,False])
cond_2 = np.array([False,True,False,True,False])
result = []
#传统代码如下
for i in range(len(cond)):
    if cond_1[i] and cond_2[i]:
        result.append(0)
    elif cond_1[i]:
        result.append(1)
    elif cond_2[i]:
        result.append(2)
    else:
        result.append(3)
print(result)
# np版本
result = np.where(cond_1 & cond_2, 0, np.where(cond_1, 1, np.where(cond_2, 2, 3)))
print(result)
```
8，numpy 求和求平均
```python
import numpy as np
print("求和，求平均")
arr = np.random.randn(5,4)
print(arr)
print(arr.mean())#所有元素求平均
print(arr.mean(axis = 1)) #对每一行的元素求平局
print(arr.sum())#所有元素求和
print(arr.sum(0))#对每一列的元素求和
```

9，numpy布尔型数组过滤
```python
import numpy as np
print("对正数求和")
arr = np.random.randn(100)
print((arr>0).sum())

print("对数组逻辑操作")
bools = np.array([False,False,True,False])
print(bools.any())#有一个为True则返回True
print(bools.all())#有一个为False则返回False
```

10，利用数组进行数据处理和排序
```python
print ('二维数组排序')
arr = np_random.randn(5, 3)
print (arr)
arr.sort(1) # 对每一行元素做排序
print (arr)

print ('找位置在5%的数字')
large_arr = np_random.randn(1000)
large_arr.sort()
print (large_arr[int(0.05 * len(large_arr))])
```


11，利用数组来去重以及其它集合运算
{%asset_img numpy_unique.png %}

> 例子：距离矩阵的计算
> 给定m\*n阶矩阵X，满足X = [x<sub>1</sub>,x<sub>2</sub>,...,x<sub> n</sub>],这里第i列向量是m维向量。
> 求n * n矩阵，使得D<sub>ij</sub>=||x<sub>i</sub> - x<sub>> j</sub>||<sup>2</sup>  
> 

这个例子的意思是有x<sub>i</sub>,x<sub>j</sub>
D<sub>ij</sub> = (x<sub>[0][i]</sub> - x<sub>[0][j]</sub>)<sup>2</sup> + (x<sub>[1][i]</sub> - x<sub>[1][j]</sub>)<sup>2</sup> + ... + (x<sub>[m][i]</sub> - x<sub>[m][j]</sub>)<sup>2</sup>


```python
import numpy as np
import numpy.linalg as la
import time

X = np.array([range(0,500),range(500,1000)])
# print(X)
m,n = X.shape

t = time.time()
D = np.zeros([n,n])
for i in range(n):
	for j in range(i+1, n):
		D[i,j] = la.norm(X[:, i] - X[:, j]) ** 2
		D[j,i] = D[i,j]
print(time.time() - t) 

t = time.time()
D = np.zeros([n,n])
#d[k] = X[k][i] -X[k][j]
#d[i,j] = d[0]<sup>2</sup>
for i in range(n):
	for j in range(i+1, n):
		d = X[:, i] - X[:, j]
		D[i,j] = np.dot(d,d)
		D[j,i] = D[i,j]
print(time.time()-t)

t = time.time()
G = np.dot(X.T, X)
H = np.tile(np.diag(G), (n, 1))
D = H + H.T - G * 2
print (time.time() - t)
```

## 数据处理分析pandas
## 可视化matplotlib/seaborn
```python
import numpy as np; np.random.seed(0)
import seaborn as sns; sns.set()
uniform_data = np.random.rand(10, 12)
ax = sns.heatmap(uniform_data)
```
{%asset_img heatmap.png %}

## 机器学习Sklearn/keras
{%asset_img scklearn.png %}
python监督学习典型的三部曲
```python
train_x, train_y, test_x, text_y = getData()

model = somemodel()#选择一种模型
model.fit(train_x, train_y)
predictions = model.predict(test_x)

score = score_function(test_y, predictions)
```

## 交互pygame
## 网络Selenium
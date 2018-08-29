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
#d[i,j] = d[0]^2 + d[1]^2
for i in range(n):
	for j in range(i+1, n):
		#把第i列和第j列相减
		d = X[:, i] - X[:, j]
		#然后做矩阵乘法的运算
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

### 数据结构Series
1，Series是一种类似于一维数组的对象，它由一组数据（各种NumPy数据类型）以及一组与之相关的数据标签（即索引）组成
2，Series的字符串表现形式为：索引在左边，值在右边
3，默认是数字索引
```python
from pandas import Series

print("用数组生成series")
obj = Series([5,7,-1,3])
print(obj)

print("指定Series的index")
obj2 = Series([5,7,-1,3], index = ['a','b','c','d'])
print(obj2)

print("使用字典生成Series")
dData = {'ohio':3999,"texas":2000,"oregon":123123}
obj3 = Series(dData)
print(obj3)
```
### 数据结构DataFrame
1，DataFrame是一个表格型数据结构，它含有一组有序的列，每列可以试不同的值的类型（数值、字符串、布尔值等）
2，DataFrame既有行索引，也有列索引，可以被看做由Series组成的字典（共用同一个索引）。
```python
import numpy as np
from pandas import Series, DataFrame

print('用字典生成DataFrame，key为列的名字。')
data = {'state':['Ohio', 'Ohio', 'Ohio', 'Nevada', 'Nevada'],
        'year':[2000, 2001, 2002, 2001, 2002],
        'pop':[1.5, 1.7, 3.6, 2.4, 2.9]}
print(DataFrame(data))
print(DataFrame(data, columns = ['year', 'state', 'pop'])) # 指定列顺序

print '指定索引，在列中指定不存在的列，默认数据用NaN。'
frame2 = DataFrame(data,
                    columns = ['year', 'state', 'pop', 'debt'],
                    index = ['one', 'two', 'three', 'four', 'five'])
print frame2
print frame2['state']
print frame2.year
print frame2.ix['three']
frame2['debt'] = 16.5 # 修改一整列
print frame2
frame2.debt = np.arange(5)  # 用numpy数组修改元素
print frame2
print

print '赋值给新列'
frame2['eastern'] = (frame2.state == 'Ohio')  # 如果state等于Ohio为True
print frame2
print frame2.columns
print

```
3，数据的清理用drop
```python
import numpy as np
from pandas import Series, DataFrame

print 'Series根据索引删除元素'
obj = Series(np.arange(5.), index = ['a', 'b', 'c', 'd', 'e'])
new_obj = obj.drop('c')
print new_obj
print obj.drop(['d', 'c'])
print

print 'DataFrame删除元素，可指定索引或列。'
data = DataFrame(np.arange(16).reshape((4, 4)),
                  index = ['Ohio', 'Colorado', 'Utah', 'New York'],
                  columns = ['one', 'two', 'three', 'four'])
print data
print data.drop(['Colorado', 'Ohio'])
print data.drop('two', axis = 1) #axis=1代表处理的是列
print data.drop(['two', 'four'], axis = 1) #原始数据并没有被删除

```

### Pandas Data Selection
{%asset_img pandas-selections.png %}
准备数据
```python
import pandas as pd
import random

data = pd.read_csv('https://s3-eu-west-1.amazonaws.com/shanebucket/downloads/uk-500.csv')
data['id'] = [random.randint(0,1000) for x in range(data.shape[0])]
data.head(5)
```

1, By row numbers(.iloc)
"iloc" in pandas is used to **select rows and columns by number**
`data.iloc[<row selection>,<column selection>]`

注意是开区间，你选择[1:5]返回的是1,2,3,4
```python
# Single selections using iloc and DataFrame
# Rows:
data.iloc[0] # first row of data frame (Aleshia Tomkiewicz) - Note a Series data type output.
data.iloc[1] # second row of data frame (Evan Zigomalas)
data.iloc[-1] # last row of data frame (Mi Richan)
# Columns:
data.iloc[:,0] # first column of data frame (first_name)
data.iloc[:,1] # second column of data frame (last_name)
data.iloc[:,-1] # last column of data frame (id)

# Multiple row and column selections using iloc and DataFrame
data.iloc[0:5] # first five rows of dataframe
data.iloc[:, 0:2] # first two columns of data frame with all rows
data.iloc[[0,3,6,24], [0,5,6]] # 1st, 4th, 7th, 25th row + 1st 6th 7th columns.
data.iloc[0:5, 5:8] # first 5 rows and 5th, 6th, 7th columns of data frame (county -> phone1).
```

2, By label or by a conditional statement(.loc)
	a) Selecting rows by label/index
	b) Selecting rows with a boolean/conditional lookup

注意用loc就不是开区间，而是闭区间了，Veness行和email列都会被选出来
```python
data.set_index("last_name", inplace=True)
data.head()

data.loc['Andrade':'Veness', 'city':'email']

#Conditional lookup
data.loc[data['first_name'] == 'Erasmo',['company_name','email']]
# Select rows where the email column ends with 'hotmail.com', include all columns
data.loc[data['email'].str.endswith("hotmail.com")]   

# Select rows with last_name equal to some values, all columns
data.loc[data['first_name'].isin(['France', 'Tyisha', 'Eric'])] 
```
在这里注意了
如果
`data.loc[data['first_name'] == 'Erasmo','email']`
即以<span style="color: red">.loc[<selection>,String]</span>形式，返回的是一个Series

如果
`data.loc[data['first_name'] == 'Erasmo',['email']`
即以<span style="color: red">.loc[<selection>,List]</span>形式，返回的是一个DataFrame

{%asset_img loc1.png %}





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
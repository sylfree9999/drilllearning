---
title: R Concepts
date: 2018-04-18 16:09:35
tags: [R, concept]
---

## apply函数

通过apply函数，可以实现对数据的循环、分组、过滤、类型控制等操作。

apply函数可以替代`for`循环函数。它可以对矩阵、数据框、数组（二维，多维）按行或列进行循环计算，对子元素进行迭代，并把子元素以参数传递的形式给自定义的FUN函数中，并返回计算结果。

`apply(X, MARGIN, FUN, ...)`

* X: 数组、矩阵、数据框
* MARGIN: 按行计算=1， 按列计算=2
* FUN: 自定义调用函数
* ...: 更多参数

例： 对一个矩阵的每一行求和

```R
> x<-matrix(1:12, ncol=3)
> x
     [,1] [,2] [,3]
[1,]    1    5    9
[2,]    2    6   10
[3,]    3    7   11
[4,]    4    8   12
> apply(x, 1, sum)
[1] 15 18 21 24
```

例： 按行循环，让数据框的x1列+1,并计算x1,x2列的均值

```R
> x <- cbind(x1=3, x2=c(4:1,2:5)); x
     x1 x2
[1,]  3  4
[2,]  3  3
[3,]  3  2
[4,]  3  1
[5,]  3  2
[6,]  3  3
[7,]  3  4
[8,]  3  5

# 自定义函数myFUN, 第一个参数x为数据，第二、第三个参数为自定义参数

> myFun <- function(x,c1,c2){
	c(sum(x[c1],1), mean(x[c2]))
}

> apply(x,1,myFUN,c1='x1',c2=('x1','x2'))
    [,1] [,2] [,3] [,4] [,5] [,6] [,7] [,8]
[1,]  4.0    4  4.0    4  4.0    4  4.0    4
[2,]  3.5    3  2.5    2  2.5    3  3.5    4
```

## [,[[,$ accessors 

[Ref:https://www.r-bloggers.com/r-accessors-explained/]

* Subset with [
	取Object子集用[]. 取出来的子集与原object类型相同

* Extract one item with [[
	The double square brackets are used to extract one element from potentially many.
	For vectors yield vectors with a single value;
	data frames give a column vector;
	for list, one element

	```R
	letters[[3]]
	iris[["Petal.Length"]]
	```

	Remember:
	* You can return only one item.
	* The result is not (necessarily) the same type of the object as the container
	* The dimension will be the dimension of the one item which is not

* Interact with $
	$ is a special case of [[]] in which you access a single item by actual name.

	The following are equal

	```R
	iris$Petal.Length
	iris[["Petal.Length"]]
	```
	
	Remember:
	*	You cannot use integer indices
	* 	The mane will not be interpolated.
	*	Returns only one item.
	*	If the name contains special characters, the name must be enclosed in **""**

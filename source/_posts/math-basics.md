---
title: math-basics
date: 2018-09-12 15:55:55
tags: [Math, Concept, MachineLearning]
---

与其恐惧，不如直面它吧！

## 对数函数
基本公式为：
$\log_a{MN} = \log_aM + \log_aN$
$\log_a{\frac{M}{N}} = \log_aM - \log_aN$
$\log_a{M^n} = n\log_aM$
$\log_{a^n}M = \frac{1}{n}\log_aM$
换底公式$\log_ba = \frac{\log_ca}{\log_cb}$
倒数公式$\frac{1}{\log_ab} = \log_ba$

## 三角函数
[Ref:https://zhuanlan.zhihu.com/p/20102140]
[Ref:https://www.youtube.com/watch?v=diMjCkwL9Xo&list=PLF38FCD363F7184B0&index=7]

### 基础定义
设角$\alpha$的的终边与单位圆交于点P(x,y),则有
$\sin\alpha =y, \cos\alpha = x$
$\tan\alpha = \frac{y}{x}, \cot\alpha = \frac{x}{y}$
$\sec\alpha = \frac{1}{x},\csc\alpha = \frac{1}{y}$
**sec pronounces secant**
**csc pronounces cosecant**

<!--more-->

### 同角三角函数基本关系
可以由上面的式子直接推导：
$\tan\alpha\cot\alpha=1$
$\sin\alpha\csc\alpha=1$
$\cos\alpha\sec\alpha=1$
还可以得出：
$\frac{\sin\alpha}{\cos\alpha}=\tan\alpha=\frac{\sec\alpha}{\csc\alpha}$ $\frac{\cos\alpha}{\sin\alpha} = \frac{\csc\alpha}{\sec\alpha}$
同时结合勾股定理，还可以得到
$\sin^2\alpha + \cos^2\alpha =1$

可以结合下面的图进行定义
{%asset_img tri_6p.png%}
{%asset_img tri_6p_2.png%}

基本公式的记忆方法
根据一个单位圆就可以得出：
$1^2+\tan^2\alpha=\sec^2\alpha$
$1^2+\cot^2\alpha=\csc^2\alpha$

{%asset_img unit_circle_1.png %}
{%asset_img unit_circle_2.png %}

广义角的定义与传统第一象限的三角函数定义相同，只不过带上了各个象限的讯息，就是到底是在x轴上下，还是y轴左右，还是x,y是同号还是异号。广义角的定义可以推出后面的傅里叶变换

### 角度制，弧度制
弧度制也是描述角度的一种单位
弧度制的含义就是一个单位圆，我把半径为1的长度放到周长上面，这个时候对应的角叫做一个Rad。
那么如果我这个弧度角转一周，产生出来的角度是多少？也就是说可以用多少长度为1的线段来描述这个圆周，其实就是
$$2\pi\text{r} = 360°$$
也就是$2\pi = 360°$
这样的话，对于弧长s/圆周长，就=这个时候的弧度角/一周的角，也就是：
$$\frac{s}{2\pi\text{r}} = \frac{\theta}{2\pi}$$
$$s=r\theta$$

{%asset_img radius_1.png %}

那么同理，对于面积：
$$\frac{A}{\pi\text{r}^2} = \frac{\theta}{2\pi}$$
也就是$A=\frac{\theta\text{r}^2}{2}$,又因为$s=\theta\text{r}$,所以：
$$A = \frac{1}{2}sr$$
有一点点像是一个三角形的面积，以s为底，r为高

### 偶函数与奇函数
偶函数 f(x) = f(-x)，对y轴在做对称，cos(x)是偶函数, tan(x)也是偶函数 tan(x) = tan(-x)
奇函数 f(x) = -f(-x),对原点在做对称，sin(x)是奇函数，cot(x)也是奇函数 

### 三角函数的诱导公式

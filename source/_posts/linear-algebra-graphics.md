---
title: linear-algebra-graphics
date: 2018-09-03 17:46:55
mathjax: true
tags: [Maths, Concept, LinearAlgebra]
---

没想到我有生之年，还要再次学习一下线性代数。

凹！被数学支配的恐惧还涌在心头，依稀记得在大学的时候学的时候感觉都懂，过一个暑假全忘了（这种特殊技能同样包括各种电视剧，比方说什么射雕英雄传，鹿鼎记，还珠格格这种，看的时候那是比谁都清楚，看完就忘）

我也是佩服我自己的。
好了，废话不多说了，现在毕竟科技发达了，不如以往，只能靠老师教的方法学。现在各种网上的资源很是丰富啊。

在众多资源中，一个3Blue1Brown的大神还有meetmath做的系列脱颖而出，我决定引用他们的例子，用这种图形化的学习方式重温一下线性代数。

MeetMath:[Ref: https://mp.weixin.qq.com/s?__biz=MzAxNzg3MTE3Ng==&mid=2247485798&idx=1&sn=15a52a1e1fc3a2ba51353b66faa735db&scene=21#wechat_redirect]

3Blue1Brown: [Ref:https://www.bilibili.com/video/av6240005/?spm_id_from=333.788.videocard.2]

## 向量的加法

向量的加法这种，是唯一一个情况需要把一个向量移开原点的情况。
为什么要移开呢？因为可以理解为从 $\vec{v}$ ,<span style="color: red;">走到</span> $\vec{w}$ 就相当于$\vec{v}$+$\vec{w}$

{%asset_img vector_Add.png%}

## 线性变换

概念：必须具有两个性质，首先直线必须在变换后还是直线，且原点不能变
{%asset_img linear_function.png %}

如何用数值来描述线性变换？
变换后的向量都可以用基本的$\hat{i}$和$\hat{j}$来表示,只要告诉你变换后$\hat{i}$和$\hat{j}$的坐标，你就可以计算出$\begin{bmatrix}x\\\y\end{bmatrix}$

你就可以计算出$\begin{bmatrix}x\\\y\end{bmatrix}$ -> x$\begin{bmatrix} 1 \\\ -2\end{bmatrix}$ + y$\begin{bmatrix}3 \\\ 0\end{bmatrix}$ = $\begin{bmatrix}1x+3y \\\ -2x+0y \end{bmatrix}$

{%asset_img ihat.png%}

```shear```的意思是保持x轴不变，然后转y轴

## 矩阵相乘
对于矩阵$\begin{bmatrix}a & b\\\ c&d \end{bmatrix}$$\begin{bmatrix} e&f\\\ g&h \end{bmatrix}$,其实就是相当于先做了$\begin{bmatrix} e&f\\\ g&h \end{bmatrix}$矩阵变换，然后做了$\begin{bmatrix}a & b\\\ c&d \end{bmatrix}$矩阵变换，所以得出的结果就是：
{%asset_img matrix_multiplication.png %}

所以如果根据矩阵相乘图形变化来思考M$_1$M$_2$ 是否= M$_2$M$_1$就很容易理解，因为两次矩阵变换的结果是不同的

##行列式 Determinant 
How much the transformation strech/squish the areas?
How much are areas scaled?

Determinant is just how much your area scaled? from ASpace to X times ASpace, then A is the determinant of the matrix
{%asset_img determint_definition.png %}

行列式也可以是负数，负数的意思就是按照矩阵描述的变换方法变换，但结果这个平面翻转了，比方说原来$\hat{j}$在$\hat{i}$的左边，但是变换后$\hat{j}$在$\hat{i}$右边，这就造成了翻转

如果是3D的情况，则是volume被变了
行列式的计算公式：

det$(\begin{bmatrix}a & b\\\ c&d \end{bmatrix})$ = ad-bc
{%asset_img determint_definition.png %}

## 逆矩阵 Inverse Matrices 列空间Column Space，秩Rank与零空间 Null Space
对于$A\vec{x}=\vec{v}$,图形含义是对于向量$\vec{x}$，经过矩阵A的变换，与向量$\vec{v}$重合,也就是说A的行列式会变成0（也就是压缩成了一条线或者一个平面），还是strech/squish成之前一样的2/3维，也就是行列式不等于0

{%asset_img inverse_matrix.png %}

如果行列式不等于0：
逆矩阵的意思是逆过来再做一次A矩阵，所以先做一次A矩阵，再做一次A逆矩阵，就相当于什么也没有做
$A^{-1}A = \begin{bmatrix} 1&0 \\\ 0&1 \end{bmatrix}$
这个时候：
$A\vec{x} = \vec{v}$就可以写成
$A^{-1}A\vec{x} = A^{-1}\vec{v}$,也就是$\vec{x} = A^{-1}\vec{v}$
这个含义就是`You are playing the transformation in reverse and following v`

**<span style="color:red">如果行列式等于0,则没有逆矩阵的情况，因为不可能有一个逆操作，从一条线变成一个平面</span>**

## 方程组的解
$$
\begin{cases}
a_1x+b_1y+c_1z=d_1 \\\ 
a_2x+b_2y+c_2z=d_2 \\\ 
a_3x+b_3y+c_3z=d_3
\end{cases}
$$
上面用方程写成的矩阵向量相乘，也可以表示成
$\begin{pmatrix} a_1&b_1&c_1 \\\ a_2&b_2&c_2 \\\ a_3&b_3&c_3 \end{pmatrix}$$\begin{pmatrix} x \\\ y \\\ z \end{pmatrix} = \begin{pmatrix} d_1 \\\ d_2 \\\ d_3 \end{pmatrix}$

常系数矩阵A，未知量向量$\vec{x}$，两者的乘积得到列向量$\vec{v}$
所以求解Ax = v就意味着我们要找到一个向量x，使得它再变换后与v完全重合
如果有逆矩阵$\vec{x} = A^{-1}\vec{v}$来理解，也就是向量v经过矩阵A的逆变换到达了x

或者，对于方程组：

$$
\begin{cases}
x+y=2 \\\ 
2x+2y=1 \\\ 
\end{cases}
$$

从列视图可以看作向量$\begin{pmatrix} 2 \\\ 1 \end{pmatrix}$没有落在矩阵$A=\begin{pmatrix} 1&1 \\\ 2&2 \end{pmatrix}$所指向的空间内(其实就是基向量$\begin{pmatrix} 1&0 \\\ 0&1 \end{pmatrix}$做矩阵A的变化)，从下图的动画中可以看到经过矩阵变换后，空间最终被压缩成了一条直线，而变化全程向量$\vec{v}$都处在直线外，所以这个方程组无解

**<span style="color: red">这个方程组有解就代表矩阵A所代表的变换没有将空间进行扁平化的压缩。即$det(A) \neq 0$</span>**

width=100% height=600px frameborder="0" scrolling="no" src="http://mmbiz.qpic.cn/mmbiz_gif/WBqG5VGfdMEA8wxqLQrofiaN5OAAEiaMduI9WiaiaibPHWf4O5kHdGodlgp1WBEDvJLY1Iuze2yCyO13DCM8PghGfmw/0?wx_fmt=gif&tp=webp&wxfrom=5&wx_lazy=1"

### Rank矩阵的秩
When the output of transformation is a line, meaning it's one-dimensional, then we say the transformation has a rank of 1

If all the vectors land on some two-dimensional plane, we say the transformation has a rank of 2.

也就是说矩阵的秩代表着变换后，其空间的维数

### Column Space
This set of all possible outputs for your matrix, whether it's a line, a plane, 3-D space whatever, is called the "column space" of your matrix



### Full Rank满秩
When this rank is as high as it can be, meaning it equals the numner of columns, we call the matrix "full rank"

### Null Space/Kernal零空间，核
This set of vectors that lands on the origin is called the "null space" or the "kernal" of your matrix,一般表示成dim Ker(X),也就是零空间的维度

### 维数定理
如果A是m\*n 矩阵，维数定理就是：
$dim Ker(A) + rank(A) = n$

## 点积Dot Product与对偶性duality

### 点积Dot Product
[Ref:https://betterexplained.com/articles/vector-calculus-understanding-the-dot-product/]

Think of the dot product as **<span style="color:red">directional multiplication</span>**.
If a vector is "growth in a direction", there's a few operations we can do:
* Add vectors, Accumulate the growth contained in several vectors
* Multiply by a constant: Make an existing vector stronger
* Dot product: Applyt the directional growth of one vector to another. The result is how much stronger we've made the original.

所以当有两个不同方向的向量相乘，这代表什么意思呢？
可以理解为两个向量不同组成部分的相乘
由于$\vec{a}$可以由$a_x$和$a_y$来表示，$\vec{b}$也可以由$b_x$和$b_y$来表示，那么$\vec{a} \cdot \vec{b}$ = $a_x \cdot b_x$ + $a_y \cdot b_x$(=0) + $a_x \cdot b_y$(=0) + $a_y \cdot b_y$来表示

由于两个垂直的向量相乘=0，所以$\vec{a} \cdot \vec{b}$也就可以表示成：

$$a_x \cdot b_x + a_y \cdot b_y$$

{%asset_img dot_product_components.png%}

或者通过**Rotate**来理解点积
由于想要知道两个向量的growth,可以把其中一个向量投影到另一个向量（即与另一个向量相同部分），这样两个向量就是相同的方向，其点积也就是相同方向向量的点积。

所以$\vec{a}$在$\vec{b}$上面相同的部分就是$\vec{a}$在$\vec{b}$上面的投影，也就是$|a|\cos(\theta) \cdot |b|$

{%asset_img dot_product_rotation.png %}

点积的图形意义就是向量$\vec{w}$在向量$\vec{v}$上的投影长度 * 向量$\vec{v}$的长度，如果是反方向，则点积为负，如果是相同方向，点积为正，如果两个向量成直角，则点积为0.
{%asset_img dot_product_1.png %}

并且$(2\vec{v} \cdot \vec{w}) = 2(\vec{v} \cdot \vec{w})$

但是为什么点积的计算方式（就是对应变量相乘然后相加）会与Projection（投影）有关呢？
{%asset_img dot_product_2.png %}

点积的几何意义：
What it means to apply one of these transofrmations to a vector.
例如对于向量$\begin{bmatrix} 4 \\\ 3 \end{bmatrix}$,有一个线性变换，将$\hat{i}$和$\hat{j}$变换至1和-2，也就是说这个transform matrix就是$\begin{bmatrix} 1&-2 \end{bmatrix} $,要跟踪向量$\begin{bmatrix} 4 \\\ 3 \end{bmatrix}$变换后的去向，就将这个向量分解成为4\*$\hat{i}$ + 3\*$\hat{j}$，由于线性性质，所以在变换后，这个向量的位置就是4\*变换后的$\hat{i}$，也就是1,加上变换后的$\hat{j}$，也就是3(-2)，所以最终它变换成-2

{%asset_img dot_product_3.png %}

### Duality对偶性(我觉得我看了不下5遍...)

那么为什么点积坐标的相加与投影有关系呢？

在坐标中可以定义一个u轴穿越原点。我们的目标就是将坐标中的任意一个向量，变成u轴上面的一个数字。换句话说，我们要能找到一个1\*2的矩阵，能够描述这个变化。或者说，任意变量经过线性变换后，跑到了U轴上变成一个点，这个时候$\hat{i}$与$\hat{j}$也在U轴上面。那么$\hat{i}$和$\hat{j}$的值又是什么呢？

这个时候，我们可以加一条对称线来辅助计算。变换后的$\hat{i}$和$\hat{j}$就是这个矩阵的列值。根据对称性，变换后的$\hat{i}$其实就是$\vec{u}$在x轴上面的投影，也就是$u_x$,同理，变换后的$\hat{j}$其实就是$u_y$，也就是说这个变化矩阵transform matrix就是$\begin{bmatrix} u_x&u_y \end{bmatrix}$

{%asset_img dot_product_duality_1.webp %}

那么，对于空间中任意一个向量$\begin{bmatrix} x \\\ y \end{bmatrix}$,从自身一个二维向量映射到U轴上面的数值的这一变化，就可以描述成
$$\begin{bmatrix} u_x&u_y \end{bmatrix}\begin{bmatrix} x \\\ y \end{bmatrix} = u_x \cdot x + u_y \cdot y$$，也就是向量在U轴上面投影的长度

对于这种二维向量变成一维数值，其本身的定义就是
$$\begin{bmatrix} u_x \\\ u_y \end{bmatrix} \cdot \begin{bmatrix} x \\\ y \end{bmatrix} = u_x \cdot x + u_y \cdot y$$

这么一来，可以发现$\begin{bmatrix} u_x&u_y \end{bmatrix}\begin{bmatrix} x \\\ y \end{bmatrix} = u_x \cdot x + u_y \cdot y$与$\begin{bmatrix} u_x \\\ u_y \end{bmatrix} \cdot \begin{bmatrix} x \\\ y \end{bmatrix} = u_x \cdot x + u_y \cdot y$相等

也就是说，对于单位向量的点积可以解读为将向量投影到单位向量所在的直线上所得到的长度

至此，两个向量点积，就是将其中一个向量转化为线性变换
$$\begin{bmatrix} x_1 \\\ y_1 \end{bmatrix} \cdot \begin{bmatrix} x_2 \\\ y_2 \end{bmatrix}$$
$$\begin{bmatrix} x_1&y_1 \end{bmatrix}\begin{bmatrix} x_2 \\\ y_2 \end{bmatrix}$$


## Cross products叉积
[Ref:https://betterexplained.com/articles/cross-product/]

点积关注的是相同部分的interaction,而叉积关注的是不同部分，见下图： 而面积其实就是不同部分造成的一种结果。比方说两个相同方向的变量，是没有面积的，只有不同方向且不在一条线上的变量才有面积/体积的概念。在物理中比方说力矩(torque)，只有在不同方向上才有力矩的概念
{%asset_img cross-product-grid.png %}

叉积就是想定义一个rule,把所有不同的部分加起来
再看一遍上面的图，根据右手定理，x cross y能够定义一个正z，但是y cross x就是一个负z
y cross z is x, z cross z is -x;
所以记住这个Order XYZXYZ（这个就是一个正的顺序，只要按照这个顺序做，就是正的方向）。那么：
$$(1,2,3) \times (4,5,6) = ?$$

先看z，z由x,y来定义，根据XYZ这个顺序，只要是x cross y，则z为正，所以
$$z = 1 \times 5 - 2 \times 4 = -3$$
再看y，y由x,z来决定，根据XYZXYZ这个顺序。只要是z cross x，则y为正，所以
$$y = -1 \times 6 + 3 \times 4 = 6$$
最后看x，x由y,z决定，根据XYZ这个顺序，y cross z = positive x:
$$x = 2 \times 6 - 3 \times 5 = -3$$
所以最终结果为(-3,6,-3)

----------------------------------3Blue1Brown------------------------------------

叉积的定义就是两个向量组成的平行四边形的面积
$$\vec{v} \times \vec{w} =  \text{Area of parallelogram} $$ 
如果$\vec{v}$在$\vec{w}$的右边，叉积为正，如果在左边，叉积为负

由于变换后的向量构成面积就相当于行列式，所以
$$\vec{v} \times \vec{w} =  det(\begin{bmatrix} 3&2 \\\ 1&-1 \end{bmatrix})$$

更为准确的理解是在3D视图中，叉积是指以两个向量的面积为长度，右手定理大拇指为方向的一个向量，<span style="color: red">注意，这里$\vec{p}$是一个向量</span>
$$\vec{v} \times \vec{w} = \vec{p}$$
$\vec{p}$的长度就是$\vec{v}$和$\vec{w}$所形成的平行四边形的面积
同时$\vec{p}$的方向与这个平行四边形垂直
{%asset_img cross_product_3d.png %}

更为通用的公式：
{%asset_img cross_product_formula.png %}

这里就有一个疑问了，我为什么行列式第一列要放$\hat{i},\hat{j},\hat{k}$?
这里要用对偶性来解释

**对偶性**：无论何时你看到一个二维到一维的线性变换，你都能在平面中这个到这个向量。用这个线性变换得到的结果与用这个向量做点积是一样的结，比方说$\begin{bmatrix} 4&1 \end{bmatrix}$这个线性变换，线性变换后的结果与以$\begin{bmatrix} 4 \\\ 1 \end{bmatrix}$做点积结果相同.
{%asset_img cross_product_duality.png %}

数值上来解释的话，这是因为这类线性变换可以用一个只有一行的矩阵来描述，而这个矩阵的每一列给出了变换后基向量的位置。
{%asset_img cross_product_duality_base.png %}

这里的收获在于，每当你看到一个从空间到数轴的线性变换，你就能找到一个向量（成为这个线性变换的对偶向量），使得应用线性变换和对偶向量点乘等价。
{%asset_img cross_product_duality_equal.png %}

回到叉积上面
1，叉积就是要根据给定的$\vec{v}$和$\vec{w}$做一个从3维空间到一维的线性变换（回忆一下，二维到一维的变换就是给定了一个$\vec{u}$）
2，然后我们要根据这个变换找到其对应的对偶向量
3，这个对偶向量就会是$\vec{v}$和$\vec{w}$的叉积

对于空间中任意一个向量$\begin{bmatrix} x \\\ y \\\ z \end{bmatrix}$
,其与$\vec{v}$与$\vec{w}$形成的平行四边形的体积可以表示成：
$$f(\begin{bmatrix} x\\\y\\\z \end{bmatrix}) = det(\begin{bmatrix} x&v_1&w_1 \\\ y&v_2&w_2 \\\ z&v_3&w_3 \end{bmatrix})$$

这个函数一个重要特征就是，这是个线性函数：(平行，等距，固定原点)
1.易知，当u取原点时，这一变换会使之缩到原点，因为这个平行六面体已经没有高了.
2.根据相似的原理，当u在一条直线上运动时，这个平行六面体的体积与u的长度成正比
3.所以在这条直线上等距取u时，这一变换会使得这些点在数轴上等距分布

一旦你知道这个是线性的，我们就可以运用对偶性来解决问题，也就是f()部分可以改成一个1x3矩阵与向量$\begin{bmatrix} x \\\ y \\\z \end{bmatrix}$的线性变换：

$$\begin{bmatrix} ?&?&? \end{bmatrix}\begin{bmatrix} x \\\ y \\\ z \end{bmatrix} = det(\begin{bmatrix} x&v_1&w_1 \\\ y&v_2&w_2 \\\ z&v_3&w_3 \end{bmatrix})$$

并且由于对偶性（也就是线性变换可以用这个矩阵的倒置与特定向量(x,y,z)来做点积来表示）

$$\begin{bmatrix} ?\\\?\\\? \end{bmatrix} \cdot \begin{bmatrix} x \\\ y \\\ z \end{bmatrix} = det(\begin{bmatrix} x&v_1&w_1 \\\ y&v_2&w_2 \\\ z&v_3&w_3 \end{bmatrix})$$

所以说我们要找的就是这个特殊的3D向量$\vec{p}$，使得向量p与其他任一向量(x,y,z)的点积等于一个3x3矩阵的行列式(这个矩阵第一列为这个任一向量(x,y,z),其余两列分别为v和w的坐标)

{%asset_img cross_product_p.png %}

这个时候我们**从计算的角度**来看，p的值单纯就由向量$\vec{v}$与向量$\vec{w}$来表示
{%asset_img cross-product-p.png %}
$$
\begin{cases}
p_1 = v_2 \cdot w_3 - v_3 \cdot w_2 \\\ 
p_2 = v_3 \cdot w_1 - v_1 \cdot w_3 \\\ 
p_3 = v_1 \cdot w_2 - v_2 \cdot w_1
\end{cases}
$$

这个计算过程与叉积的计算定义是如此的相似,而叉积定义中的$\hat{i},\hat{j},\hat{k}$只不过在传递一个信号，也就是我们应该把这些系数解读为一个向量的坐标
{%asset_img cross_product_p2.png %}
{%asset_img cross-product-definec.png %}

**从Geomatrically理解**

首先$\vec{p} \cdot \begin{bmatrix} x\\\y\\\z \end{bmatrix}$的几何意义就是将这个(x,y,z)向量映射到向量$\vec{p}$上，然后将这个投影长度与p的长度相乘:
{%asset_img cross_product_pdot.png %}

然后再从平行六边形体积的计算方式来看，首先是一个平行四边形面积(向量$\vec{v}$,$\vec{w}$)的底乘以向量(x,y,z)在垂直于平行四边形方向上的分量
{%asset_img cross-product-geo1.png%}

这个时候我们来看这个公式：
$$\vec{p} \cdot \begin{bmatrix} x \\\ y \\\ z \end{bmatrix} = det(\begin{bmatrix} x&v_1&w_1 \\\ y&v_2&w_2 \\\ z&v_3&w_3 \end{bmatrix})$$
就可以看成：
$$\vec{p} \cdot \begin{bmatrix} x \\\ y \\\ z \end{bmatrix} = \text{(Area of the parallelogram)} \times \text{(Component of }\begin{bmatrix} x\\\y\\\z \end{bmatrix} \text{perpendicular to v and w)}$$
其中左边代表**向量(x,y,z)映射到$\vec{p}$的长度**再$\times \vec{p}$的长度，右边(Component....)刚好与“向量(x,y,z)映射到$\vec{p}$的长度”的意义相同，所以**$\vec{p}$的长度也就是(Area of the parallelogram)**

## 基变换
{%asset_img basis_transform_1.png %}
用我们的基变量替换别人的基变量得到在我们坐标下变换后的变量
其实这个计算过程，就相当于矩阵的相乘：
{%asset_img basis_transform_2.png%}
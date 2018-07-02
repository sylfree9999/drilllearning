---
title: net-expression
date: 2018-06-28 11:38:39
tags: [net, concept]
---

表达式目录树Expression
编译之后不是生成的方法，不是一个委托

```c#
Func<int,int,int> func = (m,n) => m*n+2;
Expression<Func<int,int,int>> exp = (m,n)=> m*n+2;

int iResult1 = func.Invoke(12,23);
int iResult2 = exp.Compile().Invoke(12,23);
```
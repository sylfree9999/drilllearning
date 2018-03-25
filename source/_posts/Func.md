---
title: Func
date: 2018-03-25 23:07:57
tags: [c#, concept]
---

`Func<T1,T2,...,Tn,Tr>` represents a function that takes `(T1, T2, ..., Tn)` and returns `Tr`

E.g., you have function:
```
double sqr(double s){
	return x*x;
}
```
You could save it as some kind of a function-variable:
```
Func<double, double> f1 = sqr;
Func<double, double> f2 = x=> x*x;
```

And then use exactly as you would use sqr:
```
f1(2);
f2(f1(4))
```

.
---
title: conda-packages-install
date: 2018-05-29 15:31:15
tags: [python, practice]
---

## 如何查看一个包所在的地址

*	

```
import numpy
print numpy.__file__
```


*	

```
import os
import numpy
path = os.path.dirname(numpy.__file__)
```
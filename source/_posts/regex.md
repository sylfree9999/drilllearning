---
title: 基础正则表达式
date: 2019-04-10 10:42:12
tags: [regex]
---

## 风格

```javascript
//JS风格
let re = new RegExp('\\d+','g');
//perl风格
let re = /\d+/g; // '/'为定界符
```

## 选项

### 	i, 忽略大小写

```javascript
let str = 'AAdsfasdfaertert';
let re = /a/i; //找到a
alert(str.search(re));
```

### 	g, 全局匹配

## 方法

### 	match 匹配

```javascript
let str = "234sdfsfsd aser0934534sdf lert09345";
let re = /\d+/g; //找出所有的数字
alert(str.match(re));
```

### 	replace替换

```javascript
let str = "sdf3aedfsafd Adsffg Asdf";
alert(str.replace(/a/gi,'*'));//替换掉所有的a为*
```

### 	test测试

​	`test`返回`true/false`,注意的是如果是用`test`，不限定行首行尾的话，只要部分匹配就算`true`

## 量词

| 量词   | 释义                 |
| ------ | -------------------- |
| x?     | x,零次或一次         |
| x*     | x,零次或多次         |
| x+     | x,一次或多次         |
| x{n}   | x,恰好n次            |
| x{n,}  | x,至少n次            |
| x{n,m} | x,至少n次，不超过m次 |

## 元字符-`[]`

### 	任何一个

​		`/a[abc]q/` - 可以匹配aaq,abq,acq,<span style="color:red">在正则中只要不写量词，默认就是匹配一个</span>

### 	范围

​		`/[a-z]/i`

​		`/[0-9]`

​		`/[a-z0-9]/`

​		`[3-59]` 这个不是匹配3~59而是代表可以是3~5或者是9，<span style="color:red">因为正则没有分隔符</span>

### 	排除`^`

​		`[^a-z0-9]` 排除字母a-z和数字0-9

## 转义

| 转义名称 | 含义                                                        |
| -------- | ----------------------------------------------------------- |
| \w       | [a-z0-9]                                                    |
| \d       | [0-9]                                                       |
| \s       | 空白字符，包括换行，tab                                     |
| \D       | [^0-9]                                                      |
| \W       | [^a-z0-9]                                                   |
| \S       | 非空白字符                                                  |
| .        | 任意字符，例如a，任意字符5-18，z，那么可以写成`/a.{5,18}z/` |

## 修饰符

| 修饰符 | 含义                                                         |
| ------ | ------------------------------------------------------------ |
| ^      | <span style="color:red">注意，只有在元字符[]里面的^才代表排除</span>，行首 |
| $      | 结尾                                                         |

例，判定是否为QQ号，规则是第一个不为0，共5~12位数字，这里必须要加入行首`^`和行尾`$` 

```javascript
let re = /^[1-9]\d{4,11}$/;
if(str.test(re)){ //str.test如果正则里面不包含行首和结尾限定符（从头到尾），则只要字符串部分匹配也为true,例如ssd124768625d，也可以通过
    alert("Pass");
}else{
    alert("Fail");
}
```

## 优先级

​	`|`-或优先级，或的优先级非常低，所以如果要匹配gif/png/jpg结尾的图片，写成`/\.jpg|gif|png$/i`其实是<span style="color:red">错的!在计算机眼里，因为或优先级很低，所以会读成要么.jpg,要么gif，要么png$, 所以字符串`sdfgifsdgterstpng`也可以匹配成功</span>

```javascript
let re = /\.jpg|gif|png$/i;  //Wrong
let re = /\.(jpg|gif|png)$/i;
```

例，判定0-9999

```javascript
let re = /^(\d|[1-9]\d|[1-9]\d\d|[1-9]\d\d\d)$/;
//可以简写成
let re = /^(\d|[1-9]\d{1,3})$/;
```


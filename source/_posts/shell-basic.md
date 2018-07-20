---
title: Shell 基本语法
date: 2018-06-20 16:14:59
tags: [shell, concept]
---

## . ./test.sh 两个点的含义
```
#!/bin/bash
aa = "hello"
```
如果`echo $aa`是没有东西的，为什么？

当只运行一个	`./test.sh` 的时候,其实是test.sh是在别的进程里面跑的，所以你在当前进程里跑的时候是不会输出东西的
所以用`. ./test.sh`是说在我现在这个进程里面来跑这个脚本

## 变量定义

	1，系统变量：$HOME、$PWD、$SHELL(现在用的是哪种解释器)、$USER(当前用户)等
	2，查看所有变量:`set`
	3，定义变量：VAR=value，<span style="color:red;">等号两侧不能有空格</span>，变量名称一般为大写 
	4，双引号与单引号的区别：双引号仅将空格脱意，单引号会将所有特殊字符脱意(单引号里面用变量引用没有用) 

		```
		X=hello
		echo $X -> hello
		X="hello world"
		echo $X -> hello world
		X='hello\nworld'
		echo $X -> hello\nworld
		Y=abc
		X='hello $Y'
		echo $X -> hello $Y
		X="hello $Y"
		echo $X -> hello abc
		```

	5，撤销变量：unset X
	6，export：可以把变量提升为全局环境变量，所有连上去的BASH都能访问，否则只在当前的bash能用

	7，<span style="color:red;">把当前command的结果赋予另一个变量</span>
		1，用A=`ls -la`反引号的形式
		2，用A=$(ls -la)，等价于上面的方式

		```
		X="Hello;World;SS"
		echo $X | cut -d ";" -f2  //拿到以；为分隔符切分的第二个元素
		Y=`echo $X | cut -d ";" -f2`
		echo $Y -> World
		```

	8，Shell中的特殊变量
		1，$? 上一个命令执行的状态，类似与方法的返回值，通常情况下返回值为0代表成功，非0代表不正常
			```
			true
			echo $? -> 0
			false
			echo $? -> 1
			ll
			echo $? -> 0
			lsss
			echo $? -> 127
			```
		2，$$ 表示当前进程号
		3，$0 表示当前脚本名称
		4，$N 表示N位置的输入参数
			```
			#!/bin/bash
			aa="hello"
			echo "第一个参数="$1
			echo "第二个参数="$2

			./test.sh hello world
			第一个参数=hello
			第二个参数=world
			```
		5，$# 表示参数的个数，常用于循环
		6，$*和$@都表示参数列表
			"$*"会将所有的参数作为一个整体，以"$S1$S2...$Sn"的形式输出
			"$@"会将各个参数分开，以"$S1""$S2"..."$Sn"的形式输出
			```
			#!/bin/bash
			echo $*
			echo $@
			for N in "$*"
			do
			echo $N
			done

			for N in "$@"
			do
			echo $N
			done

			```

## 运算符
格式：expr m+n 或者 $((m+n)) 注意expr运算符间要有空格
例如（2+3）*4
```
S=`expr 2+3`\*4 或者 $(((2+3)*4)),最外层的$()代表取其值
```

## for循环
```
for N in 1 2 3
do
	echo $N
done
或者 for N in {1..3};do echo $N;done
或者
for ((i=0;i<=5;i++)) //必须要是两层括号
do
	echo "welcome $i times"
done
```

## while循环
```
while expression
do 
	command
done
或者
int=1
while ((int<=3))
do
	echo $int
	let int++
done
```

## case语句
```
case $1 in
start)
	echo "starting"
	;;
stop)
	echo "stoping"
	;;
*)
	echo "Usage:{start|stop}"
esac
```

## read命令
```
read -p "please enter a number: " numb
please enter a number:  1
echo $numb
1
```

## if
```
if [ $NAME=root ]
then
	echo "hello ${NAME}"
elif [ $NAME=itcast ]
	then
		echo "hello ${NAME}"
else
	echo "OUT"
fi
```
[ condition ]一定要前后有空格，空[  ]则返回1，即false

## 判断语句
[ condition ] && echo OK || echo notok
= 字符串比较
-lt 小于
-le 小于等于
-eq 等于
-gt 大于
-ge 大于等于
-ne 不等于
-r 	有读的权限
-w 	有写权限
-f 	文件存在并且是一个常规的文件
-s 	文件存在且不为空
-d 	文件存在并且为一个目录
-b 	文件存在并且是一个块设备
-L 	文件存在并且是一个链接

## Shell 自定义函数
```
[ function ] funname [()]
{
	action;
	[return int;]
}
例如可以这样定义
function start() / function start/ start()
函数只能返回int类型

如果要传入参数，需要在外面定义

!#/bin/bash
function fSum()
{
	echo $1,$2;
	return $(($1+$2));
}
fSum 3 2;
total=$?;
fSum 5 7;
total=$?;
echo $total, $?;
```
## 脚本调试
`sh -vx helloWorld.sh` 只会展现所有的执行状态，不会停

## 模拟用户输入
```bash
auto_ssh_copy_id() {
	expect -c "set timeout -1;
		spawn ssh-copy-id $1;
		expect {
			*(yes/no)* {send -- yes\r;exp_continue;}
			*assword:* {send -- $2\r;exp_continue;}
			eof		   {exit 0;}
		}
	";
}


ssy_copy_id_to_all() {
	for SERVER in $SERVERS
	do
		auto_ssh_copy_id $SERVER $PASSWORD
	done	
}
```
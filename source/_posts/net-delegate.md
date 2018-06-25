---
title: net-delegate
date: 2018-06-22 16:39:17
tags: [.NET, concept]
---

## 声明
`public delegate string WithReturnWithPara(int x, int y);`没有方法体的方法声明+delegate

委托其实就是MulticastDelegate的一个**子类**，是一个**类**！

```c#

public delegate void NoReturnNoPara();
public delegate void NoReturnWithPara(int x, int y);
public delegate int WithReturnNoPara();
public delegate void GenericDelegate(T x); //泛型委托

public void Show()
{
	{
		//2. 实例化委托，要求传入的签名一致的方法
		NoReturnNoPara method = new NoReturnNoPara(this.DoNothing);
		//3. 委托实例的调用，参数和委托声明的时候参数一致
		method.Invoke();
		//4. 与上面的Invoke效果是一样的
		method();
	}
	{
		NoReturnWithPara method = new NoReturnWithPara(this.DoNothingWithPara);
		method.Invoke(1,2);
	}
	{
		WithReturnNoPara method = new WithReturnNoPara(this.GetNothing);
		int iResult = method.Invoke();
	}

}

private void DoNothing()
{
	Console.WriteLine("This is DoNothing");
}

private void DoNothingWithPara(int x, int y)
{

}

private int GetNothing()
{
	return 1;
}
```
##.NET自带的一些委托类型

####Action -> 无返回值的委托
```c#
Action act = new Action(this.DoNothing);
Action<int,string,int,string> act2 = null;
```
####Func -> 带返回值的泛型委托，注意，最后一个泛型类型代表返回类型
```c#
Func<int> fun1 = new Func<int>(this.GetNothing);//返回一个int类型
Func<int,string> fun2 = null; //接受一个int类型的参数，返回类型为string
```
####多播委托 -> 
+=表示向一个委托实例里面添加多个方法，形成方法链，invoke的时候按添加顺序执行
-=表示向一个委托实例里面移除方法，从方法链尾部开始匹配，遇到第一个完全吻合的，移除且只移除一个；没有匹配的不报错

**如果是用lambda表达式来定义方法，那么永远都无法-=，因为编译器碰到lambda表达式，会自动生成一个委托，都是不同的实例**

**多播委托<span style="color: red">不适用于带返回值的委托</span>>带返回值的委托，因为到后面只会拿最后一个委托的返回值**

```c#
Action act = new Action(this.DoNothing);
act += this.DoNothing;
act += this.DoNothingStatic;
act += new OtherClass().DoNothing;

//act.BeginInvoke(null, null);//不能调用，因为不知道里面这么多实例应该按照什么顺序去执行
foreach(Action item in act.GetInvocationList())
{
	item.BeginInvoke(null,null);
}

act -= this.DoNothing;
act -= this.DoNothingStatic;
act -= new OtherClass().DoNothing; //你会发现这个方法没有被移除，原因是上面的act += new OtherClass()与这个是两个实例，不是同一个，所以没有移除

```

##委托的使用
```c#
private static List<Student> Where(List<Student> studentList, Func<Student, bool> func)
{
	list<Student> resultList = new List<Student>();
	foreach(var student in studentList)
	{
		if(func.invoke(student))
		{
			resultList.Add(student);
		}
	}
}
//caller
private static bool Equals(Student)
{
	return student.ClassId == 1;
} 

Func<Student,bool> func = new Func<Student,bool>(Equals);
var list = Where(studentList, func);
```

---
title: net-oo
date: 2018-06-22 15:28:35
tags: [.NET, concet]
---

##封装就是写类

封装的好处:
*	保护属性，通过访问修饰符(public, private(只能自己访问，子类都不行),internal(只能这个程序集里面访问),protected(只能自己和子类访问))
*	接口不变，可以随便扩展
*	代码重用，任何只要用了这个类都可以调用这个方法


##继承，就是可以用父类的

##多态：同一个东东运行的时候会展现不同的形态

1. 继承多态：
```c#
//编译器编译的时候认为这三个都是People类型
//但在运行的时候people, student, teacher是三种不同的类型
People people = new People();
People student = new Student();
People teacher = new Teacher();
```
2. 编译时多态:
	声明，接口
	方法的重载(overload)也是多态
	<span style="color: red;">普通方法的调用</span>
		注意：`Parent ins = new Child(); ins.Method();`会调用的是父类方法，因为这是编译时确定的！！！


3. 运行时多态
	抽象方法与虚方法的区别：
		虚方法本身是一个普通方法，但是加了一个virtual，子类继承的时候可以覆写也可以不覆写
		抽象方法没有方法体，必须在一个抽象类里面定义，子类继承后，必须显性的override掉这个抽象类

	在override之前加`sealed`代表不想让它的子类再覆写

	<span style="color: red;">`new`这种写法尽量不要用！改成虚方法</span>

```c#
public abstract class ParentClass
{
	public int age = 70;

	public void CommonMethod()
	{
		Console.WriteLine("ParentClass CommonMethod");
	}

	//虚方法本身是一个普通方法，但是加了一个virtual
	//子类继承的时候可以覆写也可以不覆写
	public virtual void VirtualMethod()
	{
		Console.WriteLine("ParentClass VirtualMethod");
	}

	public virtual void VirtualMethod(string name)
	{
		Console.WriteLine("ParentClass VirtualMethod with string name");
	}

	//抽象方法没有方法体，必须在一个抽象类里面定义
	//子类继承后，必须显性的override掉这个抽象类
	public abstract void AbstractMethod();
}

public class ChildClass: ParentClass
{
	public int age  = 18;

	//这里隐藏父类的CommonMethod,并没有覆盖掉
	public new void CommonMethod()
	{
		Console.WriteLine("ChildClass CommonMethod");
	}

	public override void VirtualMethod()
	{
		Console.WriteLine("ChildClass VirtualMethod");
		base.VirtualMethod();
	}

	public override void AbstractMethod()
	{
		Console.WriteLine("ChildClass AbstractMethod");
	}
}

//caller
public static void Test()
{
	ParentClass instance = new ChildClass();
	//父类，age=70
	Console.WriteLint(instance.age);
	//父类,编译的时候决定了普通方法的调用，只根据等号左边来看，ChildClass里面的new一点用都没有
	instance.CommonMethod();
	//子类，虽然最终调用的是父类，运行的时候决定了虚方法的调用
	instance.VirtualMethod();
	//子类,运行时决定了抽象方法的调用
	instance.AbstractMethod();
}
```

##接口抽象类

什么方法适用于虚方法：
	大家都有默认实现，只有少部分不同，建议采用虚方法
其他用abstract方法：
	抽象方法就是约束一下，但是不提供实现，子类必须override，且必须在抽象类里面

	**抽象类是不能实例化的**，只能这么用
	
	```c#
	BasePhone iphone = new iPhone();

	public abstract class BasePhone
	{

	}
	```

除了可以用抽象类来约束，也可以用接口来约束,接口方法默认都是public，且不能放字段（可以放属性）
```c#
public interface IExtend
{
	void Online();
	string Remark{get;set;}
	event Action DoNothingHandle;
	//索引器
	string this[int index]{get;set;}
	//string description; 不能
	//delegate xxx;不能
}
```

抽象类和接口区别，想约束东西的时候是用抽象类还是接口？

*	抽象类可以包含一些已经实现的东西，然后可以再加上约束的功能，其主要是类，加上一点约束的功能，表明的主要是is a what
*	接口更灵活，一个类可以继承多个接口，纯粹的约束功能。只能表明can do what,不局限于是哪个类

工作中大部分用的都是接口，除非有些代码需要重用会要用抽象类 
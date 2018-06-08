---
title: net-reflection
date: 2018-06-07 14:54:29
tags: [.NET, concept]
---

### 代码编译成机器码的过程
<span style="color: red">注意在变成exe/dll之后还会有一层CLR/JIT，才会编译成机器码</span>

{% asset_img 20180607145635.png %}

为什么要有二次编译：
兼容性，不同的平台。32位64位/linux,windows在不同环境下编译的方法不同

想用同一种高级语言通用于所有的平台


#### 反射调用带参数的构造函数：

```c#
Assembly assemly = Assembly.Load("Test.DB.SqlServer"); //以前需要依靠一个类，现在相当于只依赖于一串字符串
Type testType = assemly.GetType("Test.DB.SqlServer.ReflectionTest"); //注意传的时候需要加上前方的namespace
object oTest1 = Activator.CreateInstance(testType);//默认调用无参构造函数
object oTest2 = Activator.CreateInstance(testType,new object[]{895,"霉霉"});//调用参数第一个是int类型，第二个是string类型的构造函数
```

#### 反射调用Generic类型:
```c#
//Generic Class
namespace Test.DB.SqlServer
{
	public class GenericClass<T,W,X>
	{
		public void Show(T t, W w, X x)
		{
			Console.WriteLine("t.type={0},w.type={1},x.type={2}", t.GetType().Name,w.GetType().Name,x.GetType().Name);
		}
	}
}


Assembly assemly = Assembly.Load("Test.DB.SqlServer"); 
Type genericType = assemly.GetType("Test.DB.SqlServer.GenericClass`3");//因为泛型有占位符，所以要写占位符
Type realGenericType = genericType.MakeGeneric(typeof(int),typeof(string),typeof(Program)); //用genericType是无法生成实例的，因为这个时候还没有参数类型，必须要定义好才能用，所以要调用MakeGeneric方法，用realGenericType生成占位符
object oGeneric = Activator.CreateInstance(realGenericType);
```

#### 反射调用Singleton单例

单力模式的意思就是保证程序运行的时候只会对这个类实例化一次

##### 构造函数种类及执行顺序
1. 默认构造函数，如果没有为类指定任何构造函数，编译器会自动为类创建一个无参构造函数
2. 静态构造函数，不能访问实例成员，只能用来初始化一些静态字段或者属性，**仅在第一次调用类的任何成员时自动执行，不带反问修饰符，不带任何参数，且每个类只能有一个静态构造函数**
3. 	私有构造函数，将构造函数声明为私有，则不能通过new()在外部代码中实例话，可以这样实例：
```c#
public class Demo
{
	private Demo(){}
	public static Demo NewDemo()
	{
		return new Demo();
	}
}

```
4. **构造函数的执行顺序**
	**子类静态构造 -> 父类静态构造 -> 父类构造 -> 子类构造**


单例模式
通常使用的情况是<span style="color: red">不能在外面调用单例模式的私有构造函数的</span>
但是通过反射的方法是可以<span style="color:red; font-weight: bold;">调用单例模式的私有构造函数</span>!

```c#

namespace Test.DB.SqlServer
{
	public sealed class Singleton
	{
		private static Singleton _Singleton = null;
		//构造函数首先要私有化，别人不能调用它，只能它自己调用
		private Singleton()
		{
			Console.WriteLine("Singleton被构造");
		}

		//静态构造函数首先会被调用，这个时候会调用私有构造函数
		//由于静态构造函数只会被调用一次，所以这个类也就只会被实例化一次
		static Singleton()
		{
			_Singleton = new Singleton();
		}


		public stati Singleton GetInstance()
		{
			return _Singleton;
		}
	}
}


Type singletonType = assemly.GetType("Test.DB.SqlServer.Singleton");

//反射是可以直接去访问单例模式的私有构造函数，下面这个方法会调用单例模式的私有构造函数
//并且还可以实例化多个单例
object oSingleton1 = Activator.CreateInstance(singletonType, true);
object oSingleton2 = Activator.CreateInstance(singletonType, true);
```

#### 反射不强制转换也能调用方法， Reflection + Method -> MVC

```c#
Assembly assemly = Assembly.Load("Test.DB.SqlServer");
Type testType = assemly.GetType("Test.DB.SqlServer.ReflectionTest");
object oTest1 = Activator.CreateInstance(testType);

MethodInfo method = testType.GetMethod("Show1"); //以前写的具体方法也都换成了字符串
method.Invoke(oTest1,new object[]{1332}); //调用含参数的方法
{
	method.Invoke(null,null);//调用无参数的静态方法，也可以写成method.Invoke(oTest1,null);	
}
{
	MethodInfo method = testType.GetMethod("Show3",new Type[]{}); //重载方法没有参数的
}
{
	MethodInfo method = testType.GetMethod("Show3", new Type[]{typeof(int)}); //重载方法有一个int类型的参数
}
{
	MethodInfo method = testType.GetMethod("Show4",BindingFlags.Instance | BindingFlags.NonPublic); //调用私有方法
}

public class GenericMethod
{
	public void Show<T,W,X>(T t, W w, X x)
	{
		Console.WriteLine("XXX");
	}
}

{
	Type genericType = assemly.GetType("Test.DB.SqlServer.GenericMethod");
	object oGeneric = Activator.CreateInstance(genericType); // 因为GenericMethod只是个普通类型，不是泛型类型
	MethodInfo method = genericType.GetMethod("Show"); //泛型方法不需要使用占位符
	MethodInfo methodNew = method.MakeGeneric(typeof(int),typeof(string),typeof(int)); //记得这里要重新生成一个MethodInfo
	methodNew.Invoke(oGeneric, new object[]{10,"test",10});
}

```

#### 反射调用属性和字段 Reflection + Property -> O/RM
```c#
 Type type = typeof(People);
 object oPeople = Activator.CreateInstance(type);
 foreach(var item in type.GetProperties()){ // 反射可以动态给对象属性赋值/获取值
 	Console.WriteLine(item.Name);
 	Console.WriteLine(item.GetValue(oPeople));
 	if(item.Name.Equals("Id"))
 		item.SetValue(oPeople,1234);
 	else if(item.Name.Equals("Name"))
 		item.SetValue(oPeople,"ttt");
 	Console.WriteLine(item.GetValue(oPeople))
 }
```
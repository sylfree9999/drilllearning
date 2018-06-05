---
title: .net-generic
date: 2018-06-05 11:12:08
tags: [.NET, concept]
---

## 	泛型约束

现在有类
```c#
public interface ISports
    {
        void Pingpang();
    }

    public interface IWork
    {
        void Work();
    }


    public class People
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public void Hi()
        { }

    }

    public class Chinese : People, ISports, IWork
    {
        public void Tradition()
        {
            Console.WriteLine("仁义礼智信，温良恭俭让");
        }
        public void SayHi()
        {
            Console.WriteLine("吃了么？");
        }

        public void Pingpang()
        {
            Console.WriteLine("打乒乓球...");
        }

        public void Work()
        {
            throw new NotImplementedException();
        }
    }

    public class Hubei : Chinese
    {

        public Hubei(int id)
        {
        }
        public string Changjiang { get; set; }
        public void Majiang()
        {
            Console.WriteLine("打麻将啦。。");
        }
    }


    public class Japanese : ISports
    {
        public int Id { get; set; }
        public string Name { get; set; }

        public void Pingpang()
        {
            Console.WriteLine("打乒乓球...");
        }
        public void Hi()
        { }
    }
```

如果你现在有一个Generic Method:
```c#
public class GenericMethod<T>
{
	public static void Show<T>(T instance){
		
		People pInstance = (People) instance;
		Console.WriteLine(pInstance.Id); //不会报错，但是这样做一点意义就没有了

		Console.WriteLine(instance.Id); //会报错，没有Id
		Console.WriteLint(instance.Name); //会报错，没有Name


	}
}

```

### 约束类型

如果现在有一个<span style="color: red">基类约束</span>

1. 	基类约束，可以使用基类里面的属性和方法
2. 	基类约束，要求类型参数必须是基类或者其子类，所以如果你调用GenericMethod.Show(japanese)就会报错，因为它不属于People类
3. 	基类约束，如果where后面跟多个类型，这些类型属于and关系，必须同时满足才行
```c#
public staic void Show<T>(T instance)
where T: People
{
	Console.WriteLine(instance.Id); //不会报错，因为告诉了T是属于什么类型
	Console.WriteLine(instance.Name);
}
```

<span style="color: red">类型约束</span>
```c#
public static T DoNothing<T>(T tParameter)
//where T: ISpotrs //接口类型约束
//where T: class // 引用类型约束
//where T: struct // 值类型约束
where T: new() //无参数构造函数约束
{
	//return default(T);//会根据T的类型，产生一个默认值，可以应用于值类型约束的返回

	//return null; //引用类型约束

	T t = new T();
	return t; //无参数构造函数返回
}

```

显示声明出来类型和用约束的区别

1. 	用约束来写更加灵活，比方说其可以运用ISports或者new()的写法
2. 	如果显式声明出来，就只能用People里面的方法

```c#
public static void Show<T>(T instance)
	where T: People, ISports, new() // and关系
{
	Console.WriteLine(instance.Id);
	Console.WriteLine(instance.Name);
	instance.Hi();
	instance.Pingpang();
	T t  = new T();
}
```

```c#
public static void ShowPeople(People instance)
{
	Console.WriteLine(instance.Id);
	Console.WriteLine(instance.Name);
	instance.Hi();
	instance.Pingpang();//报错
}
```

无参数构造函数约束
<span style="color: red">Hubei就不能使用，因为Hubei这个类里面没有定义无参构造函数</span>
```c#
Hubei hb = new Hubei(1);
GenericMethod.Show(hb);//报错
```

### Covariant协变与Contravariant逆变

out -> Covariant
in  -> Contravariant

<span style="color: red">只能放在接口或者委托的泛型参数前面</span>，类和方法是不能用的，这个跟之前定义函数的in, out是两个概念

协变与逆变只对引用类型有效，因为值类型没有什么父子关系

```c#
public class Bird{
	public int Id {get;set;}
}
public class Sparrow: Bird{
	public string Name{get;set;}
}
```
背景
```c#
Bird bird1 = new Bird();
Bird bird2 = new Sparrow(); //左边是父类，右边是子类
Sparrow sparrow1 = new Sparrow();
//Sparrow sparrow2 = new Bird();//错，不是所有的鸟都是麻雀

List<Bird> birdList1 = new List<Bird>();
List<Bird> birdList2 = new List<Sparrow>(); //错！！！！！！！！！一群麻雀是一群鸟这个竟然是错的，因为List<T>是一个泛型概念，List<Sparrow>与List<Bird>并没有父子关系

//只能像下面这样写，把每一个Sparrow转换成Bird才可以，有点不和谐了对不对
List<Bird> birdList3 = new List<Sparrow>().Select(c=>(Bird)c).ToList();

```
协变

**告诉编译器实例化的类型就是out T中T的子类**

先看下IEnumerable的定义，这里面用了协变
```c#
public interface IEnumerable<out T>: IEnumerable
{
	...
}
```
```c#
IEnumerable<Bird> birdList1 = new List<Bird>();
IEnumerable<Bird> birdList2 = new List<Sparrow>(); //这个就没问题，协变的意思就是说告诉编译器，如果我实例化的类型是我out的子类，就没问题
```
**协变只能是返回结果**
```c#
public interface ICustomerListOut<out T>
{
	T Get();
	//void Show(T t);//报错，如果用了协变，只能作为返回结果，不能作为参数类型
}

public class CustomerListOut<T>: ICustomerListOut<T>
{
	public T Get()
	{
		return default(T);
	}
}
```
逆变 Constravariant

**只能修饰传入参数**
```c#
public interface ICustomerListIn<in T>
{
	//T Get(); //报错，只能坐参数，不能作返回值
	void Show(T t);
}

public class CustomerListIn<T>: ICustomerListIn<T>
{
	public void Show(T t){

	}
}
```
定义了逆变以后，我可以实现<span style="color: red">左边子类，右边父类的情况</span>

```c#
ICustomerListIn<Sparrow> customerList1 = new CustomerListIn<Sparrow>();
ICustomerListIn<Sparrow> customerList2 = new CustomerListIn<Bird>(); //右边可以是父类！！！！！

//因为定义的时候已经定义了customerList2一定是Sparrow类型，在show的时候已经要求了必须传入Sparrow类型
customerList2.Show(new Sparrow());//Show这里要求必须传入的是Sparrow类型
```

### 	泛型类中的静态字段

泛型：jit编译的时候指定具体类型，同一个泛型类，不同的参数类型，其实会变成不同的类型

静态字段/静态构造函数：一个类型只会初始化一次，就在第一次调用的时候初始化，之后就常驻内存

那么！！！！
<span style="color: red">泛型+静态会怎么样？</span>

泛型类的静态字段，**是独立的**
它会根据不同类型，产生不同的类，只有在不同类型第一次声明的时候会初始化，但是相同类型第二次用的时候就不会初始化！

```c#

	Console.WriteLine(GenericCache<int>.GetCache());
	Thread.Sleep(10);
	Console.WriteLine(GenericCache<long>.GetCache());//第一次进long的时候，仍然会初始化
	Thread.Sleep(10);
	Console.WriteLine(GenericCache<int>.GetCache());//这个时候就不会在初始化了，因为int类型的已经初始化过了

```
这里就牵扯到了泛型静态缓存
**泛型缓存的效率非常高**，是直接在内存中缓存，CPU直接拿值
但是这个缓存没有办法清除
---
title: net-design-pattern
date: 2018-07-26 18:03:17
tags: [.NET, concept]
---
## 依赖倒置原则：怎么抽象
1，上层和下层中间应该通过一个抽象层进行工作，抽象是稳定的，实现是多变的！所以定义抽象要谨慎
2，每一层模块应该都要有抽象，有一个类cls,就要有一个ICls
3，调用者左边为抽象，右边为具体实现

```c#
//caller
{
	AbstractPhone phone = new iPhone();
	phone.Call();
}
{
	AbstractPhone phone = new Lumia();
	phone.Call();
}

//中间层，就相当于定义的一个规范
public abstract class AbstractPhone
{
	public int Id {get;set;}
	public string Branch {get;set;}
	public abstract void Call();
}

//下层实现层
public class iPhone:AbstractPhone
{
	public override void Call()
	{
		Console.WriteLine("This is iPhone calling!")
	}
}

public class Lumia:AbstractPhone
{
	public override void Call()
	{
		Console.WriteLine("This is Lumia calling!");
	}
}

```

其实中间层也可以写成一个泛型
```c#
public void Call<T>(T phone) where T : AbstractPhone
{
	Console.WriteLine("This is {0} calling", phone.Name);
}
```
## 接口隔离原则
划分接口的时候，首先不能大而全，也不能太碎，要按照一定的规则进行分组

## 设计模式-创建型设计模式，关注对象的创建
### 单例模式，就是保证类型只有一个实例，减少初始化的消耗

局限：
1，实例会常驻内存
2，实例中的变量，在多线程的情况下会被影响

使用场景：数据库连接池

#### 方法一
1，构造函数私有化，保证不会被外部创建
2，对外提供一个公开方法提供这个对象
3，实例定义成一个静态变量，保证内存中就只有一个
4，注意了，如果class Singleton变成class Singleton<T>,就无法保证实例是单例的，因为解释器会在编译的时候动态生成类型
```c#
public class Singleton
{
	private Singleton()
	{

	}
	//volatile保证多线程的时候值不会被多次修改
	private static volatile Singleton _singleton = null;
	private static object Singleton_Lock = new object();

	public static Singleton CreateInstance()
	{
		if(_singleton == null)
			_singleton = new Singleton();
		return _singleton;
	}
}
```
如果多线程同时调用上面的CreateInstance，就无法保证只构造一次(假设一个构造函数要构造40s)，所以需要加一层Lock

但是只加一次lock也不行，因为如果第二轮开5个线程让构造Singleton,则会发现第二轮的也在等待锁，而这个时候明明已经Singleton实例化好了的

所以在lock外面会再加上一层if判断

**经典的双if-lock:**
```c#
public static Singleton CreateInstance()
{
	if(_singleton is null)//保证对象初始化之后，不会再去等待锁
	{
		lock(Singleton_Lock)//保证只有一个线程进去
		{
			Thread.Sleep(1000);
			Console.WriteLine("这里等待了1s的锁");
			if(_singleton == null)//保证只会被实例化一次
				_singleton = new Singleton();
		}
	}
	
	return _singleton;
}
```

#### 方法二
1，通过静态构造函数来返回实例,是由CLR来保证程序第一次使用这个类型前被调用且只调用一次
```c#
public class SingletonSecond
{
	private static volatile SingletonSecond _singletonSecond = null;
	static SingletonSecond()
	{
		_singletonSecond = new SingletonSecond();
		Console.WriteLine("SingletonSecond starts").
	}
}
```

#### 方法三
1，使用静态字段，在第一次使用这个类之前，也是由CLR保证的，初始化且只初始化一次
```c#
public class SingletonThird
{
	private SingletonThird()
	{

	}

	private static SingletonThird _singletonThird = new SingletonThird();

	public static SingletonThird CreateInstance()
	{
		return _singletonThird;
	}
}
```

### 原型模式,解决对象重复创建的问题
局限：
1，常驻内存
2，多线程的话，会在内存中创建多个实例，即使这个实例跟第一次创建的实例是一样的

1，通过MemberwiseClone来clone新对象，避免重复创建对象
2，每次Clone的时候都是以第一次SingletonSecond静态构造函数构造的来copy，所以每次返回的是新的对象
```c#
public static SingletonSecond CreateInstancePrototype()
{
	SingletonSecond sp = (SingletonSecond)_singletonPrototype.MemberwiseClone();
	return sp;
}
```
### 三大工厂+建造者模式
#### 简单工厂
局限：
1，细节没有消失，只是转移，并且矛盾都集中在了一个地方
```c#
{
	//不好，左右两边都是具体实现
	Human human = new Human();
	player.PlayWar3(human);
}
{
	//好，左边是抽象，右边是细节
	IRace human = new Human();
	player.PlayWar3(human);
}
{
	//如何把右边也替换掉？简单工厂模式,就是帮忙完成对象的创建
	IRace human  = ObjectFactory.CreateRace(RaceType.Human);
	player.PlayWar3(human);
}


public static IRace CreateRace(RaceType raceType)
{
	IRace iRace = null;
	switch(raceType)
	{
		case RaceType.Human:
			iRace = new Human();
			break;
		case RaceType.Undead:
			iRace = new Undead();
			break;
		default:
			throw new Exception("Wrong race!");
	}
	return iRace;
}

//简单工厂的升级，用反射
//这样写程序里面完全没有细节，细节都在config文件里面
private static string IRaceTypeConfigReflection = ConfigurationManager.AppSettings["IRaceTypeConfigReflection"];
private static string DllName = IRaceTypeConfigReflection.Split(',')[1];
private static string TypeName = IRaceTypeConfigReflection.Split(',')[0];
///IOC的雏形
public static IRace CreateRaceConfigReflection()
{
	Assembly assembly = Assembly.Load(DllName);
	Type type = assembly.GetType(TypeName);
	IRace iRace = Activator.CreateInstance(type) as IRace;
	return iRace;
}

```

#### 工厂方法
1，将职责单一化，一个工厂只负责一种实例的创建
2，创建的工厂作为一个中间层，把细节包了一层
3，这样写方便扩展,可以增加新的行为
```c#
{
	IFactory factory = new HumanFactory();
	//IFactory factory = new HumanFactoryAdvanced();
	IRace race = factory.CreateRace();

}
public class HumanFactory: IFactory
{
	public virtual IRace CreateRace()
	{
		return new Human();
	}
}
//这样写方便扩展,可以增加新的行为
public class HumanFactoryAdvanced:HumanFactory
{
	public override IRace CreateRace()
	{
		Console.WriteLine("This is an extension.");
		return new Human();
	}
}
```

#### 抽象工厂
1，从外表来说是一个工厂去创建多个对象
2，适用于工厂里面的对象都紧密相连
```c#
public class HumanFactory:FactoryAbstract
{
	public override IRace CreateRace()
	{
		return new Human();
	}
	public override IArmy CreateArmy()
	{
		return new HumanArmy();
	}
	public override IHero CreateHero()
	{
		return new HumanHero();
	}
}

public abstract class FactoryAbstract
{
	public abstract IRace CreateRace();
	public abstract IArmy CreateArmy();
	public abstract IHero CreateHero();
}

//caller
{
	FactoryAbstract humanFactory = new HumanFactory();
	IRace race = humanFactory.CreateRace();
	IArmy army = humanFactory.CreateArmy();
	IHero hero = humanFactory.CreateHero();
}
```
**经验之谈：在创建一个对象的时候，尽量不要直接去创建这个对象，而是通过一个中间层，这样细节的变化只会波及到工厂，只改工厂的就好，不会波及到上层**

## 设计模式-结构型设计模式：关注类与类之间的关系
纵向可以：继承--实现
横向可以：聚合，组合，关联，依赖（是指在方法里用了别的类）
核心：组合优于继承

###  适配器模式Adapter

是在项目重构升级的时候会用，之前的方法已经都稳固了，但是这个时候想要用第三方的方法，就把第三方的方法与我们的方法适配一下

比方说我们之前定义了一个IHelper,里面定义了增删改查四个方法，并且已经有了MySqlHelper,OracleHelper

这个时候我们想要用一个第三方软件提供的RedisUtility,这里面也定义了自己增删改查方法，但是第三方是不可能继承于我们的类IHelper的，这个时候我们就需要写一个适配方法

#### 方法一：纵向

问题：侵入性很强
因为通过了继承，我多出了很多功能，我其实只需要IHelper的增删改查就好，但是这个时候我还拥有了RedisUtility里面的AddRedis之类的方法。并且如果RedisUtility什么时候也增加了Add方法，那么我们现在的方法就要改
```c#

public class RedisHelperClass: RedisUtility, IHelper
{
	public void Add<T>()
	{
		base.AddRedis<T>();
	}
	public void Delete<T>()
	{
		base.DeleteRedis<T>();
	}
	public void Update<T>()
	{
		base.UpdateRedis<T>();
	}
	public void Query<T>()
	{
		base.QueryRedis<T>();
	}
}

//caller
{
	IHelper helper = new RedisHelperClass();
	helper.Add<Program>();
}
```
#### 方法二：组合
另一种写法是组合，在类的内部内置了需要类的属性，字段

组合的写法就比较灵活，不仅类里面可以有redisHelper，如果将来想要有Cache也可以直接加上去

```c#
public class RedisHelperObject: IHelper
{
	private RedisUtility _redisHelper = null;
	public RedisHelperObject(RedisUtility redisHelper)//这里可能是一个抽象的接口注入进来
	{
		this._redisHelper = redisHelper;
	}

	public RedisHelperObject()
	{
		this._redisHelper = new RedisUtility();
	}

	public void Add<T>()
	{
		this._redisHelper.AddRedis<T>();
	}

	public void Delete<T>()
	{
		this._redisHelper.DeleteRedis<T>();
	}

	//...
}
```

### 代理模式
1，有一个真实的做事情的类
2，有一个接口
3，有一个代理的类，这个类继承于接口，也有方法的实现，但是到真正的实现是调用真实类来实现
4，代理只能传达原有逻辑，不能新增业务逻辑，就是包一层
5，真正调用的时候不再调用RealSubject，而是调用ProxySubject
6，这种模式可以让用户在真正使用的时候才去创建对象(DoSomething方法)。因为我在用的时候是调用的ProxySubject，这个构建不消耗资源
```c#
public class ProxySubject: ISubject
{
	//这个是单例代理
	private static ISubject _iSubject = null;
	private void Init()
	{
		_iSubject = new RealSubject();
	}

	//下面这个是缓存代理
	private static bool _booleanResult = false;
	private static bool _isInit = false;
	private static Dictionary<string,bool> _cache=new Dictionary<string,bool>();

	public bool GetSomething()
	{

		if(!_isInit)//缓存
		{
			_booleanResult = _iSubject.GetSomething();
			_isInit = true;
		}
		return _booleanResult;
	}

	//这个是延迟代理，延迟构建RealSubject
	public void DoSomething()
	{
		if(_iSubject == null)
		{
			this.Init();
		}
		_iSubject.DoSomething();
	}
}
```

###  装饰器模式
1，声明一个你需要用的变量
2，在构造函数中把你需要的变量初始化
```c#
public class BaseStudentDecorator: AbstractStudent
{
	//没有用继承的方式，用的是组合的方式，通过构造函数初始化变量
	private AbstractStudent _student = null;
	public BaseStudentDecorator(AbstractStudent student)
	{
		this._student = student;
	}

	public override void Study()
	{
		this._student.Study();
	}
}

public class StudentPayDecorator: BaseStudentDecorator
{
	public StudentPayDecorator(AbstractStudent student)
	:base(student)
	{

	}

	public override void Study()
	{
		Console.WriteLine("Pay");
		base.Study();
	}
}

//caller
{
	AbstractStudent student = new StudentVip()
	{
		Id = 381,
		Name = "Bird"
	};

	//BaseStudentDecorator decorator = new BaseStudentDecorator();
	//把左边BaseStudentDecorator换成AbstractDecorator
	//AbstractStudent decorator = new BaseStudentDecorator();
	//decorator.Study();
	student = new BaseStudentDecorator(student);
	student.Study();//输出的是vip学习

	//StudentPayDecorator studentPayDecorator = new StudentPayDecorator(decorator);
	//AbstractStudent studentPayDecorator = new StudentPayDecorator(decorator);
	//studentPayDecorator.Study();

	//也可以写成如下，这个时候的student为BaseStudentDecorator
	student = new StudentPayDecorator(student);
	student.Study();//输出先是pay，然后BaseStudentDecorator的Study,即输出vip学习

	//所以之后如果你想给一个对象加一些行为，都可以像这样写
	//AOP的雏形
	student = new BaseStudentDecorator(student);
	student = new StudentRegDecorator(student);
	student = new StudentPayDecorator(student);
	//最终打出来的是付费，注册，vip学习
	student.Study();
}
```

## 设计模式 - 行为型设计模式：关注对象和行为的分离
通俗来讲，就是把方法写在哪里更适合
哪里变化 就封装哪里，让别人传进来，自己不去完成

### 观察者模式
```c#
private List<IObserver> _observerList = new List<IObserver>();
public void Add(IObserver observer)
{
	this._observerList.Add(observer);
}
public void Remove(IObserver observer)
{
	this._observerList.Remove(observer);
}

public void MiaoObserver()
{
	foreach(var observer in this._observerList)
	{
		observer.Action();
	}
}

//上面这就类似于event,event就是委托的一个实例
public event Action MiaoHandler;
public void MiaoEvent()
{
	if(MiaoHandler != null)
	{
		foreach(Action item in this.MiaoHandler.GetInvocationList())
		{
			item.Invoke();
		}
		//this.MiaoHandler();
	}
}

```



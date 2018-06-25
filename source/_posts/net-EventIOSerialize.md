---
title: net-EventIOSerialize
date: 2018-06-25 10:00:51
tags: [.NET, concept]
---

## EVENT
假如现在有一个猫类型，它叫一声会引发一连串反应，诸如
```c#
public class Cat
{
	public void Miao()
	{
		new Neighbor().Awake();
		new Dog().Bark();
		new Mouse().Run();
		new Baby().Cry();
	}
}
```
这样的写法会导致耦合性高，不易扩展，增加，减少或者调整顺序都会变得比较困难，最好是猫叫一声->触发一系列的动作

**用委托的方法实现**

<!-- more -->

```c#
//这个MiaoEventHandler来指定一堆动作
//委托MiaoEventHandler来定义动作，Cat就不管了，Cat就不依赖于里面的动作了
public class Cat
{
	public Action MiaoEventHandler;
	
	public void MiaoAction()
	{
		if(this.MiaoEventHandler != null)
		{
			this.MiaoEventHandler.Invoke();
		}
	}
}



//caller
static void Main(string[] args)
{
	{
		//Event
		Cat cat = new Cat();
		cat.Miao();
		//委托的时候只能加方法名，而不是调用，所以不是Awake()

		//带有参数的方法的调用，就可以用lambda来完成
		//这就是多播委托的一种使用，注意，多播委托是不适用于带返回值的委托的，因为到最后只会取最后一个委托的返回值！
		cat.MiaoEventHandler += () => new Neighbor().Awake(123);
		cat.MiaoEventHandler += new Dog().Bark;
		cat.MiaoEventHandler += new Mouse().Run;
		cat.MiaoEventHandler += new Baby().Cry;
		cat.MiaoAction();
	}
}
```

**用事件的方法实现**

Event就是Action委托前面加event关键字，防止外部直接invoke和赋值，子类都没有办法Invoke

**事件和委托的区别联系：**
<span style="color: red">事件是委托的实例，委托是一个类型，而事件是一个实例，委托类型的实例</span>
例：Student是一个类型，而Dashan是Student类型的一个实例


```c#
public event Action MiaoEventHandlerEvent;
public void MiaoActionEvent()
{
	if(this.MiaoEventHandlerEvent != null)
	{
		this.MiaoEventHandlerEvent.Invoke();
	}
}
```

**为什么要有event?**
就是为了这个MiaoEventHandler不能在外部被调用被赋值

在上面的那个例子，`MiaoEventHandler`是可以在中间被invoke和赋值的，比方说
```c#
cat.MiaoEventHandler += () => new Neighbor().Awake(123);
cat.MiaoEventHandler += new Dog().Bark;

//这样是可以的
cat.MiaoEventHandler.Invoke();
cat.MiaoEventHandler = null;

cat.MiaoEventHandler += new Mouse().Run;
cat.MiaoEventHandler += new Baby().Cry;
```

<span style="color: red">但是如果用了Event，就不可以在中间被赋值，只能在Cat类的MiaoActionEvent里面去调用</span>

## EVENT的应用

事件的应用一定会有
1，事件的发布者，在这里用来Invoke事件
2，事件的订阅用户
3，事件的注册

```c#
//这个是事件的发布者，只有事件的发布者才能Invoke这个事件

public class iPhone8
{
	//EventHandler<PriceChangeEventArgs>是事件的委托类型， PriceChange是事件名称
	public event EventHandler<PriceChangeEventArgs> PriceChange;

	protected virtual void OnPriceChanged(PriceChangeEventArgs e)
	{
		if (this.PriceChange != null)
		{
			this.PriceChange.Invoke(this, e);
		}
	}

	private decimal price;
	public decimal Price
	{
		get {return price;}
		set 
		{
			if(price == value)
				return;
			decimal oldPrice = price;
			price = value;
			if(this.PriceChange != null)
				this.OnPriceChanged(new PriceChangeEventArgs(oldPrice, price));
		}
	}
	
}


//EventHandler是框架帮我们定义的，专门用来作事件用
//sender是事件的触发者, e的类型是泛型，也就是TEventArgs类型，一般这个类型在定义的时候必须继承于EventArgs
public delegate void EventHandler<TEventArgs>(object sender, TEventArgs e);
//EventArgs其实就是个空壳,但是你可以继承它之后自己自定义一些属性
public class EventArgs
{
	public static readonly EventArgs Empty;
	public EventArgs();
}

//PriceChangeEventArgs
public class PriceChangeEventArgs: EventArgs
{
	public int Id {get;set;}
	public readonly decimal OldPrice;
	public readonly decimal NewPrice;

	public PriceChangeEventArgs(decimal oldPrice, decimal newPrice)
	{
		OldPrice = oldPrice;
		NewPrice = newPrice;
	}
}




//事件订阅者
public class Businessman
{
	public void Iphone8_PriceChange(object sender, PriceChangeEventArgs e)
	{
		Console.WriteLine("年终大促,iphone只卖" + e.NewPrice + "元！");
	}
}

//事件的注册
public class EventRegister
{
	private iPhone8 _iphone = null;

	public void Init()
	{
		this._iphone = new iPhone8();
		Businessman businessman = new Businessman();
		this._iphone.PriceChange += businessman.Iphone8_PriceChange;
	}

	public void SetPrice(decimal price)
	{
		this._iphone.Price = price;
	}
}
```

## IO Serialize
```c#

//检查文件夹是否存在
if(!Directory.Exists(LogPath))
{
	//一次性创建全部的子路径
	DirectoryInfo directoryInfo = Directory.CreateDirectory(LogPath);
	//原文件夹会没有
	Directory.Move(LogPath, LogMovePath);
	Directory.Delete(LogMovePath);
}
//不能用这个检查文件夹是否存在
Directory directory = new DirectoryInfo(LogPath);
FileInfo fileInfo = new FileInfo(Path.Combine(LogPath,"info.txt"));
if(!File.Exists(Path.Combine(LogPath, "info.txt")))
{
	Directory.CreateDirectory(LogPath);
	//打开文件流（创建文件并写入）
	using(FileStream fileStream = File.Create(fileName))
	{
		string name = "111";
		byte[] bytes = Encoding.Default.GetBytes(name);
		fileStream.Write(bytes, 0 , bytes.Length);
		fileStream.Flush();
	}
	//打开文件流（创建文件并写入）,这个File.Create会把之前的文件删掉，重新写
	using(FileStream fileStream = File.Create(fileName))
	{
		StreamWriter sw = new StreamWriter(fileStream);
		sw.Write("123");
		sw.Flush();
	}
	//流写入器（创建/打开文件并写入）
	using(StreamWriter sw = File.AppendText(fileName))
	{
		string msg = "Today is a good day.";
		sw.WriteLine(msg);
		sw.Flush();
	}
	//流写入器(创建/打开文件并写入)
	using(StreamWriter sw = File.AppendText(fileName))
	{
		string name = "12312";
		byte[] bytes = Encoding.Default.GetBytes(name);
		sw.BaseStream.Write(bytes,0,bytes.Length);
		sw.Flush();
	}


	//读取,
	//一次性读所有的数据，不推荐
	foreach(var result in File.ReadAllLines(fileName))
	{
		Console.WriteLine(result);
	}

	string sResult = File.ReadAllText(fileName);

	Byte[] byteContent = File.ReadALlBytes(fileName);
	string sResultByte = System.Text.Encoding.UTF8.GetString(byteContent);

	//分批读取，比较好
	using(FileStream stream = File.OpenRead(fileName))
	{
		int length = 5;
		int result = 0;

		do 
		{
			byte[] bytes = new byte[length];
			result = stream.Read(bytes,0,5);
			for(int i=0; i< result; i++)
			{
				Console.WriteLine(bytes[i].TOString());
			}
		}
		while(length == result);
		
	}
}

//写日志
public static void Log(string msg)
{
	StreamWriter sw = null;
	try
	{
		string fileName = "log.txt";
		string totalPath = Path.Combine(LogPath, fileName);

		if(!Directory.Exists(LogPath))
		{
			Directory.Create(LogPath);
		}
		sw = File.AppendText(totalPath);
		sw.WriteLine(string.Format("{0}:{1}",DateTime.Now,msg));
		sw.WriteLine("**************************************")；
	}
	catch(Exception ex)
	{
		Console.WriteLine(ex.Message);
	}
	finally
	{
		if(sw != null)
		{
			sw.Flush();
			sw.Close();
			sw.Dispose();
		}
	}
}
```

## 画验证码
```c#
public static void Drawing()
{
	Bitmap bitmapobj = new Bitmap(100, 100);
	//在Bitmap上面创建一个新的Graphics对象
	Graphics g = Graphics.FromImage(bitmapobj);
	//创建绘画对象，如Pen,Brush等等
	Pen redPen = new Pen(Color.Red,8);
	g.Clear(Color.White);
	//绘制图形
	g.DrawLine(redPen,50,20,500,20);
	//画椭圆
	g.DrawEllipse(Pens.Black, new Rectangle(0,0,200,100));
	//画弧线
	g.DrawArc(Pens.Black,new Rectangle(0,0,100,100),60,180);
	//画直线
	g.DrawLine(Pens.Black,10,10,100,100);
	//画矩形
	g.DrawRectangle(Pens.Black,new Rectangle(0,0,100,200));
	//画字符串
	g.DrawString("I love coding",new Font("Arial",12),new SolidBrush(Color.Red),new PointF(10,10));

	If(!Directory.Exists(ImagePath))
	{
		Directory.CreateDirectory(ImagePath);
	}

	bitmapobj.Save(ImagePath+"pic1.jpg",ImageFormat.Jpeg);
	bitmapobj.Dispose();//释放所有对象
	g.Dispose();
}
```
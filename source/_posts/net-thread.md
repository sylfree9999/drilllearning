---
title: net-thread
date: 2018-07-22 21:57:15
tags: [.NET, concept]
---
## Thread (.NET 1.0) Basic

1，	前台线程thread.Start();进程退出后还会继续执行，直到执行结束。且前台线程只有这种形式，后面的ThreadPool,Async都是后台线程 
2，	后台线程thread.IsBackground=true;进程退出后还会继续执行，直到执行结束。

```c#
private void btnThreads_Click(object sender, EventArgs e)
{
	Console.WriteLine($"*************btnThreads_Click Start {Thread.CurrentThread.ManagedThreadId.ToString("00")}");

	ThreadStart threadStart = new ThreadStart(()=>
		{
			Thread.Sleep(5000);
			this.DoSomething("btnThreads_Click");
		});

	Thread thread = new Thread(threadStart);
	
	thread.IsBackground=true;//这样就会改成后台线程，这样进程退出后，线程也会一起推出
	thread.Start();//默认是前台线程，进程退出后还会继续执行，直到执行结束。

	//thread.Join();//做等待用的，执行thread的这个线程会等待thread线程
}
```
<!--more-->

### 用Thread实现回调且不卡界面
等同于BeginInvoke的回调
```c#
private void ThreadWithCallBack(ThreadStart threadStart, Action act)
{
	ThreadStart startNew = new ThreadStart(
			()=>{
				threadStart.Invoke();
				act.Invoke();
			}
		);
	Thread thread = new Thread(startNew);
	thread.Start();
}
```

### Thread实现带返回值的且不卡界面
```c#
private void ThreadWithReturn<T>(Func<T> funcT)
{
	T t = default(T);
	ThreadStart startNew = new ThreadStart(
			() = >
			{
				t = funcT.Invoke();
			});
	Thread thread = new Thread(startNew);
	thread.Start();

	//因为只有在计算委托的时候才会线程等待，所以返回的时候要包一个委托
	return new Func<T>(()=>
	{
		thread.Join();
		return t;
	});
}
```

## ThreadPool(.NET 2.0)
ThreadPool的特点：
1，减少了线程创建/销毁的工作
2，可以限制线程的数量

### 带回调的ThreadPool
```c#
ThreadPool.QueueUserWorkItem(
	o => {
		new Action(
			()=>{
				Thread.Sleep(5000);
				this.DoSomethingLong("btnThreads_Click");
			}).Invoke();
		//Callback
		Console.WriteLine("This is a callback func.");
	}
);
```

### 线程等待
Notice!没有需求，就不要等待，容易阻塞线程
```c#
//这个就是用作标志，如果这个标志是false，那么主线程就会一直等待,除非在子线程里面设置mre.Set()
ManualResetEvent mre = new ManualResetEvent(false);//false代表关闭
ThreadPool.QueueUserWorkItem(
	o => {
		Thread.Sleep(5000);
		this.DoSomethingLong("btnThreads_Click");
		Console.WriteLine(o.ToString());

		mre.Set();//打开
	},"backbone");

Console.WriteLine("before WaitOne");
mre.WaitOne();//这个是做真正的Wait操作，但是这里等待的是一个信号量，其不管是谁执行的，只有把mre.Set()我就立刻执行，这是与thread.Join()的区别
Console.WriteLine("after WaitOne");
mre.Reset();//关闭
```

## Task(.NET 3.0)
Task的优势：
1，使用的是线程池的线程，全部是后台线程
2，API十分强大

```c#
TaskFactory taskFactory = Task.Factory;
{
	taskFactory.StartNew(()=>{this.DoSomethingLong("btnTask_Click001");});
taskFactory.StartNew(()=>{this.DoSomethingLong("btnTask_Click002");});
taskFactory.StartNew(()=>{this.DoSomethingLong("btnTask_Click003");});
}
```

### 需要多线程加快速度，但是又要求全部/某些完成后才能返回
这种写法会卡界面
```c#
TaskFactory taskFactory = Task.Factory;

{
	List<Task> taskList = new List<Task>();
	taskList.Add(taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click001")));
	taskList.Add(taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click002")));
	taskList.Add(taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click003")));
	//这个一定会卡界面，因为是主线程在等待
	Task.WaitAll(taskList.ToArray());
	//需要某个完成之后返回,只要其中有任何一个完成，就打印下一句，然后其他的子线程再陆续自行完成
	Task.WaitAny(taskList.ToArray());

	Console.WriteLine("全部任务都完成才能走到这里")
}
```

### 不卡界面的写法/回调
```c#
TaskFactory taskFactory = Task.Factory;
List<Task> taskList = new List<Task>();
taskList.Add(taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click001")));
taskList.Add(taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click002")));
taskList.Add(taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click003")));

taskFactory.ContinueWhenAny(taskList.ToArray(),t=>Console.WriteLine($"This is ContinueWhenAny {Thread.CurrentThread.ManagedThreadId.ToString()}"));
taskFactory.ContinueWhenAll(taskList.ToArray(), tList => Console.WriteLine($"This is ContinueWhenAll callback {Thread.CurrentThread.ManagedThreadId.ToString()}"))

Task.WaitAny(taskList.ToArray());
Console.WriteLine("某个任务完成，才会执行");

Task.WaitAll(taskList.ToArray());
Console.WriteLine("全部任务都完成，才会执行");

```
这里注意了，一般ContinueWhenXX都是在Task.WaitXX之后执行的，因为Task.WaitXX是主线程，它只需要听从一个信号量就可以，但是ContinueWhenXX是需要重新起一个线程，所以会比较慢

{%asset_img TaskWhenAny.png %}

### 那么如何知道到底是哪个线程任务完成了呢？可以在taskFactory.StartNew的时候定义一个state
```c#
Task task = taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click001"),"It's A NAME");
//task.AsyncState里面就会保存“It's A NAME”
```
### 取返回值
```c#
Task<int> intTask = taskFactory.StartNew(()=>123);
int iResult = intTask.Result;
```

### 如果只想某一个线程里面做回调
```c#
Task task = taskFactory.StartNew(()=>this.DoSomethingLong("btnTask_Click001"),"It's A NAME")
	.ContinueWith(t=>Console.WriteLine("这里是It's A Name的回调"));
```

## Parallel
1，相当于Task+WaitAll
2，主线程也参与计算，节约了一个线程，所以计算的时候卡界面

```c#
Parallel.Invoke(()=> this.DoSomethingLong("btnParallel_Click_001"),
	()=> this.DoSomethingLong("btnParallel_Click002"),
	()=> this.DoSomethingLong("btnParallel_Click003"),
	()=> this.DoSomethingLong("btnParallel_Click004"));
```
{%asset_img parallel.png %}

也可以写成这种形式
```c#
Parallel.For(0,5,t=>{
	this.DoSomethingLong($"btnParallel_Click_00{t}");
	});

Parallel.ForEach(new int[]{0,1,2,3,4},t=>{
		this.DoSomethingLong($"btnParallel_Click_00{t}");
	});

//也可以控制最大线程数量,比方说最大能用3个线程
ParallelOptions options = new ParallelOptions()
{
	MaxDegreeOfParallelism = 3;
}

Parallel.ForEach(new int[]{0,1,2,3,4},options,(t,state)=>{
	this.DoSomethingLong($"btnParallel_Click_00{t}");
	state.Stop();//结束全部的
	state.Break();//停止当前的
	});
```

### Thread的异常
1，多线程里面的异常是会被吞掉的，外层是Catch不到线程里面的异常的
2，除非让主线程WaitAll才能拿到这个线程
3，建议多线程里面的异常自己在Action里面处理好，比方说加try catch

```c#
TaskFactory taskFactory = new TaskFactory();
List<Task> taskList = new List<Task>();

try
{
	for(int i=0; i< 20; i++)
	{
		string name = string.Format($"btnThreadCore_Click_{i}");
		Action<object> act = t =>{
			try
			{
				Thread.Sleep(2000);
				if(t.ToString().Equals("btnThreadCore_Click_11"))
				{
					throw new Exception(string.Format($"{t}执行失败"));
				}
				Console.WriteLine("{0}执行成功",t);
			}
			//如果这一段的catch拿掉，外层是catch不到线程里面的异常的
			//catch(Exception ex)
			//{
			//	Console.WriteLine(ex.Message);
			//}
		};
		taskList.Add(taskFactory.StartNew(act,name));
	}
	//要抓到里面的异常需要这么做：
	Task.WaitAll(taskList.ToArray());
}
catch(AggregateException aex)
{
	foreach(var item in aex.InnerExceptions)
	{
		Console.WriteLine(item.Message);
	}
}
catch(Exception ex)
{
	Console.WriteLine(ex.Message);
}

```

## 线程取消
1，线程取消不是操作线程，而是操作共享变量（多个线程都能访问到的东西，变量/数据库的数据/标识）
2，每个线程在执行的过程中，要经常去查看一下这个信号量，然后自己结束自己
3，线程不能被别人终止，只能自己干掉自己
4，延迟是少不了的 
5，<span style="color: red">CancellationTokenSource可以在cancel之后，取消没有启动的任务</span>
```c#
TaskFactory taskFactory = new TaskFactory();
List<Task> taskList = new List<Task>();

CancellationTokenSource cts = new CancellationTokenSource();
try
{
	for(int i =0; i<40; i++)
	{
		string name = string.Format("btnThreadCore_Click{0}",i);
		Action<object> act = t =>
		{
			try
			{
				Thread.Sleep(2000);
				if(t.ToString().Equals("btnThreadCore_Click_11"))
				{
					throw new Exception($"{t}执行失败");
				}
				//检查信号量，初始化的实会是false
				if(cts.IsCancellationRequested)
				{
					Console.WriteLine("{0} 放弃执行",t);
				}
				else
				{
					Console.WriteLine("{0} 执行成功",t);
				}
			}
			//在线程内部执行try catch的检查
			catch(Exception ex)
			{
				//只要cts.Cancel发出来了，还没有执行的线程就不会再执行了，这是.	NET框架帮忙做的
				cts.Cancel();
				Console.WriteLine(ex.Message);
			}
		};
		taskList.Add(taskFactory.StartNew(act, name, cts.Token));
	}
}
catch(AggregateException aex)
{
	foreach(var item in aex.InnerExceptions)
	{
		Console.WriteLine(item.Message);
	}
}
catch(exception ex)
{

	Console.WriteLine(ex.Message);
}

Task.WaitAll(taskList.ToArray());

```

## 多线程临时变量

如果只是这样写，出来的结果会是5个5
为什么呢？
因为BeginInvoke不占用主线程，在它loop的时候主线程已经执行到下面的代码去了，再启动子线程的时候，i已经遍历到5了
```c#
for(int i = 1; i< 5; i++)
{
	new Action(() =>
	{
		Thread.Sleep(100);
		Console.WriteLine(i);
	}).BeginInvoke(null,null);
}
```
{%asset_img param.png %}
但是如果你加一个变量
每次启动子线程的时候，k都是独立不同的
```c#
for(int i = 1; i< 5; i++)
{
	int k = i;
	new Action(() =>
	{
		Thread.Sleep(100);
		Console.WriteLine(k);
	}).BeginInvoke(null,null);
}
```
{%asset_img param2.png %}

## 线程安全问题 lock
**<span style="color: red">注意！！只要用了多线程，还有for循环，最好就是在for里面定义一个新的变量与i对应，防止线程变量问题</span>**

多个线程操作同一个变量，都有可能发生线程不安全问题
线程内部不佛念故乡的东西是安全的
CancellationToken, ManualResetEvent这类的都是安全的
```c#
int TotalCount;
var IntList = new List<int>();
for(int i=0; i<10000;i++)
{
	int newI = i;
	//要注意，这里并不是说起10000个线程，因为用taskFactory其实用的还是线程池里面的，不会起这么多线程的
	taskList.Add(taskFactory.StartNew(()=>
	{
		this.TotalCount += 1;//多个线程同时操作，有些操作可能会被覆盖，所以有可能是10000，也可能<10000
		IntList.Add(newI);
	}));
}
Task.WaitAll(taskList.ToArray());
Console.WriteLine(this.TotalCount);
Console.WriteLine(IntList.Count());
```
结果却是如图：
{%asset_img safety.png %}

为什么呢？
对于这个this.TotalCount,会有多个线程对它同时加1，所以有时候操作被覆盖了;
IntList集合也是不安全，引用类型，同时多个线程对它访问，也会有可能被覆盖的;

### 怎么样让其正确？
方法一，lock，用变量来保证，**但是lock的方法块里面是单线程的**,所以一定要保证不需要lock的逻辑放在lock之外

如果每个实例想要单独的锁定，那么就用一个**private object**，这样只有实例了你这个类的才能用

1，**不要用lock(this),因为只要有一个人锁定了，别的地方想要用这个变量，就会都被锁定**
2，**不要用lock("12345"),这种是享元模式的内存分配，如果有另外一个变量string b = "12345"，那么会锁定这个变量b**
3，如果需要全局唯一的锁，那么推荐的做法是`private static readonly object XX_Lock=new object();`,private保证不让别人访问，只能内部访问，static保证全局只有一个，readonly保证不会在lock内部被更改
4，如果想要实例唯一，用`private object YY_Lock = new object();`

```c#
private static readonly object btnThreadCore_Click_Lock = new object();
for(int i=0; i<10000;i++)
{
	int newI = i;
	//要注意，这里并不是说起10000个线程，因为用taskFactory其实用的还是线程池里面的，不会起这么多线程的
	taskList.Add(taskFactory.StartNew(()=>
	{
		//线程看到这会先检查有没有别的变量在用这个名为btnThreadCore_Click_Lock锁定，如果锁定了就会等待
		//这样就保证唯一时刻只有一个线程在访问
		lock(btnThreadCore_Click_Lock)
		{
			this.TotalCount += 1;
			IntList.Add(newI);
		}
		
	}));
}
```
方法二，让其没有冲突，从数据上隔离开，比方说这个线程访问前100个，另一个线程访问后面200个
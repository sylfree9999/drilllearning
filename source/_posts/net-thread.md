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
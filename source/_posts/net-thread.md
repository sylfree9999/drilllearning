---
title: net-thread
date: 2018-07-22 21:57:15
tags: [.NET, concept]
---
## Basic

1，	前台线程thread.Start();进程退出后还会继续执行，直到执行结束。
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

	//thread.Join();//做等待用的，将现在的线程与主线程合并
}
```

用Thread实现回调且不卡界面
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

Thread实现带返回值的且不卡界面
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
---
title: net-async
date: 2018-07-17 12:16:40
tags: [.NET, concept]
---

## Basic

异步多线程：多线程是说的CLR线程，异步是说IO线程
要用异步多线程必须要用Delegate委托
```c#
private void btnAsync_Click(object sender, EventArgs e)
{
	//同步调用，必须DoSomethingLong结束后才会走下一步
	Action<string> act = new Action<string>(this.DoSomethingLong);
	act.Invoke("this.DoSomethingLong");

	//异步调用，会启动一个线程；现象是直接进入下一行，不会等待
	act.BeginInvoke("this.DoSomethingLong",null,null);
}

private void DoSomethingLong(string name)
{
	Console.WriteLine($"********DoSomethingLong Start {Thread.CurrentThread.ManagedThreadId.ToString("00")}");
	long lResult = 0;
	for(int i=0; i<1000000;i++)
	{
		lResult += i;
	}
	Thread.Sleep(2000);

	Console.WriteLine($"********DoSomethingLong End {Thread.CurrentThread.ManagedThreadId.ToString("00")}");
}
```
<!--more-->

## 异步多线程如何控制顺序

回调，这种方法十分稳定，一定会在委托执行完后再执行
```c#
private void btnAsync_Click(object sender, EventArgs e)
{
	Console.WriteLine($"***********btnAsync_Click Startc {Thread.CurrentThread.ManagedThreadId.ToString("00")}");

	Action<string> act = this.DoSomethingLong;

    //回调方法，一定会在DoSomethingLong之后调用
	AsyncCallback callback=ar => Console.WriteLine($"这里是BeginInvoke调用完成之后才执行的{Thread.CurrentThread.ManagedThreadId.ToString("00")}");
	//para asyncState会被保存在iAsyncResult的asyncState参数中
	IAsyncResult iAsyncResult = act.BeginInvoke("btnAsync_Click",callback,"asyncState");
}
```

等待
1, while这里是主线程来做的，所以会咯界面
2, EndInvoke可以拿到之前委托的结果 
```c#
private void btnAsync_Click(object sender, EventArgs e)
{
	Console.WriteLine($"***********btnAsync_Click Startc {Thread.CurrentThread.ManagedThreadId.ToString("00")}");

	Action<string> act = this.DoSomethingLong;
	//para asyncState会被保存在iAsyncResult的asyncSta te参数中
	IAsyncResult iAsyncResult = act.BeginInvoke("btnAsync_Click",null,null);
	int i=1;
	//1 卡界面，主线程会等待
	//2 边等待边做事
	//3 有误差，会等待200毫秒
	while(!iAsyncResult.IsCompleted)
	{
		if(i < 10)
		{
			Console.WriteLine("文件上传{0}%...请等待",i++ * 10);
		}
		else
		{
			Console.WriteLine("马上结束");
		}
		Thread.Sleep(200);
		Console.WriteLine("这里是BeginInvoke调用完成之后才执行的");
	}

	 //另外一种方式可以让异步变同步,不会有误差的，一直等待任务完成，这种方式不能在等待的过程中做别的事情
	iAsyncResult.AsyncWaitHandle.WaitOne();
	//最多等待1000毫秒，可以做超时控制
	iAsyncResult.AsyncWaitHandle.WaitOne(1000);

	{
		Func<int,string> func = i => i.ToString();
		iAsyncResult iAsyncResult = func.BeginInvoke(DateTime.Now.Year, ar=>{
				//这个就是传入的“Lalala”
				Console.WriteLine(ar.AsyncState);
			},"Lalala");
		//这个result就是func的返回值
		string result = func.EndInvoke(iAsyncResult);
	}

	//对于每个异步调用，只能有一个EndInvoke
	{
		Func<int,string> func = i => i.ToString();
		iAsyncResult iAsyncResult = func.BeginInvoke(DateTime.Now.Year, ar=>{
				string resultIn = func.EndInvoke(ar);
				//这个就是传入的“Lalala”
				Console.WriteLine($"This is {ar.AsyncState} 的异步调用结果 {resultIn}");
			},"Lalala");
		//这个result就是func的返回值
		
	}
}
```
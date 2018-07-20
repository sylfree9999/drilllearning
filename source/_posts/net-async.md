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
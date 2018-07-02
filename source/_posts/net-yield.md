---
title: net-yield
date: 2018-06-28 10:46:18
tags: [net, concept]
---
迭代器
<span style="color: red">注意！yield是写在while里面的，且返回的是result!不是results!</span>

yield 是一个状态机，只有在真正调用的时候才会进到方法里面调用
```c#
//一次性把所有数据都计算好
public IEnumerable<int> CommonMethod()
{
	List<int> results = new List<int>();
	int counter = 0;
	int result = 1;

	while(counter++ < 10)
	{
		Thread.Sleep(1000);
		Console.WriteLine($"获取{counter}次数据");
		result = result * 2;
		results.Add(result);
	}
	return results;
}

//按需获取 
public IEnumerable<int> YieldMethod()
{
	int counter = 0;
	int result = 1;
	while(counter++ < 10)
	{
		Thread.Sleep(1000);
		Console.WriteLine($"获取{counter}次数据");
		result = result * 2;
		yield return results;
	}
}

//caller
IEnumerable<int> intListCommon = show.CommonMethod();//返回的是最终的结果
IEnumerable<int> intListYield = show.YieldMethod();//这个时候返回的是一个状态机，不是最终的结果


//只有在调用item的时候，才会真正走进去，且每次循环后是从while开始的！
foreach(var item in intListYield)
{

}
```

## linq

.NET里面linq其实也是用的yield方式实现的，只有在真正使用的时候才会去执行逻辑代码

比方说
```c#
var itemList = studentList.Where(x=>x.Age < 30);
```
但是如果用了ToList()，就会之u姐去执行逻辑代码
```c#
var itemList2 = studentList.Where(x=>x.Age>30).ToList();
```


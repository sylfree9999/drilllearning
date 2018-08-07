0---
title: net-attribute
date: 2018-06-21 17:09:23
tags: [.NET, concept]
---

## 概念
Attribute其实是为了生成MetaData的
Attribute就是一个继承于Attribute的类

```c#
public class CustomAttribute: Attribute{

	public CustomAttribute(){
		Console.WriteLine("This is constructor of CustomAttribute");
	}

	public CustomAttribute(string remark){

	}

	public string Remark{get;set;}
	public string Description{get;set;}

	public void Show(){
		Console.Writeline($"This is {this.GetType().Name}");
	}
}

//也可以间接继承于Attribute
public class CustomChildAttribute: CustomAttribute{

}
```

<!-- more -->

Attribute默认情况下不能重复修饰

Attribute可以放在类，方法，属性，字段等很多地方，在`[AttributeUsage(AttributeTargets.All, AllowMultiple=False)]`中设置

`[Custom] = [Custom()]`,代表默认用无参构造函数
`[Custom("This is a student", Remark="123", Description="567")]`  构造函数的时候顺便把属性都赋值


## 使用
特性在你不显式调用的时候，一点用都没有
特性是通过反射来使用的
```c#
///
特性编译后是metadata，只有反射才能使用
///
public class PeopleManager
{
	public static void Manage(Student student){
		
		Type type = student.GetType();
	
		//type.GetCustomAttributes会实例化这个特性
		if(type.IsDefined(typeof(CustomAttribute),true)){
			object item = type.GetCustomAttributes(typeof(CustomAttribute),true)[0];
		    CustomAttribute attribute = item as CustomAttribute;
		    attribute.Show();
		}
		
		foreach(var item in type.GetConstructors()){
			if(item.IsDefined(typeof(CustomAttribute),true)){
				object ii = item.GetCustomAttributes(typeof(CustomAttribute),true)[0];
			}
		}

		MethodInfo method = type.GetMethod("Answer");
		if(method.IsDefined(typeof(CustomAttribute),true)){
			object item = method.GetCustomAttributes(typeof(CustomAttribute),true)[0];
		}

		foreach(var item in method.GetParameters()){

		}

		if(method.ReturnParameter.IsDefined(typeof(CustomAttribute),true)){

		}


		student.Study();
		student.Answer("SS");
	}
}
```

## 实战
```c#
public class Student{

	[AuthoritytAttribute(Remark="Answer Questions")]
	[Custom]
	[return: Custom]
	public string Answer([Custom]string name){
		return $"This is {name}"
	}
}

public class AuthoritytAttribute:Attribute{
	public string Remark {get;set;}
	public bool IsLogin(){
		return new Random().Next(100,200) > new Random().Next(100,199);
	}
}

public class PeopleManager
{
	public static void Manage(Student student){

		//Attribute可以增加功能，也可以多一点信息（Remark)
		Type type = typeof(Student);
		MethodInfo method = method.GetMethod("Answer");
		if(method.IsDefined(typeof(AuthoritytAttribute),true)){
			object item = type.GetCustomAttributes(typeof(AuthoritytAttribute),true)[0];
			AuthoritytAttribute attribute = item as AuthoritytAttribute;
			Console.WriteLine(attribute.Remark);
			// if(DateTime.Now > DateTime.Now.AddDaus(1))//实际上可以使用HttpContext.Current.Cookie/Session来检查用户登陆信息
			// {
			// 	throw new Exception("Not authorized"); //redirect to login page
			// }

			//将权限认证放到了attribute中
			if(!attribute.IsLogin()){
				throw new Exception("Not authorized");
			}

		}
		student.Answer("SS");
	}
	
}

//Caller
class Program{
	static void Main(string[] args){
		Student studnet = new Student();
		//这个方法调用是不会call AuthorityAttribute的
		student.Answer("SS");

		//这样写才会支持AuthorityAttribute
		PeopleManager.Manage(student);
	}
}
```

实例
```c#
[AttributeUsage(AttributeTargets.Enum | AttributeTargets.Field)]
public class RemarkAttribute: Attribute
{
	public RemarkAttribute(string remark)
	{
		this.Remark = remark;
	}

	public string Remark{get;set;}
}

[Remark("用户状态")]
public enum UserState
{
	[Remark("正常")]
	Normal = 0,
	[Remark("冻结")]
	Forzen = 1,
	[Remark("删除")]
	Deleted = 2
}

public class RemarkExtend
{
	//扩展方法
	public static string GetRemark(this Enum enumValue){
		Type type = enumValue.GetType();
		FieldInfo field = type.GetField(enumValue.ToString());
		if(field.IsDefined(typeof(RemarkAttribute),true)){
			RemarkAttribute remarkAttribute = (RemarkAttribute)field.GetCustomAttribute(typeof(RemarkAttribute));
		return remarkAttribute.Remark;
		}else{
			return enumValue.ToString();
		}
		
	}
}

//caller
public void Main(string[] args)
{
	UserState.Deleted.GetRemark();
}
```
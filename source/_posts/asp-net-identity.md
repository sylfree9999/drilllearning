---
title: ASP.NET Identity 原理
date: 2018-03-25 21:09:31
tags: [ASP.NET, Identity, Concept]
---

转自:
[MVC5 - ASP.NET Identity登录原理 - Claims-based认证和OWIN](http://www.cnblogs.com/jesse2013/p/aspnet-identity-claims-based-authentication-and-owin.html)

实现登录实际上只有简单的三行代码
```
private IAuthenticationManager AuthenticationManager
{
	get{
		return HttpContext.GetOwinContext().Authentication;
	}
}

private async Task SignInAsync()
{
	//1.	利用ASP.NET Identity获取用户对象
	var user = await UserManager.FindAsync("UserName","Password");
	//2.	利用ASP.NET Identity获取Identity对象
	var identity = await UserManager.CreateIdentityAsync(user, DefaultAuthenticationTypes.ApplicationCookie);
	//3.	将上面拿到的identity对象登录
	AuthenticationManager.SignIn(new AuthenticationProperties(){
		IsPersistent = true
		}, identity);
}
```

`CreateIdentityAsync`返回的是一个ClaimsIdentity，这又是什么？

## Claim-baised Identity

Claim-based 认证将Authentication 和 Authorization 与login 分开，将Authentication 和 Authorization 拆分为另外的web服务。

主要特点：
+	将认证与授权拆分成独立的服务
+	服务调用者不需要关注如何去认证
+	如果用户成功登陆，认证服务会返回令牌
+	服务调用者从令牌中读取所需信息，诸如用户名以及角色信息等

例如QQ登陆：

1.	用户到网站访问一个需要登录的页面
2.	网站检测到用户没有登录，返回一个跳转到QQ的登录页响应（**302**指向QQ登录页面的地址并加上一个返回的链接页面，通常为returnUrl=)
3.	用户被跳转到指定的QQ登录页
4.	用户在QQ登录页面上输入用户名和密码，QQ会在自己的数据库中查询，一旦登陆成功，会返回一个跳转到我们站点的响应（**302指向我们的网站页面**)
5.	用户被跳转到我们网站的一个检测登录的页面，我们可以拿到用户的身份信息，建立**ClaimsPrincipal**和**ClaimsIdentity**对象，生成**cookie**等
6.	我们再把用户带到指定的页面，也就是returnUrl，那是用户登录前最后一次访问的页面

{% asset_img qq-claim-based-login.png %}

## ClaimsIdentity, ClaimsPrincipal

ClaimsIdentity和ClaimsPrincipal继承了接口IIdentity和IPrincipal

**Identity**
```c#
public interface IIdentity
{
	string AuthenticationType { get; }
	bool IsAUthenticated { get; }
	string Name { get; }
}
```

**IPrincipal**
IPrincipal代表了一个安全**上下文**，这个上下文对象包含了上面identity以及一些角色和组的信息，每一个线程都会关联一个Principal的对象，但是这个对象是<span style="background-color: #FFFF00">属性进程或者AppDomain级别的</span>.

[Ref: What is the idea behind IIdentity and IPrincipal in .NET
](https://stackoverflow.com/a/27108829/4336416)

`IIdentity` is just used for the user's authenticated identity, regardless of what roles they may have.

`IPrincipal` is used to combine a user's identity with the `authorized` roles they have in a given security context.

For example, you can use a third-party login provider, like Facebook or Google, to get the user's identity, but you will not get a principal from those providers, as they don't provide any roles. You can use your own application or a third-party role-based authorization provider to apply roles to , say, a `FacebookIdentity` or `GoogleIdentity`. A different application can expect a different principal, with its own roles , but still use the same identity as in another application

例子：
```c#
public class HomeController : Controller
{
	[Authorize(Role = "Users")]
	public ActionResult Index(){
		return View();
	}

	[Authorize(Roles = "Managers")]
	public ActionResult Manager()
	{
		return View();
	}
}
```

登录, 在global.asax中添加了Application_AuthenticateRequest方法，**就是每次MVC要对用户进行认证的时候都会进到这个方法里面**，然后就神奇的把用户给登陆了。

```c#
protected void Application_AuthenticateRequest()
{
	var claims = new List<Claim>();
	claims.Add(new Claim(ClaimTypes.Name, "Zhang san"));
	claims.Add(new Claim(ClaimTypes.Role, "Users"));
	var identity = new ClaimsIdentity(claims, "MyClaimsLogin");

	ClaimsPrincipal principal = new ClaimsPrincipal(identity);
	HttpContext.Current.User = principal;
}
```

最后结论，我们讲了ClaimsIdentity什么的，讲了这么多和今天的主题有嘛关系？我们上面说ASPNET Identity登录有三句话，第一句话可以略过，第二句话就是我们上面讲的。

```
var identity = await UserManager.CreateIdentityAsync(user, DefaultAuthenticationTypes.ApplicationCookie);
```

UserManager实际上只是为我们创建了一个ClaimsIdentity的对象，还是通过我们自己从数据库里面取出来的对象来创建的，它也就干了那么点事，一层小小的封装而已。不要被后面的DefaultAuthenticationTypes.ApplicationCookie吓到了，这里还没有和cookie扯上半点关系，这就是一个字符串常量，和我们上面自己定义的MyClaimsLogin是没有区别的。

到这里，我想算是把登录代码的第二句话讲完了，讲清楚了，那么我们来看看第三句话，也就是最后一句，其实它才是登录的核心，第二句只是创建了一个ClaimsIdentity的对象。

```
private IAuthenticationManager AuthenticationManager
{
	get { return HttpContext.GetOwinContext().Authentication; }
}
AuthenticationManager.SignIn(new AuthenticationProperties() { IsPersistent = true }, identity);
```

IAuthenticationManager 在`Microsoft.Owin.Security`命名空间下，而这个接口是定义在Microsoft.Owin.dll中。

##Owin

OWIN目标是解耦服务器和应用，这里面的服务器主要是指web服务器，比如说IIS等，那么是如何做到的呢？

**解耦服务器与应用程序**
首先需要复习ASP.NET或者<span style="background-color: #FFFF00">IIS集成模式管道模型</span>，也就是说一个http请求在进入IIS之后（IIS7.0以上）一直到返回response这中间所经历的步骤。

{% asset_img netpipe.png %}
{% asset_img mvc-request-lifecycle.png %}
[Ref: A Detailed walkthrough of ASP.NET MVC Request lifecycle](https://www.codeproject.com/Articles/1028156/A-Detailed-Walkthrough-of-ASP-NET-MVC-Request-Life)

我们可以开发自己的HttpModule(比方说是MyFormsModules)去注册这些事件，然后做相应的处理。比方说`FormsAuthenticationModule`就是注册了`AuthenticateRequest`事件，然后在这里去检查用户的cookie信息来判断用户是否登录了，这就是一个典型的**应用程序与服务器之间的交互**问题，而这些事件最后是被IIS触发的,我们是通过web.config把我们自定义的http module注册进了IIS，但是**如果我们的网站不运行在IIS了，我们自己开发的这些HTTP module还能用么？**

另一个，我们`Request`和`Response`都是封装在`HttpContext`里面的，而这些信息从IIS里面来，最后也是交给IIS，如果web服务器不是IIS，那么这些信息从哪里获取呢？

所以能够看出来，应用程序和服务器之间的耦合很大。我们不能够轻易换掉其中任何一个。

## OWIN如何做到解耦

它通过将服务器与应用程序之间的交互归纳为一个方法签名，称之为"应用程序代理(application delegate)"

```
AppFunc = Func<IDictionary<string, object>, Task>;
```

在一个基于Owin的应用程序中的每一个组件都可以通过这样的一个代理来与服务器进行交互。 这们这里的交互其实是与服务器一起来处理http request，比如说ASP.NET管理模型中的那些事件，认证，授权，缓存等等，原先我们是通过自定义的http module，在里面拿到包含了request和response的HttpContext对象，进行处理。而现在我们能拿到的就是一个Dictionary。

可是别小看了这个Dictionary，我们所有的信息比如Application state, request state，server state等等这些信息全部存在这个数据结构中。这个dictionary会在Owin处理request的管道中进行传递，没错有了OWin之后，我们就不再是与ASP.NET 管道打交道了，而是OWin的管道，但是这个管道相对于ASP.NET 管道而言更灵活，更开放。

这个字典在OWin管道的各个组件中传输时，你可以任意的往里面添加或更改数据。 OWin默认为我们定义了以下的数据：
{% asset_img owin-defaults.png %}

有了这些数据以后，我们就不需要和.NET的那些对象打交道了，比如说ASP.NET MVC中的HttpContextBase, 以及WEB API  中的HttpRequestMessage和HttpResponseMessage。我们也不需要再考虑system.web 这个dll里的东西，我们只需要通过OWin就可以拿到我们想要的信息，做我们想做的事了。而OWin，它本身和web服务器或者IIS没有任何关系。

## Forms Authentication

在Forms认证中我们检测完用户名和密码之后，只需要调用小面的代码就会为我们创建用户cookie.
```
FormsAuthentication.SetAuthCookie("Jesse", false);
```

然后FormsAuthenticationModule(**这就是一个HTTP Module**)会在ASP.NET管道的AuthenticateRequest阶段去检查是否有这个cookie，并把它转换成我们需要的Identity对象，这样的话我们就不需要每一次都让用户去输入用户名和密码了。所以登录过程如下：
1。	用户在没有登录的情况下访问了我们需要登录的页面
2.	FormsAuthenticationModule检查不到用户身份的cookie，没有生成identity对象，HttpContext.User.IsAuthenticated = false
3.	在ASP.NET 管道 的Authroize 授权阶段，将用户跳转到登录页面
4.	用户输入用户名和密码点击提交
5.	我们检查用户名和密码，如果正确，就调用FormsAuthentication.SetAuthCookie方法生成登录cookie
6.	用户可以正常访问我们需要登录的页面了
7.	用户再次访问我们需要登录的页面
8.	FormsAuthenticationModule检查到了用户身份的cookie，并生成identity对象，HttpContext.User.IsAuthenticated = true
9.	ASP.NET 管道的 Authroize授权阶段，HttpContext.User.IsAuthenticated=true，可以正常浏览
10. 7,8,9循环

**Forms Authentication有以下不足**

1.	用户名直接暴露在cookie中，需要额外的手段去将cookie加密
2.	不支持claim-based认证

我们上面Forms的登录过程，对于OWin登录来说同样适用。我们在上面讲ASP.NET Identity登录第二句话的时候已经拿到了ClaimsIdentity，那么我们接下来要看的问题就是如何借助于IAuthenticationManager 去登录？ FormsAuthenticationModuel没有了，谁来负责检测cookie？您请接着往下看！

## MVC5默认的StartUp配置类

VS除了为我们引用OWin相关dll，以及移除FormsAuthenticationModule以外，还为我们在App_Start文件夹里添加了一个Startup.Auth.cs的文件。
```
public partial class Startup
{
	public void ConfigureAuth(IAppBuilder app)
	{
		app.UseCookieAuthentication(new CookieAuthenticationOptions
			{
				AuthenticationType = DefaultAuthenticationTypes.ApplicationCookie,
				LoginPath = new PathString("/Account/Login"),
				CookieSecure = CookieSecureOption.Never,
			});
	}
}
```

UseCookieAuthentication是一个IAppBuilder的扩展方法，定义在Microsoft.Owin.Security.Cookies.dll中
```
public static IAppBuilder UseCookieAuthentication(this IAppBuilder app, CookieAuthenticationOptions options)
{
	if(app == null)
	{
		throw new ArgumentNullException("app");
	}
	//添加OWIN middleware组件到OWIN管道
	app.Use(typeof(CookieAuthenticationMiddleware), app, options);
	//为前面添加的Middleware指定在IIS管道的哪个阶段执行
	app.UseStageMarker(PipelineStage.Authenticate);
	return app;
}
```

PipelineStage这个枚举定义与IIS管道里的那些顺序同，也是我们Http Module里面可以绑定的那些事件：
```
public enum PipelineStage
{
	Authenticate = 0,
	PostAuthenticate = 1,
	Authorize = 2,
	PostAuthorize = 3,
	ResolveCache = 4,
	PostResolveCache = 5,
	MapHandler = 6,
	PostMapHandler = 7,
	AcquireState = 8,
	PostAcquireState = 9,
	PreHandlerExecute = 10,

}
```

也就是说我们上面注册的CookieAuthenticationMiddleware会在AuthenticaRequest 阶段执行。而它就是真正生成cookie以及读取cookie的那只背后的手。
顺便回顾一下如何在http module中为Authenticate绑定事件：
```
public class MyModule : IHttpModule
{
	public void Init(HttpApplication context)
	{
		context.AuthenticateRequest += ctx_AuthRequest;
	}

	void vtx_AuthRequest(object sender, EventArgs e)
	{

	}
}
```

.

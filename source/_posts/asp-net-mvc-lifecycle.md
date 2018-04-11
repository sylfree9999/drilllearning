---
title: ASP.NET MVC Request Life Cycle
date: 2018-03-26 10:15:43
tags: [concept]
---

[Ref A Detailed Walkthrough of ASP.NET MVC Request Life Cycle](https://www.codeproject.com/Articles/1028156/A-Detailed-Walkthrough-of-ASP-NET-MVC-Request-Life)

This is mainly for **Page Life Cycle** other than **Application Life Cycle**.
A typical **Application Life Cycle** contains **Application Start** and **Application End events** while **Http Life Cycle** is something which is repeated for every request.

## MVC Request Life Cycle
{% asset_img mvc-life-cycle.png %}

### URL Routing Module

The incoming request from **IIS pipeline** is handed over to URL Routing module which analyses the request and looks up **Routing table** to figure out which controller the incoming request maps to.

Routing table is a static container of routes defined in MVC application with corresponding controller action mapping. If the route is found in the routing table `MVCRouteHandler` executes and bring s the instance of `MVCHttpHandler`.

`MVC handler` begins initializing and executing controller. The `MVCHttpHandler` also takes of converting route data into concrete controller that is capable of serving the request. `MVC handler` does all this with the help of MVC Controller factory and activator which are responsible for creating an instance of the controller. <span style="background-color: #FFFF00">This is also the place where the Dependency Injection is performed if the application has been designed to invoke parameterized controller constructor and satisfy its dependencies</span>.

After the controller instance is created **the next major step is to find and execute the corresponding action**. A component called ActionInvoker finds and executes the action defined in routing table. Before the action method is called model bindings takes place which maps data from http request to action method parameters. After the model binding, action filters are invoked which includes OnActionExecuting filter. This is followed by action execution and Action Executed filter execution and finally preparing Action Result.

Once the Action method has been finished executing the next step is Result execution. MVC separates the action declaration from Result execution. If the Result from action execution is view, then depending upon configuration, ASPX or Razor view engine will be called to find and render the html view as a response of http request. If the result was not view then it’s passed as-is to http response.

## Application Life Cycle

MVC application life cycle contains two application level events that are associated with start and end events of the application. Application start fires **when the application is brought to life by a very first request** to the application. Application end event is fired **when application has been shut down**.

It’s important to understand application life cycle events to get a better understanding on how MVC life cycle starts. So far we have seen that URL Routing module is the starting point for MVC application that has a collection of predefined routes to map from. Now, the question here is **how does URL routing handler gets this information from**? The answer is simple, using Application start event. MVC applications provide these events in Global.asax file which contains all the application level events. All the prestart things are managed in the application start event.

MVC Application_Start event is:

+	An event that fires when first request is received.
+	Can be used to **run initial configuration and settings code**
+	The event takes care of **registering all areas of MVC application, installing global filters, adding routes and bundles**.

## Register Routes

Since Application_start event is the first event that gets called when application receives its very first request, **all the pre application tasks like routing takes place here**.

As you see in the diagram below ResolveRequestCache needs to know the routes to choose from, and this needs to have static route collection already created.

{% asset_img register-routes.png %}

## HttpHandlers
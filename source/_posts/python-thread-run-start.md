---
title: python-thread-run-start
date: 2018-05-30 15:27:37
tags: [concept, python]
---

## start()

>	Start the thread's activity.
	It must be called at most once per thread object. It arranges for the object's **run()** method to be invoked in a separate thread of control.
	This method will raise a RuntimeError if called more than once on the same thread object.

	它安排对象在另一个单独的线程中调用run()方法，而不是当前所出的线程

## run()

>	Method representing the thread's activity.
	You may override this method in a subclass. The standard run() method invokes the callable object passed to the object's constructor as the target argument.
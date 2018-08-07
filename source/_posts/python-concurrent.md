---
title: python-concurrent
date: 2018-08-07 16:05:05
tags: [python, concept]
---
## 全局解释器锁GIL
1，GIL是一个全局排他锁，同一时刻只有一个线程在运行，就类似于Python是个单线程的程序
2，multiprocessing库很大程度上是为了弥补GIL低效的缺陷，它完整复制了一套thread所提供的接口方便迁移，唯一不同的是它使用了多进程而不是多线程，所以每个进程有自己的独立的GIL，因此不会出现进程间的GIL争抢
3，多进程的fork操作，调用一次返回两次，操作系统会自动把当前进程（称为父进程）复制了一份（作为子进程），然后分别在父进程和子进程内返回。子进程永远返回0，而父进程返回子进程的ID。子进程只需要调用`getppid()`就可以拿到父进程的ID
```python
import os

print('Process (%s) start...' % os.getpid())
pid = os.fork()
if pid == 0:
	print("Child Process {0}, Parent Process {1}".format(os.getpid(), os.getppid()))
else:
	print("Parent Process is me {0}, my child process is {1}".format(os.getpid(),pid))
```
multiprocessing
```python
from multiprocessing import Process
import time

def f(n):
	time.sleep(1)
	print n*n

if __name__ == "__main__":
	for i in range(10):
		p = Process(target = f, args = [i,])
		p.start()
```

## 进程间通信Queue
1，Queue是多进程安全的队列，可以实现多进程之间的数据传递
2，Queue.qsize() 返回队列的大小  
	Queue.empty() 如果队列为空，返回True,反之False  
	Queue.full() 如果队列满了，返回True,反之False 
	Queue.get([block[, timeout]]) 获取队列，timeout等待时间  
	Queue.get_nowait() 相当Queue.get(False) 
	非阻塞 Queue.put(item) 写入队列，timeout等待时间  
	Queue.put_nowait(item) 相当Queue.put(item, False)
```python
from multiprocessing import Process, Queue
import time

def write(q):
	for i in ['A','B','C','D','E']:
		print('Put {0} to queue'.format(i))
		q.put(i)
		time.sleep(0.5)

def read(q):
	while True:
		v = q.get(True)
		print('Get {0} from queue'.format(v))

if __name__ == '__main__':
	q = Queue()
	pw = Process(target = write, args=(q,))
	pr = Process(target = read, args=(q,))
	pw.start()
	pr.start()
	pw.join()
	pr.join()
	pr.terminate()
```
## 进程池Pool
1，用于批量创建子进程，可以灵活控制子进程的数量
```python
from multiprocessing import Pool
import time

def f(x):
	print x*x
	time.sleep(2)
	return x*x

if __name__ == '__main__':
	'''定义启动进程的数量'''
	pool = Pool(processes = 5)
	res_list = []

	for i in range(10):
		'''以异步并行的方式启动进程，如果要同步等待的方式，可以在每次启动进程之后调用res.get()方法，也可以是用Pool.apply'''
		res = pool.apply_async(f, [i,])
		print('-----------:',i)
		res_list.append(res)
	pool.close()
	pool.join() #强制等待所有进程运行完毕
	for r in res_list:
		print("result: ",(r.get(timeout = 5)))

#结果
'''
ubuntu@bosch-shiny1:~$ python multiPython.py 
-----------: 0
0
-----------: 1
-----------: 2
-----------: 3
-----------: 4
-----------: 5
-----------: 6
-----------: 7
-----------: 8
-----------: 9
1
4
9
16
25
36
49
64
81
result:  0
result:  1
result:  4
result:  9
result:  16
result:  25
result:  36
result:  49
result:  64
result:  81
'''
```

## 多进程与多线程对比
1，主要区别就在于线程之间可以共享进程的资源，而进程是独立的
2，由于进程之前是互相独立的，所以结果会是
```python
from multiprocessing import Process
import threading
import time
lock = threading.Lock()

def run(info_list,n):
	lock.acquire()
	info_list.append(n)
	lock.release()
	print("{0}\n".format(info_list))

if __name__ == '__main__':
	info = []
	for i in range(10):
		p = Process(target=run, args=[info,i])
		p.start()
		p.join()
	time.sleep(1)
	print('------------------------threading--------------------')
	for i in range(10):
		p = threading.Thread(target=run, args=[info,i])
		p.start()
		p.join()
```
结果为
```
[0]

[1]

[2]

[3]

[4]

[5]

[6]

[7]

[8]

[9]

------------------------threading--------------------
[0]

[0, 1]

[0, 1, 2]

[0, 1, 2, 3]

[0, 1, 2, 3, 4]

[0, 1, 2, 3, 4, 5]

[0, 1, 2, 3, 4, 5, 6]

[0, 1, 2, 3, 4, 5, 6, 7]

[0, 1, 2, 3, 4, 5, 6, 7, 8]

[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
```
如果想让multiprocessing也像多进程一样，可以用Queue
```python
from multiprocessing import Process,Queue
import time
import threading
lock = threading.Lock()

def run(queue,info_list,n):
        lock.acquire()
        while not queue.empty():
                value = queue.get(True)
                info_list.append(value)
        lock.release()
        if len(info_list) > 0:
                print('{0}\n'.format(info_list))

def foo(q,n):
        q.put(n)


if __name__ == '__main__':
        info = []
        q = Queue()
        for i in range(10):
                for j in range(1,i+1):
                        q.put(j)
                p = Process(target=run,args=[q,info,i])
                p.start()
                p.join()
```
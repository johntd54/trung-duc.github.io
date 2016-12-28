---
layout: post
title: "161214 - Python Multithreading"
date: 2016-12-14 16:43:55
categories: Python
---

# Guiding Questions

1. Does Python multithreading run the program simultaneously in multiple cores?
2. How to send/receive messages/notifications between threads?
3. What is the overview architecture of all components and their overall interactions with each other in multithreading?
4. What is the maximum number of threads in multithreading?

# Synchronizing Threads

* Thread synchronization uses locking mechanism, which can be activated by calling `threading.Lock()` method.
* Use `lock.acquire(blocking)` to force threads to run synchronously.
* Use `lock.release()` to release the lock when it is no longer required.
* Locking is useful to prevent the race condition.
* Some useful functions:

    - `threading.activeCount()`
    - `threading.currentThread()`
    - `threading.enumerate()`
    - `Thread.run()`: should be subclassed
    - `Thread.__init__()`: can be subclassed
    - `Thread.start()`
    - `Thread.join([time])`
    - `Thread.isAlive()`
    - `Thread.getName()`
    - `Thread.setName()`

# Nittygitties

* The variables in main thread (usually thread that Python interpreter was started) will be shared by all other threads. To avoid unintentional modification of those variables, use thread-local data, e.g. `mydata = threading.local(); mydata.x = 1;`
* Flag a thread daemon by setting daemon=True in constructor or directly setting `daemon` attribute. A daemon thread is a thread that will not stop Python from exitting.
* There might be "alien threads" created in Python, which are threads of control started outside the threading module (e.g. directly from C code).
* Can use `threading.Event` object to handle communication between threads. One thread signals an event and other threads wait for it.

# Answers

1. Does Python multithreading run the program in multiple cores?

    No. Threads are spawned in the same process, which share common memory resources. Moreover CPython (default Python interpreter) uses a Global Interpreter Lock to make sure that only one thread can access Python code at a time.

2. How to send/receive messages/notifications between threads?

    In Python, all threads access the same memory resources (from the same namespace). As a result, data (especially global data) can easily be accessed by all threads.



# Sources

https://www.tutorialspoint.com/python/python_multithreading.htm
https://pymotw.com/3/threading/
https://docs.python.org/3.5/library/threading.html
https://docs.python.org/3.5/library/multiprocessing.html
http://jessenoller.com/2009/02/01/python-threads-and-the-global-interpreter-lock/

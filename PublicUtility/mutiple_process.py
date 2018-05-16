#!/usr/bin/env python
#encoding: utf-8
'''
@summary: 多进程，和多线程的threading.thread用法非常类似
多进程multiprocessing 模块的使用与多线程threading 模块类似，multiprocessing 提供了本地和
远程的并发性，有效的通过全局解释锁(Global Interceptor Lock, GIL)来使用进程(而不是线程)。由于
GIL 的存在，在CPU 密集型的程序当中，使用多线程并不能有效地利用多核CPU 的优势，因为一个解释器
在同一时刻只会有一个线程在执行。所以，multiprocessing 模块可以充分的利用硬件的多处理器来进行
工作。它支持Unix 和Windows 系统上的运行
'''
import multiprocessing
import time

def a(name):
	print name
	time.sleep(3)

	print time.ctime()
def b(name):
	print name*2
	print time.ctime()

def invoke():
	threads = []
	threads.append(multiprocessing.Process(target=a,args=('aaa',)))
	threads.append(multiprocessing.Process(target=b,args=('bbb',)))
	threads.append(multiprocessing.Process(target=a, args=('ccc',)))

	for t in threads:
		t.start()

	for t in threads:
		t.join()

if __name__ =='__main__':
	invoke()

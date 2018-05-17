#/usr/bin/env python
#encoding: utf-8
'''
@summary: create a common way for threading class，主要例子为生产者消费者问题，线程间通信
@create by YQY at 2018-05-16
@change: 2018-05-17 add produce and consumer example
'''
import threading
import Queue
import random
import time


class MyThread(threading.Thread):
	def __init__(self,func,args):
		threading.Thread.__init__(self)
		self.func =func
		self.args = args
		self.lock = threading.Lock()  #线程锁，用于资源同步

	def run(self):
		# self.result = self.func(*self.args)
		self.func(*self.args)

	# def get_result(self):  #获取线程返回值
	# 	try:
	# 		return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
	# 	except Exception:

def use_product(queue, number):
	'''
	@summary: use product
	'''
	for i in range(number*10):
		try:
			result = queue.get(block=0)  # block不为0则是阻塞等待直到有新数据进入队列
			print 'use' + str(result) + str(time.ctime())
			time.sleep(random.randint(2,5))
		except Exception as e:
			print e

def produce_product(queue, number):
	'''
	@summary: produce product
	'''
	for i in range(number*5):
		i=random.randint(number,100)
		try:
			queue.put(i)
		except Exception as e:
			print e
		print 'product' + str(i) + str(time.ctime())
		time.sleep(random.randint(1,3))

if __name__ == "__main__":
	queue = Queue.Queue(10) #用于线程间安全的消息交换，最大size10，FIFO, 也可设置LIFO等
	funcs = [produce_product,use_product,produce_product,use_product]
	list_func = []

	for i in range(len(funcs)):
		t = MyThread(funcs[i],(queue,i+1))
		list_func.append(t)

	for func in list_func:
		func.start()

	for func in list_func:
		func.join()

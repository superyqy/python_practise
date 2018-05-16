#/usr/bin/env python
#encoding: utf-8
'''
@summary: create a common way for threading class
@create by YQY at 2018-05-16
'''
import threading
import Queue
import time


class MyThread(threading.Thread):
	def __init__(self,func,args,name=''):
		threading.Thread.__init__(self)
		self.func =func
		self.args = args
		self.name = name
		self.lock = threading.Lock()  #线程锁，用于资源同步

	def run(self):
		self.result = self.func(*self.args)

	def get_result(self):
		try:
			return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
		except Exception:
			return None
	
def get(name,value,queue):
	print "{0} is {1}".format(name,value)

	return queue.get()

def set(queue):
	queue.put(time.ctime())

if __name__ == "__main__":
	list = ['jack','dada']
	t_list = []
	queue = Queue.Queue(10) #用于线程间安全的消息交换，最大size10，FIFO, 也可设置LIFO等
	for name,value in list.items():
		t = MyThread(test,(name),test.__name__)
		t_list.append(t)

	for t in t_list:
		t.start()

	for t in t_list:
		t.join()
		print t.get_result()
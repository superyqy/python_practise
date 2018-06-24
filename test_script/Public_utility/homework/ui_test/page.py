#!/usr/bin/env python
#encoding: utf-8
'''
@summary: HTML page basic function
@author: YQY
@change: 2018-06-23 create script
'''

class Page(object):
	'''
	@summary: basic class for page operation
	'''
	def __init__(self, driver, url):
		self.driver = driver
		self.url = url
		self.timeout = 30

	def open_page(self):
		'''
		@summary:open page
		'''
		if self.url:
			self.driver.get(self.url)

	def locate_element(self, *location):
		'''
		@summary: find element, by id, name, xpath...
		:param location:
		:return: element object
		'''
		return self.driver.find_element(*location)

	def check_element_exist(self, *location):
		'''
		@summary:check wheter element exist
		:param location:
		:return: bool
		'''
		try:
			self.driver.find_element(*location)
			return True
		except:
			return False

	def get_current_windows_handler(self):
		'''
		@summary: get current active window handler
		:return: window handler
		'''
		current_window = self.driver.current_window_handle

		return current_window

	def switch_window(self, current_window):
		'''
		@summary: switch from one window to another
		:param current_window:
		'''
		all_window = self.driver.window_handles
		for window in all_window:
			if window != current_window:
				self.driver.switch_to.window(window)


if __name__ == "__main__":
	pass

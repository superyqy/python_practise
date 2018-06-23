#!/usr/bin/env python
#encoding: utf-8
'''
@summary: HTML page basic function
'''

class Page(object):
	'''
	@summary: basic class
	'''
	def __init__(self, driver, url):
		self.driver = driver
		self.url = url
		self.timeout = 30

	def open_page(self):
		if self.url:
			self.driver.get(self.url)

	def locate_element(self, *location):
		return self.driver.find_element(*location)

	def check_element_exist(self, *location):
		try:
			self.driver.find_element(*location)
			return True
		except:
			return False

	def get_current_windows_handler(self):
		current_window = self.driver.current_window_handle

		return current_window

	def switch_window(self, current_window):
		all_window = self.driver.window_handles
		for window in all_window:
			if window != current_window:
				self.driver.switch_to.window(window)


if __name__ == "__main__":
	pass

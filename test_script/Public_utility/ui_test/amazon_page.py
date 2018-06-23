#!/usr/bin/env python
#encoding: utf-8
'''
@summary: page instance for amazon pages
@author: YQY
@change: 2018-06-23 create script
'''

import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from page import Page
reload(sys)
sys.setdefaultencoding('utf-8')


class AmazonMainPage(Page):
	'''
	@summary: amazon main page, input book and search
	'''
	search_box = (By.ID, "twotabsearchtextbox")
	submit_button = (By.XPATH, '//*[@id="nav-search"]/form/div[2]/div/input')

	def input_book_name(self, book_name):
		'''
		@summary: input book name in search box
		:param book_name:
		:return:
		'''
		book_name = book_name.decode()
		self.locate_element(*self.search_box).send_keys(book_name)

	def click_to_search(self):
		'''
		@summary: click search botton
		:return:
		'''
		try:
			self.locate_element(*self.submit_button).click()
			return True
		except:
			return False

class BookListPage(Page):
	'''
	@summary: check whether book exist in page and click to open detail page
	'''
	test_book = (By.XPATH, '//*[@id="result_0"]/div/div[3]/div[1]/a/h2')

	def click_to_open_detail_page(self, book_title):
		'''
		@summary: open book detail page from book list page
		:param book_title:
		:return:
		'''
		current_window = None
		if self.check_element_exist(*self.test_book):
			if book_title == self.locate_element(*self.test_book).text:
				self.locate_element(*self.test_book).click()
				current_window = self.get_current_windows_handler()

		return current_window

class BookDetailPage(Page):
	'''
	@summary: add book into  cart and get result text and price
	'''
	test_book_name = (By.XPATH, '//*[@id="productTitle"]')
	add_cart_button = (By.ID, 'add-to-cart-button')
	add_success_text = (By.XPATH,'//*[@id="huc-v2-order-row-confirm-text"]/h1')
	price = (By.XPATH, '//*[@id="hlb-subcart"]/div[1]/span/span[2]')

	def get_product_title(self,current_window):
		'''
		@summary:get book title
		:param current_window:
		:return:
		'''
		self.switch_window(current_window)
		element = self.locate_element(*self.test_book_name)

		return element.text

	def add_into_cart(self):
		'''
		@summary: add book into cart
		:return:
		'''
		self.locate_element(*self.add_cart_button).click()

	def get_result_from_cart(self):
		'''
		@summary: get result text and price from cart page
		:return:
		'''
		result_text = ''
		result_price = ''

		if self.check_element_exist(*self.add_success_text):
			result_text = self.locate_element(*self.add_success_text).text
		if self.check_element_exist(*self.price):
			result_price = self.locate_element(*self.price).text

		return result_text, result_price

def search_book(url, driver, book_name):
	'''
	@summary: search book
	:param url:
	:param driver:
	:param book_name:
	:return:
	'''
	amazon_main_page = AmazonMainPage(driver, url)
	amazon_main_page.open_page()
	amazon_main_page.input_book_name(book_name)
	result = amazon_main_page.click_to_search()

	return result

def open_book_detail_page(url, driver, book_title):
	'''
	@summary: open book detail page
	:param url:
	:param driver:
	:param book_title:
	:return:
	'''
	book_list_page = BookListPage(driver, url)
	current_window = book_list_page.click_to_open_detail_page(book_title)

	return current_window

def add_into_cart(url, driver, current_window, title):
	'''
	@summary: add book into cart
	:param url:
	:param driver:
	:param current_window:
	:param title:
	:return:
	'''
	result_text = ''
	result_price = ''

	detail_page = BookDetailPage(driver, url)
	product_title = detail_page.get_product_title(current_window)
	if product_title == title:
		detail_page.add_into_cart()
		result_text, result_price = detail_page.get_result_from_cart()

	return result_text, result_price

def test_search_book(url, book, book_title):
	'''
	@summary: the whole process from search book and enter detail page and add into cart
	:param url:
	:param book:
	:param book_title:
	:return: string: result text and price
	'''
	result_text = ''
	result_price = ''

	driver = webdriver.Firefox()
	driver.implicitly_wait(30)  # setup implicitly wait time
	driver.maximize_window()

	try:
		result = search_book(url, driver, book)   # open amazon main page and search book
		if result:
			current_window = open_book_detail_page(url, driver, book_title)   # open book's detail page
			result_text,result_price = add_into_cart(url, driver, current_window, book_title)  # add book into cart
	except Exception as e:
		print "Search book error: {0}".format(e)
	finally:
		driver.quit()

	if isinstance(result_text, unicode):
		result_text = result_text.encode("utf-8")
	if isinstance(result_price, unicode):
		result_price = result_price.encode("utf-8").lstrip("￥ ")

	return result_text, result_price

if __name__ == "__main__":
	pass
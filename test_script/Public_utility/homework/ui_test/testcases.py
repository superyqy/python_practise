#!/usr/bin/env python
#encoding: utf-8
'''
@summary: run testcases with unittest framework
@author: YQY
@change: 2018-06-23 create script
'''
from selenium import webdriver
from amazon_page import AmazonMainPage
from amazon_page import BookListPage
from amazon_page import BookDetailPage


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


if __name__ == '__main__':
	pass
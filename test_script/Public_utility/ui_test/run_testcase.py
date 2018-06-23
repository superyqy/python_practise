#!/usr/bin/env python
#encoding: utf-8
'''
@summary: run testcases with unittest framework
@author: YQY
@change: 2018-06-23 create script
'''
import unittest
import amazon_page


class RunTestcase(unittest.TestCase):
	'''
	@summary:run all testcase with unittest
	'''
	def setUp(self):
		pass

	def test_add_book_into_cart(self):
		'''
		@summary: testcase of search book>enter detail page>add into cart>check result
		'''
		url = "https://www.amazon.cn"
		book = "软件测试"
		book_title = "软件测试(原书第2版)"
		standard_text = "商品已加入购物车"
		standard_price = "28"
		result_text, result_price = amazon_page.test_search_book(url, book, book_title)
		self.assertEqual(result_text, standard_text, "add to cart message doesn't match!")
		self.assertEqual(float(standard_price), float(result_price), "add to cart price doesn't match!")

	def tearDown(self):
		pass

if __name__ == "__main__":
	unittest.main()
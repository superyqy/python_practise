#!/usr/bin/env python
#encoding: utf-8
'''
@summary: selenium webdriver practise script
@author: YQY
@changed: 2018-02-24 create script
'''

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


URL = 'http://www.baidu.com'
URL_NEWS='http://news.baidu.com'
URL_PAN='http://pan.baidu.com'

def test_locate_element():
	try:
		driver = webdriver.Firefox()
		driver.get(URL)
		inputbox = driver.find_element_by_id('kw')
		inputbox.send_keys('baidu')
		time.sleep(3)
		inputbox.clear()
		time.sleep(10)
		driver.find_element_by_name('wd').send_keys('baidu')
		driver.find_element_by_xpath('//*[@id="kw"]').send_keys('test')
		driver.find_element_by_xpath("//input[@id='kw' and @name='wd']").send_keys('baidu')
		driver.find_element(By.ID,'kw').send_keys('1')
		driver.find_element(By.NAME, 'wd').send_keys('2')
		driver.find_element(By.XPATH, '//input[@id="kw"]').send_keys('3')
		driver.find_element_by_id('su').click()
		driver.find_element_by_id('su').submit()
		driver.quit()
	except Exception as e:
		print e

def test_control_browser_size():
	driver = webdriver.Firefox()
	driver.get(URL)
	driver.set_window_size(480,800)
	time.sleep(2)
	driver.maximize_window()
	driver.quit()

def test_forward_backward():
	driver = webdriver.Firefox()
	driver.get(URL)
	driver.get(URL_NEWS)
	driver.back()
	time.sleep(2)
	driver.forward()
	time.sleep(2)
	driver.quit()

def test_get_element_value():
	driver = webdriver.Firefox()
	driver.get(URL)
	inputbox =driver.find_element_by_id('kw')
	print inputbox.size
	text = driver.find_element_by_id("cp").text
	print text
	attribute = driver.find_element_by_id("kw").get_attribute('type')
	print attribute

def test_mouse_actionchains():
	driver=webdriver.Firefox()
	driver.implicitly_wait(8)
	driver.get(URL_PAN)
	login = driver.find_element(By.XPATH,'//*[@id="TANGRAM__PSP_4__footerULoginBtn"]')
	login.click()
	username = driver.find_element(By.ID,'TANGRAM__PSP_4__userName')
	username.send_keys('normalyoo')
	password = driver.find_element(By.ID,'TANGRAM__PSP_4__password')
	password.send_keys('JAY690038031.')
	submit = driver.find_element(By.ID,'TANGRAM__PSP_4__submit')
	submit.click()
	if check_if_element_exist(driver,'TANGRAM__PSP_29__rebindGuideCancel'):
		driver.find_element(By.ID, 'TANGRAM__PSP_29__rebindGuideCancel').click()
		print 'exist'
	else:
		print 'not exist'

	sort_icon = driver.find_element_by_xpath("//span[@class='icon icon-order']")
	ActionChains(driver).move_to_element(sort_icon).perform()
	sort_by_time = driver.find_element_by_xpath('//span[@data-key="time"]')
	sort_by_time.click()
	sort_by_size = driver.find_element_by_xpath("//li[@data-key='size']")
	sort_by_size.click()

def check_if_element_exist(driver,element_index):
	'''
	@summary: find_elements方法是查找页面上所有相同属性的方法
	'''
	elements_list = driver.find_elements(By.ID,element_index)
	if 0<len(elements_list):
		return True
	else:
		return False

def test_keyboard_event():
	driver = webdriver.Firefox()
	driver.implicitly_wait(8)
	driver.get(URL)
	search_box = driver.find_element_by_name('wd')
	search_box.send_keys("keyboard")
	search_box.send_keys(Keys.BACK_SPACE)
	search_box.send_keys(Keys.SPACE)
	time.sleep(2)
	search_box.send_keys("Test")
	time.sleep(2)
	search_box.send_keys(Keys.CONTROL,'a')
	search_box.send_keys(Keys.CONTROL,'c')
	search_box.send_keys(Keys.CONTROL,'v')
	search_box.send_keys(Keys.CONTROL,'x')
	time.sleep(3)
	search_box.send_keys(Keys.CONTROL,'v')
	search_box.send_keys(Keys.ENTER)

def test_get_url_title():
	driver = webdriver.Firefox()
	driver.implicitly_wait(8)
	driver.get(URL)
	print driver.current_url
	print driver.title
	print driver.find_element_by_name('wd').text

def test_webdriver_wait():
	driver = webdriver.Firefox()
	driver.get(URL)
	element = WebDriverWait(driver,5,0.5).until(EC.presence_of_element_located((By.NAME,'wd')))
	element.send_keys('test')

def test_get_mutiple_events():
	driver = webdriver.Firefox()
	driver.implicitly_wait(8)
	driver.get(URL)
	elements_list = driver.find_elements_by_name('wd')
	for element in elements_list:
		print element.get_attribute('type')
		if element.get_attribute('type')=='text':
			print 'yes'
		else:
			print 'no'



if __name__ == "__main__":
	test_get_mutiple_events()
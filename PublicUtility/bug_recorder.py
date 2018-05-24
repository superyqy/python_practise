#!/usr/bin/env python
# encoding: utf-8
'''
Create a common script fot get bug list from 禅道 bug_lst and generate html file
@author: YQY
@changed: 2018-05-24 create script
管理员账号登录禅道>后台>二次开发>Bug， 可获取相关API
'''
import json
import requests
import html_generator
import all_config

def create_session():
	'''
	@summary: create session and return sessionID
	'''
	session_id=''
	get_session_url = 'http://{0}:{1}/zentao/api-getsessionid.json?m=api&f=getSessionID&t=json'.format(all_config.IP_CHANDAO,all_config.PORT)

	response = requests.get(get_session_url)
	if 200 == response.status_code:
		result = response.json()
		result = json.loads(result['data'])
		session_id = result['sessionID']

	return session_id

def login_chandao(session_id):
	'''
	@summary: Login chandao with current session
	:param session_id:
	:return:
	'''
	login_status = False
	username = all_config.USERNAME_CHANDAO
	password = all_config.PASSWORD_CHANDAO
	login_url = 'http://{0}:{1}/zentao/user-login.json?f=login&t=json&sid={2}&account={3}&password={4}'.format(all_config.IP_CHANDAO, all_config.PORT, session_id, username, password)

	response = requests.post(login_url)
	if 200 == response.status_code:
		login_status = True
	else:
		print "login failed!"

	return login_status

def get_all_bug(session_id):
	'''
	@summary get all opened bug
	:param session_id:
	:return:
	'''
	bug_list = []
	product_type = 2 #信贷
	all_bug_url = 'http://{0}:{1}/zentao/bug-browse-{2}-0-unclosed-0.json?sid={3}'.format(all_config.IP_CHANDAO, all_config.PORT, product_type, session_id)
	# single_bug='http://10.1.10.42:81/zentao/bug-view-3296.json?sid={0}'.format(session_id)
	header = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
	          "Accept-Encoding": "gzip, deflate",
	          "Accept-Language": "zh-CN,zh;q=0.9",
	          "Connection": "keep-alive"}

	response = requests.get(all_bug_url, headers=header)
	data = response.json()
	data = data['data']
	data = data.decode("unicode-escape").encode("utf-8")
	data_list = data.split('{"id":"')

	for bug in data_list:
		if '"product":"2"' in bug:  # 获取信贷产品未关闭状态的bug
			bug_id = bug.split('",')[0]
			bug_title = bug.split('"title":"')[1].split('","')[0]
			bug_severity = bug.split('"severity":"')[1].split('","')[0]
			bug_link = '<a href="http://{0}:{1}/zentao/bug-view-{2}.html">http://{0}:{1}/zentao/bug-view-{2}.html</a>'.format(all_config.IP_CHANDAO, all_config.PORT, bug_id)
			bug_assign_to = bug.split('"assignedTo":"')[1].split('","')[0]
			bug_open_date = bug.split('openedDate":"')[1].split('","')[0]
			bug_opened_by = bug.split('openedBy":"')[1].split('","')[0]
			bug_list.append([bug_id, bug_title, bug_severity, bug_opened_by, bug_assign_to, bug_open_date,bug_link])

	return bug_list

def recorder_bug_and_genereate_html():
	name_list = ['ID','Title','Severity','Opened_by','Assign_to','Open_date','Link']
	session_id = create_session()
	title = 'Bug_list'
	if session_id:
		login_result = login_chandao(session_id)
		if login_result:
			bug_list = get_all_bug(session_id)
			if bug_list:
				htmler = html_generator.HtmlGenerator()
				htmler.create_html(title, value_list=bug_list, name_list=name_list)

if __name__ == '__main__':
	recorder_bug_and_genereate_html()
#!/usr/bin/env python
# encoding: utf-8
'''
@summary: API accesssor
@author: YQY
@change: 2018-03-09 create script
@change:2018-05-15 update script's logic and add comments and doc
'''
import os
try:
	import requests
except:
	os.system('sudo -H pip install requests')
	import requests
import urllib
import json
import configparser
import set_logging

class APIAccessor(object):
	'''
	@summary: api operator, include get, post, put, delete method
	'''
	def __init__(self):
		self.current_path = os.path.join(os.path.dirname(__file__),'config')
		conf = configparser.ConfigParser()
		conf.read(os.path.join(self.current_path,'api_config.ini'))
		self.server_ip = conf.get('HTTP', 'host')
		self.port = conf.get('HTTP','port')
		self.timeout = float(conf.get('HTTP','timeout'))
		self.logger = set_logging.set_logging('CI')

	def set_ip(self,ip):
		'''
		@summary: set api's ip
		@param ip: string ip
		'''
		self.server_ip = ip

	def set_port(self,port):
		'''
		@summary: set api's port
		@param port: string port
		'''
		self.port = port

	def assemble_url(self, url_part):
		'''
        @summary: assemble api's url
        @param url_part: string  api url
        @return: string url
        '''
		url = ''

		self.logger.info('start to assemble url for api, url_part: {0}'.format(url_part))

		if '' not in [self.server_ip, url_part]:
			if not url_part.startswith('/'):  # incase input url doesn't starts with '/'
				url_part = '/'.join(url_part)
				if self.port:
					url = 'http://{0}:{1}{2}'.format(self.server_ip, self.port, url_part)
			else:
				url = 'http://{0}{1}'.format(self.server_ip, url_part)
		else:
			self.logger.error('ip or url_part is empty, please have a check！')

		return url

	def get(self, url, param = {}, auth = (), cookie = {}):
		'''
        @summary: create GET request
        @param url: string url
        @param params: dictionary store input parameters
        @param auth: tuple store username and password
        @param cookie: dictionary store cookie information
        @return: a tuple response, first element is status_code, second is response body
        '''
		response = None

		self.logger.info('start to get by api, url: {0}, param: {1}, auth: {2}'.format(url, param, auth))

		if auth and not param and not cookie: # need authorization
			try:
				response = requests.get(url, auth = auth, timeout=self.timeout)
			except Exception as e:
				self.logger.critical('Get failed for: {0}'.format(e))
		elif param and not cookie and not auth:
			try:
				response = requests.get(url, param=param, timeout=self.timeout)
			except Exception as e:
				self.logger.critical('Get failed for: {0}'.format(e))
		elif cookie and not param and not auth:
			try:
				response = requests.get(url, cookie=cookie, timeout=self.timeout)
			except Exception as e:
				self.logger.critical('Get failed for: {0}'.format(e))
		elif param and auth:
			try:
				response = requests.get(url, param=param, auth = auth, timeout=self.timeout)
			except Exception as e:
				self.logger.critical('Get failed for: {0}'.format(e))
		elif param and cookie:
			try:
				response = requests.get(url, param=param, cookie=cookie, timeout=self.timeout)
			except Exception as e:
				self.logger.critical('Get failed for: {0}'.format(e))
		else:
			try:
				response = requests.get(url, timeout=self.timeout)
			except Exception as e:
				self.logger.critical('Get failed for: {0}'.format(e))

		status_code = response.status_code
		response_body = response.json()

		return status_code, response_body

	def post(self, url, payload):
		'''
        @summary: create POST request
        @param url: string request's url
        @param payload: dictionary request's paload data
        @return: a tuple response , first element is status_code, second is response body
        '''
		response = None

		self.logger.info('start to post data by api, url: {0}, payload: {1}'.format(url, payload))

		if payload:
			if isinstance(payload,dict): # post dictionary
				try:
					response = requests.post(url,data=payload, timeout=self.timeout)
				except Exception as e:
					self.logger.critical('Post failed for: {0}'.format(e))
			else:  # post string in json format
				try:
					response = requests.post(url,data=json.dumps(payload), timeout=self.timeout)
				except Exception as e:
					self.logger.critical('Post failed for: {0}'.format(e))

		status_code = response.status_code
		response_body = response.json()

		return status_code, response_body

	def put(self,url, payload):
		'''
		:param url:
		:param payload:
		:return:
		'''
		pass

	def delete(self,url,payload):
		'''
		:param url:
		:param payload:
		:return:
		'''
		pass

def operate_api(url_part, params = {}, payload={}, request_type = 'get'):
	'''
    @summary: operate API and get response code and body
    @param request_type: string ,optional, value should be get, post, put, delete
    @param params: string, optional, parameter in url
    @param payload: string, optional, payload data
    '''
	status_code = ''
	response_body = ''

	api_operator = APIAccessor()
	request_type = request_type.lower()

	if 'get' == request_type:
		url = api_operator.assemble_url(url_part, params = params)
		status_code, response_body = api_operator.get(url)
	elif 'post' == request_type:
		url = api_operator.assemble_url(url_part,params=params)
		status_code,response_body = api_operator.post(url, payload)

	return status_code, response_body


if __name__ == '__main__':
	pass


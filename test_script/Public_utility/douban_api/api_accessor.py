#!/usr/bin/env python
# encoding: utf-8
'''
@summary: API accesssor
@author: YQY
@change: 2018-06-22 create script
'''
import os
import json
import ConfigParser
try:
	import requests
except:
	os.system('pip install requests')
	import requests

class APIAccessor(object):
	'''
	@summary: api operator, include get, post, put, delete method
	'''
	def __init__(self):
		self.current_path = os.path.join(os.path.dirname(__file__), 'config')
		self.read_config()

	def read_config(self,config_name="api_config.ini"):
		'''
		@summary: read config parameters from config.ini
		:param config_name:
		:return:
		'''
		conf = ConfigParser.ConfigParser()
		conf.read(os.path.join(self.current_path, config_name))
		self.server_ip = conf.get('HTTP', 'host')
		self.port = conf.get('HTTP', 'port')
		self.url = conf.get('HTTP', 'url')
		self.timeout = float(conf.get('HTTP', 'timeout'))

	def assemble_url(self, resource_url):
		'''
        @summary: assemble api's url
        @param url_part: string  api url
        @return: string url
        '''
		url = ''

		if resource_url:  # resource url exist
			if self.server_ip != "0.0.0.0" and self.port != "0":
				url = 'http://{0}:{1}/{2}'.format(self.server_ip, self.port, resource_url.lstrip("/"))
			elif self.url:
				url = self.url
		else:
			print "Assemble api's url failed, need to check config.ini!"

		return url

	def get(self, url, single_parameter='', parameters={}):
		'''
        @summary: create GET request
        @param url: string url
        @param params: dictionary store input parameters
        @param auth: tuple store username and password
        @param cookie: dictionary store cookie information
        @return: a tuple response, first element is status_code, second is response body
        '''
		status_code = -1   # store returned status code
		response_body = {}  # store response body in dictionary format

		if parameters and not single_parameter:  # request with parameter dictionary
			try:
				response = requests.get(url, params=parameters, timeout=self.timeout)
				status_code = response.status_code
				response_body = response.json()
			except Exception as e:
				print 'Request failed! URL: {0}, Parameters: {1}, Error: {2}'.format(url, parameters, e)
		elif single_parameter and not parameters:  # request with single parameter value
			url = url.rstrip("/") + "/" + single_parameter
			try:
				response = requests.get(url, timeout=self.timeout)
				status_code = response.status_code
				response_body = response.json()
			except Exception as e:
				print 'Request failed! URL: {0},Parameter: {1}, Error: {2}'.format(url, single_parameter, e)

		return status_code, response_body

	def post(self, url, payload):
		'''
		@summary: create POST request
		@param url: string request's url
		@param payload: dictionary request's payload data
		@return: a tuple response , first element is status_code, second is response body
		'''
		status_code = -1  # store returned status code
		response_body = {}  # store response body in dictionary format

		if payload and url:
			if isinstance(payload, dict):  # post dictionary
				try:
					response = requests.post(url, data=payload, timeout=self.timeout)
					status_code = response.status_code
					response_body = response.json()
				except Exception as e:
					print 'Request failed! URL: {0},Payload: {1}, Error: {2}'.format(url, payload, e)
			else:  # post string in json format
				try:
					response = requests.post(url, data=json.dumps(payload), timeout=self.timeout)
					status_code = response.status_code
					response_body = response.json()
				except Exception as e:
					print 'Request failed! URL: {0},Payload: {1}, Error: {2}'.format(url, payload, e)

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


if __name__ == '__main__':
	pass

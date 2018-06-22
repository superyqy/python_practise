#!/usr/bin/env python
# encoding: utf-8
'''
@summary: testcase for douban api
@author: YQY
@change: 2018-06-22 create script
'''
import api_accessor

class DoubanTest():
	'''
	@summary: create testcase for douban api test
	'''
	def __init__(self):
		self.api_operator = api_accessor.APIAccessor()

	def access_api(self, url_part, single_parameter='', parameters={}, payload={}, request_type='get'):
		'''
		@summary: operate API and get response code and body
		@param request_type: string ,optional, value should be get, post, put, delete
		@param params: string, optional, parameter in url
		@param payload: string, optional, payload data
		'''
		status_code = -1
		response_body = {}

		request_type = request_type.lower()

		if 'get' == request_type:
			url = self.api_operator.assemble_url(url_part)
			status_code, response_body = self.api_operator.get(url, single_parameter=single_parameter, param=parameters)
		elif 'post' == request_type:
			url = self.api_operator.assemble_url(url_part)
			status_code, response_body = self.api_operator.post(url, payload)

		return status_code, response_body

	def check_status_code(self, status_code):
		'''
		@summary: compare status code
		@param: int status_code
		@return: bool result
		'''
		result = False
		request_success = 200

		if request_success == status_code:
			result = True
		else:
			print 'Request failed for {0}!'.format(status_code)

		return result



if __name__ == "__main__":
	pass
	movie_id = '1304102'
	url = "http://api.douban.com/v2/movie/subject/{0}".format(movie_id)
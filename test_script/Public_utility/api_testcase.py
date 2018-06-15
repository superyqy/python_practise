#!/usr/bin/env python
#encoding: utf-8
'''
Create scripts for API automation test
@author: YQY
@change: 2018-06-11 create script
'''
import os
import json
from api_accessor import api_accessor
import requests
from set_logging import log_event
from excel_handler import excel_handler

@log_event
def test_api():
	# r = requests.get('http://10.1.10.91:9002/lx/openapi/salesman/qualification')
	req_param = {"loanContractNo":"SZFT201806120002"}
	status_code, body = api_accessor.operate_api(url_part=r"/business/p2pAppInfoAction.do",params=req_param,request_type='post')

	return status_code, body


def read_excel(file_path):
	request_params = {}  # store request parameter
	standard_data = {}   # store response parameter
	request_start_row = 0 # store request start row in excel
	response_start_row = 0 # store response start row in excel

	if os.path.exists(file_path):
		reader = excel_handler.ExcelReader(file_path)
		sheet = reader.get_sheet_object(sheet_index=1)  # get sheet by sheet index

		for i in range(200):
			name = reader.get_cell(sheet,i,1)
			if name == 'request parameter':
				request_start_row = i+1
			if name == 'response parameter':
				response_start_row = i+1
				break

		if request_start_row>0 and response_start_row >0:
			for i in range(request_start_row, response_start_row-1):  # get request parameters
				name = reader.get_cell(sheet,i,1)
				value = reader.get_cell(sheet,i,2)
				request_params[name] = value
			for i in range(response_start_row, 200): # get response parameter's name, value and compare type
				name = reader.get_cell(sheet,i,1)
				if name:
					value = reader.get_cell(sheet,i,2)
					compare_type = reader.get_cell(sheet,i,3)
					standard_data[name] = [value, compare_type]
				else:
					break  # break when reach the response's end

	return request_params, standard_data,request_start_row


def compare_response_parameter(response_data, standard_data, compare_type='in'):
	'''
	@summary: compare response data with standard data
	'''
	compare_result = False
	compare_type = compare_type.lower()

	if response_data and standard_data and compare_type:
		if 'in' == compare_type:
			if standard_data in response_data:
				compare_result = True
		elif 'not in' == compare_type:
			if not standard_data in response_data:
				compare_result = True
		elif 'equal' == compare_type:
			if standard_data == response_data:
				compare_result = True
		elif 'not equal' == compare_type:
			if standard_data <> response_data:
				compare_result = True
		elif 'less than' == compare_type:
			if float(response_data) < float(standard_data):
				compare_result = True
		elif 'greater than' == compare_type:
			if float(response_data) > float(standard_data):
				compare_result = True

	return compare_result


def testcase_one(file_path):
	false_count = 0

	request_params, standard_data,request_start_row = read_excel(file_path)  # get standard data and compare type from excel
	print request_params
	print type(request_params)

	writer = excel_handler.ExcelWriter(file_path)
	writer.write_cell(sheet_name="Sheet1", data=json.dumps(request_params), row=request_start_row-1, column=4)
	print 'finish'

	# status_code, result_data = test_api()  # get api response code and body
	# print status_code
	# print result_data
	# return
	# if api_accessor.compare_status_code(status_code):
	# 	if result_data:
	# 		if isinstance(result_data, dict):
	# 			for key,value in result_data.items():
	# 				if key in standard_data.keys():
	# 					result = compare_response_parameter(value,standard_data[key][0],standard_data[key][1])
	# 					if not result:
	# 						false_count +=1
	# print '##########'
	# print false_count
	# print '##########'

	return false_count


if __name__ == '__main__':
	file_path=r"E:\yinxiuwen\yqy_ci\test_data\testcase_1.xls"
	testcase_one(file_path)
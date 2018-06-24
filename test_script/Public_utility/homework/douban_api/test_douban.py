#!/usr/bin/env python
# encoding: utf-8
'''
@summary: testcase for douban api
@author: YQY
@change: 2018-06-22 create script
'''
import os
import re
import json
import time
import excel_handler
import api_accessor

class ReadExcel(object):
	'''
	@summary: read testcase from excel file
	'''
	base_info = "request base info"
	request = "request parameter"
	response = "response parameter"
	max_row_size = 300

	def __init__(self):
		self.testcase_dir = os.path.join(os.path.dirname(__file__), 'testcase')

	def read_excel(self, file_path):
		'''
		@summary: read excel
		:param file_path:
		:return: dictioanry all_sheet_data to store all sheet's data
		'''
		all_sheet_data = {}

		if os.path.exists(file_path):
			if file_path.endswith(".xls") and not file_path.startswith("~"):
				reader = excel_handler.ExcelReader(file_path)
				sheet_name_list = reader.get_sheets_name() # get all sheets' name
				if sheet_name_list:
					for sheet_name in sheet_name_list:
						url = ""
						method = ""
						request_parameters = {}
						response_parameters = {}
						if 'template' == sheet_name.lower():  # skip template sheet
							continue
						sheet = reader.get_sheet_object(sheet_name=sheet_name)  # get sheet by sheet name
						if not sheet:  # skip if can't get sheet object
							continue
						base_info_row, request_row, response_row, end_empty_row = self.get_row_number(reader, sheet)  # get all row number
						if 0 not in [base_info_row, request_row, response_row, end_empty_row]:
							if base_info_row < request_row:
								url, method = self.get_base_info(reader, sheet, base_info_row+1, request_row)  # get base info
							if request_row < response_row:
								request_parameters = self.get_request_parameter(reader, sheet, request_row+1, response_row)  # get request parameter
							if response_row < end_empty_row:
								response_parameters = self.get_response_parameter(reader, sheet, response_row+1, end_empty_row)  # get response parameter
						if url and method and request_parameters and response_parameters:
							all_sheet_data[sheet_name] = [url, method, request_parameters, response_parameters]

		return all_sheet_data

	def transfer_data_type(self, data):
		'''
		@summary transfer number and float data format
		:param data:
		:return:
		'''
		parameter_value = ""
		int_number = re.compile("^-?\d+$")  #  匹配整数
		float_number = re.compile("^-?\d+\.\d+$")  # 匹配负数，浮点数

		if str(data).endswith(".0"):  # transfer unicode data to string and split .0
			data = str(data)
			data = data.split(".")[0]

		if int_number.match(str(data)):
			parameter_value = int(str(data))
		elif float_number.match(str(data)):
			parameter_value = float(str(data))
		elif isinstance(data,unicode):
			parameter_value = data.encode("utf-8")
		else:
			parameter_value = data

		return  parameter_value

	def get_base_info(self, reader, sheet, start_row, end_row):
		'''
		@summary: get request base info
		:param reader:
		:param sheet:
		:param start_row:
		:param end_row:
		:return:
		'''
		url = ''
		method = ''

		if reader and sheet and start_row>0 and start_row<end_row:
			for row in range(start_row, end_row):
				name = reader.get_cell(sheet, row, 1).lower()
				value = reader.get_cell(sheet, row, 2)
				if "url" == name:
					url = self.transfer_data_type(value)
				elif "method" == name:
					method = self.transfer_data_type(value)
				if url and method:
					break

		return url, method

	def get_request_parameter(self,reader, sheet, start_row, end_row):
		'''
		@summary: get request parameters
		:param reader:
		:param sheet:
		:param start_row:
		:param end_row:
		:return:
		'''
		request_parameters = {}

		if reader and sheet and start_row > 0 and start_row < end_row:
			for row in range(start_row, end_row):
				name = self.transfer_data_type(reader.get_cell(sheet, row, 1))
				value =  self.transfer_data_type(reader.get_cell(sheet, row, 2))
				if name and value != None:
					request_parameters[name] = value

		return request_parameters

	def get_response_parameter(self,reader, sheet, start_row, end_row):
		'''
		@summary: get response parameters
		:param reader:
		:param sheet:
		:param start_row:
		:param end_row:
		:return:
		'''
		response_parameters = {}

		if reader and sheet and start_row > 0 and start_row < end_row:
			for row in range(start_row, end_row):
				name = self.transfer_data_type(reader.get_cell(sheet, row, 1))
				type = self.transfer_data_type(reader.get_cell(sheet, row, 2))
				value =  self.transfer_data_type(reader.get_cell(sheet, row, 3))
				if name and type and value:
					response_parameters[name] = [type, value, row]

		return response_parameters

	def get_row_number(self, reader, sheet):
		'''
		@summary:get each start row number
		:param reader:
		:param sheet:
		:return:
		'''
		base_info_row = 0
		request_row = 0
		response_row = 0
		end_empty_row = 0

		if reader and sheet:
			for i in range(1,self.max_row_size):
				name = reader.get_cell(sheet,i,1)
				if not name:   # get end row
					end_empty_row = i
				elif name.lower() == self.base_info:  # get base info start row
					base_info_row = i
				elif name.lower() == self.request:  # get request start row
					request_row = i
				elif name.lower() == self.response:  # get response start row
					response_row = i
				if 0 not in [base_info_row, request_row, response_row, end_empty_row]:  # break if all row number acquired
					break

		return base_info_row, request_row, response_row, end_empty_row

	def main(self):
		'''
		@summary: get all excel files' data
		:return:
		'''
		all_data = {}

		if os.path.exists(self.testcase_dir):
			excel_file_list = []
			if os.path.isfile(self.testcase_dir): # input work dir is a single file
				excel_file_list.append(self.testcase_dir)
			else:
				excel_file_list = os.listdir(self.testcase_dir)
			for file in excel_file_list:
				excel_file_name = os.path.basename(file).split(".")[0]
				all_sheet_data = self.read_excel(os.path.join(self.testcase_dir, file))
				all_data[excel_file_name] = all_sheet_data

		return all_data


class AccessAPI(object):
	'''
	@summary: create testcase for douban api test
	'''
	def __init__(self):
		self.api_operator = api_accessor.APIAccessor()

	def access_api(self, url_part, single_parameter='', parameters={}, payload={}, request_type='GET'):
		'''
		@summary: operate API and get response code and body
		@param request_type: string ,optional, value should be get, post, put, delete
		@param params: string, optional, parameter in url
		@param payload: string, optional, payload data
		'''
		status_code = -1
		response_body = {}

		request_type = request_type.upper()
		if 'GET' == request_type:
			url = self.api_operator.assemble_url(url_part)
			status_code, response_body = self.api_operator.get(url, single_parameter=single_parameter, parameters=parameters)
		elif 'POST' == request_type:
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
		request_success = 200  # this can be changed by situation

		if request_success == status_code:
			result = True
		else:
			print 'Request failed for {0}!'.format(status_code)

		return result


def compare_response_parameter(respone_parameter, standard_parameter, compare_type):
	'''
	@summary: compare response parameter
	:param respone_parameter:
	:param standard_parameter:
	:param compare_type:
	:return:
	'''
	result = "Failed"

	compare_type = compare_type.lower()
	if compare_type == "equal":
		if str(respone_parameter) == str(standard_parameter):
			result = "Pass"
	elif compare_type == "not equal":
		if str(respone_parameter) != str(standard_parameter):
			result = "Pass"
	elif compare_type == 'less than':
		if float(respone_parameter) < float(standard_parameter):
			result = "Pass"
	elif compare_type == 'greater than':
		if float(respone_parameter) > float(standard_parameter):
			result = "Pass"
	elif compare_type == 'in':
		if str(respone_parameter) in str(standard_parameter):
			result = "Pass"
	elif compare_type == 'not in':
		if str(respone_parameter) not in str(standard_parameter):
			result = "Pass"

	return result

def get_value_with_mutiple_level(check_key, target_dict, level):
	result_value = ""

	if 1<level and isinstance(check_key, list) and isinstance(target_dict, dict):
		if 2 == level:
			if check_key[0] in target_dict.keys():
				for item in target_dict[check_key[0]]:
					if check_key[1] in item.keys():
						result_value = item[check_key[1]]
						break
		elif 3 == level:
			if check_key[0] in target_dict.keys():
				for item in target_dict[check_key[0]]:
					if check_key[1] in item.keys():
						for data in item[check_key[1]]:
							if check_key[2] in data.keys():
								result_value = data[check_key[2]]
								break

	return result_value

def create_folder():
	'''
	@summary create folder with time as name
	'''
	result_folder = os.path.join(os.path.dirname(__file__), 'testresult')
	current_time = time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time()))
	result_folder = os.path.join(result_folder, current_time)

	if not os.path.exists(result_folder):
		os.makedirs(result_folder)

	return result_folder

def execute_testcase():
	'''
	@summary: read testcase from excel, accesss api, compare result
	:return: dictionary, all_file_result, store all file's all sheet's result
	'''
	all_file_result = {}  # excel file name as key, each file's all sheet result as value
	read_excel = ReadExcel()
	access_api = AccessAPI()

	all_files_data = read_excel.main()  #  get all testcase from excel testcases

	if all_files_data:
		for each_file in all_files_data.keys():
			each_file_result = {}
			for sheet_name in all_files_data[each_file].keys():  # check each sheet, one sheet is one testcase
				all_response_compare_result = {}
				testcase =  all_files_data[each_file][sheet_name]
				url = testcase[0]
				request_type = testcase[1]
				response_parameters_dict = testcase[3]
				status_code = -1
				response_body = {}
				if 1 == len(testcase[2].items()):  # accesss api with one parameter
					single_param = testcase[2].values()[0]
					status_code, response_body = access_api.access_api(url_part=url, single_parameter=single_param,request_type= request_type)
				elif 1 < len(testcase[2].items()): # accesss api with more than one parameter
					status_code,response_body = access_api.access_api(url_part=url, parameters=testcase[2], request_type=request_type)
				if access_api.check_status_code(status_code):
					for key in response_parameters_dict.keys():
						standard_parameter = response_parameters_dict[key][1]
						compare_type = response_parameters_dict[key][0]
						row = response_parameters_dict[key][2]
						if ":" in key:  # key has mutiple levels
							key_with_level = key.split(":")
							respone_parameter = get_value_with_mutiple_level(key_with_level,response_body, len(key_with_level))
							all_response_compare_result[row] = compare_response_parameter(respone_parameter,standard_parameter,compare_type)
						else:  # key has only one level
							if key in response_body.keys():
								respone_parameter = response_body[key]
								all_response_compare_result[row] = compare_response_parameter(respone_parameter, standard_parameter, compare_type)
							else:
								all_response_compare_result[row] = "Can't find response parameter"
				each_file_result[sheet_name] = all_response_compare_result
			all_file_result[each_file] = each_file_result

		return all_file_result

def write_result_into_excel(all_file_result):
	'''
	@summary: 本来应该以testcase.xls为模板，存储在testresult文件夹中，但周末时间不够写完后续excel存储相关代码，只能先以Json形式存为TXT
	:param all_file_result:
	'''
	if all_file_result:
		result_folder = create_folder()
		result_file = os.path.join(result_folder, 'result.txt')
		with open(result_file,'w') as f:
			f.writelines(json.dumps(all_file_result))
		print "Test completed, API Test result stored in: {0}".format(result_file)

def run():
	all_file_result = execute_testcase()
	write_result_into_excel(all_file_result)

if __name__ == "__main__":
	run()
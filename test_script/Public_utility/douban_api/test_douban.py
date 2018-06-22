#!/usr/bin/env python
# encoding: utf-8
'''
@summary: testcase for douban api
@author: YQY
@change: 2018-06-22 create script
'''
import os
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
					url = value
				elif "method" == name:
					method = value
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
				name = reader.get_cell(sheet, row, 1)
				value = reader.get_cell(sheet, row, 2)
				if name and value:
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
				name = reader.get_cell(sheet, row, 1)
				type = reader.get_cell(sheet, row, 2)
				value = reader.get_cell(sheet, row, 3)
				if name and type and value:
					response_parameters[name] = [type, value]

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


class DoubanTest(object):
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
			print url
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
		request_success = 200

		if request_success == status_code:
			result = True
		else:
			print 'Request failed for {0}!'.format(status_code)

		return result


def main():
	url = '/v2/movie/subject'
	tester = DoubanTest()
	status_code,response_body = tester.access_api(url_part=url,single_parameter="1304102")
	print status_code
	result = response_body['casts']
	for actor in result:
		print actor["id"]


if __name__ == "__main__":

	reader = ReadExcel()
	data = reader.main()
	print data
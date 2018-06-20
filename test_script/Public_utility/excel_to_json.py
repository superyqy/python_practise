#!/usr/bin/env python
#encoding: utf-8
'''
@summary: read api's request parameters and create a dictionary format
@author：YQY
@change: created at 2018-06-18 by YQY
'''

import os
import sys
import time
import json
from decimal import Decimal
from excel_handler import excel_handler


class ExcelToJson(object):
	request_name = "Test Case Name"  # request parameter start signal
	first_level = "1st_level"
	second_level = "2rd_level"
	max_row_size = 300

	def __init__(self, work_dir):
		self.current_min = time.strftime('%Y%m%d%H%M',time.localtime(time.time()))
		self.current_dir = os.path.dirname(__file__)
		self.work_dir = work_dir

	def read_excel(self, file_path):
		'''
		@summary: read excel
		:param file_path:
		:return: dictioanry all_sheet_data to store all sheet's data
		'''
		all_sheet_data = {}

		if os.path.exists(file_path):
			if file_path.endswith(".xls"):
				file_name = os.path.basename(file_path)
				reader = excel_handler.ExcelReader(file_path)
				sheet_name_list = reader.get_sheets_name() # get all sheets' name
				if sheet_name_list:
					for sheet_name in sheet_name_list:
						request_name_row = []  # store all request start row number
						end_empty_row = 0
						sheet = reader.get_sheet_object(sheet_name=sheet_name)  #get sheet by sheet name
						if not sheet:  # skip if sheet doesn't exist
							continue
						for i in range(1, self.max_row_size):
							name = reader.get_cell(sheet, i, 1)
							if name == self.request_name:  # get all request parameter name's start row
								request_name_row.append(i)
						if request_name_row:
							for i in range(request_name_row[-1], self.max_row_size):  # get the end empty row's number
								if not reader.get_cell(sheet, i, 1):
									end_empty_row = i
									break
							parameter_name_dict = {}  # store parameter name row-number as key, parameter name as value
							for i in range(len(request_name_row)):  # get all parameter name
								parameter_name_dict[request_name_row[i]] = self.read_parameter_name(reader, sheet, request_name_row[i])
							for key, value in parameter_name_dict.items(): # get parameter value by row
								row = key
								parameter_name_list = parameter_name_dict[key]
								request_parameters, testcase_name = self.read_parameter_value(reader, sheet, row+1, parameter_name_list)

						# 	for i in range(request_start_row, response_start_row-1):  # get request parameters
						# 		name = reader.get_cell(sheet,i,1)
						# 		if name:
						# 			value = reader.get_cell(sheet,i,2)
						# 			request_params[name] = value
						#
						#
						# if request_params:  # store current sheet's request params into txt file
						# 	self.write_request_into_file(request_params, sheet_name, file_name)
						#
						# all_sheet_data[sheet_name] = [request_params, standard_data,request_start_row] # store all data into dictionary

		return all_sheet_data

	def read_parameter_value(self, reader, sheet, row, parameter_name_list):
		'''
		@summary read parameter's value
		:param reader:
		:param sheet:
		:param row:
		:param parameter_name_list:
		:return:
		'''
		request_parameters = {}  # parameter name as key, cell value as value
		testcase_name = ""  # test case name
		if reader and sheet and row and parameter_name_list:
			level_one_index_list = self.get_all_level_one_index(parameter_name_list)
			testcase_name = reader.get_cell(sheet, row, 1)
			print testcase_name
			if not level_one_index_list:  # parameter has only one level
				pass
				# for i in range(1,len(parameter_name_list)):
				# 	parameter_name, parameter_value = self.transfer_data_type(parameter_name_list[i], reader.get_cell(sheet, row, i + 1))
				# 	request_parameters[parameter_name] = parameter_value
			else:
				second_level_index_list = self.get_all_level_two_index(parameter_name_list, level_one_index_list)
				print second_level_index_list


		return testcase_name, request_parameters

	def read_parameter_value_with_mutiple_level(self, parameter_name_list, second_level_index_list, reader, sheet, row):
		row_dict = {} # parameter name as key, parameter value as value
		level_one_index_list = second_level_index_list.keys()
		end_cell_index = len(parameter_name_list)

		for i in range(level_one_index_list):
			first_level_index = level_one_index_list[i]
			if second_level_index_list[first_level_index]:  # second level exist
				start_cell = second_level_index_list[first_level_index]
			else:  # second level not exist
				if not level_one_index_list[i] == end_cell_index:
					for i in range(first_level_index, level_one_index_list[i+1]):
						cell_value = reader.get_cell(sheet, row, i+1)
						row_dict[parameter_name_list[i]] = cell_value


	def get_all_level_one_index(self, parameter_name_list):
		level_one_index_list = []

		for i in range(len(parameter_name_list)):
			if self.first_level == parameter_name_list[i].lower():
				level_one_index_list.append(i+1)

		return level_one_index_list

	def get_all_level_two_index(self, parameter_name_list, level_one_index_list):
		second_level_index_list = {}

		for level_one in level_one_index_list:   # init each level_1's second level cell index
			second_level_index_list[level_one] = []
		if parameter_name_list and level_one_index_list:
			for i in range(len(level_one_index_list)-1):  # search second level one for all level one except the last one
				second_level_index = []
				for j in range(level_one_index_list[i], level_one_index_list[i+1]):
					if self.second_level == parameter_name_list[j].lower():
						second_level_index.append(j+2)
				second_level_index_list[level_one_index_list[i]] = second_level_index
			for j in range(level_one_index_list[-1], len(parameter_name_list)-1):  # search second level for the last level one
				second_level_index = []
				if self.second_level == parameter_name_list[j].lower():
					second_level_index.append(j+2)
					second_level_index_list[level_one_index_list[-1]] = second_level_index

		return second_level_index_list

	def transfer_data_type(self, parameter_name, data):

		parameter_type = ""
		parameter_value = ""

		parameter_name = parameter_name

		if ":" in parameter_name:  # get parameter type
			parameter_name, parameter_type = parameter_name.split(":")
		# transfer data type
		if not parameter_type:
			parameter_value = data
		elif "int" in parameter_type.lower():
			print data
			parameter_value = int(data)
		elif "num" in parameter_type.lower():
			parameter_value = Decimal(str(data))
		else:
			parameter_value = data

		return parameter_name, parameter_value

	def read_parameter_name(self, reader, sheet, row):
		'''
		@summary read parameter name
		:param reader:
		:param sheet:
		:param row:
		:return:
		'''
		name_list = []

		if reader and sheet and row:
			for i in range(self.max_row_size):
				cell_value = reader.get_cell(sheet, row, i+1)
				if cell_value:
					name_list.append(cell_value)
				else:
					break

		return name_list


	# def read_single_row(self,reader, sheet, row):
	# 	'''
	# 	@summary read single row data
	# 	:param sheet:
	# 	:param row:
	# 	:return:
	# 	'''
	# 	case_name = ''
	# 	parameter_name = []
	#
	# 	if reader and sheet and row:
	# 		case_name = reader.get_cell(sheet, row, 1)


	def write_request_into_file(self,request_params, sheet_name, file_name):
		'''
		@summary: write request param as json
		:param request_params:
		:param sheet_name:
		:param file_name:
		'''
		if request_params and sheet_name and file_name:
			result_folder = self.create_folder_by_time()
			result_file = os.path.join(result_folder, file_name.split(".")[0]+".txt")
			with open(result_file,'a') as f:
				f.writelines(sheet_name+":\n")
				f.writelines(json.dumps(request_params))
				f.writelines("\n\n")

			print "Stored {0}'s {1} into {2} successfully!".format(file_name, sheet_name, result_file)


	def create_folder_by_time(self):
		'''
		@summary create folder with time as name
		'''
		result_folder = os.path.join(self.current_dir,self.current_min)

		if not os.path.exists(result_folder):
			os.makedirs(result_folder)

		return result_folder


	def get_all_file_request_data(self):
		'''
		@summary: get all excel files' data
		:return:
		'''
		if os.path.exists(self.work_dir):
			if os.path.isfile(self.work_dir): # input work dir is a single file
					_ = self.read_excel(self.work_dir)
			else:
				files = os.listdir(self.work_dir)
				for file in files:
					self.read_excel(os.path.join(self.work_dir,file))

if __name__ == "__main__":
	work_dir = r"E:\yinxiuwen\yqy_ci\test_case\testcase_template.xls"    #sys.argv[1]  #
	processor = ExcelToJson(work_dir)
	processor.get_all_file_request_data()



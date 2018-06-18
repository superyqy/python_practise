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
from excel_handler import excel_handler


class ExcelToJson(object):
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
						request_params = {}  # store request parameter
						standard_data = {}  # store response parameter
						request_start_row = 0  # store request start row in excel
						response_start_row = 0  # store response start row in excel
						sheet = reader.get_sheet_object(sheet_name=sheet_name)  #get sheet by sheet name
						for i in range(1,200):
							name = reader.get_cell(sheet,i,1)
							if name == 'request parameter':  # get request parameter's start row
								request_start_row = i+1
							if name == 'response parameter':  #get response parameter's start row
								response_start_row = i+1
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
						if request_params:  # store current sheet's request params into txt file
							self.write_request_into_file(request_params, sheet_name, file_name)

						all_sheet_data[sheet_name] = [request_params, standard_data,request_start_row] # store all data into dictionary

		return all_sheet_data


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
	work_dir = sys.argv[1]
	processor = ExcelToJson(work_dir)
	processor.get_all_file_request_data()
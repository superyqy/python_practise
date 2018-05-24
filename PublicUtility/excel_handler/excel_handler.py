#!/usr/bin/env python
# encoding: utf-8
'''
Create a excel handler to read and write excel file
@author: YQY
@change: 2018-05-22 create script, add excel reader
@change: 2018-05-23 add new function to get sheet by index
'''
# https://blog.csdn.net/chengxuyuanyonghu/article/details/54951399
# http://www.open-open.com/lib/view/open1472701496085.html
#https://blog.csdn.net/chengxuyuanyonghu/article/details/54951399   参考这个

import  set_logging
import time
import os
try:
	import xlrd
except:
	os.system("sudo -H pip install xlrd")
	import xlrd
try:
	import xlwt
except:
	os.system("sudo -H pip install xlwt")
	import xlwt


class ExcelReader(object):
	def __init__(self,file_path):
		self.file_path = file_path
		self.create_workbook()

	def create_workbook(self):
		'''
		@summary: create excel workbook
		'''
		if os.path.exists(self.file_path):
			self.workbook = xlrd.open_workbook(self.file_path)

	def get_sheets_name(self):
		'''
		@summary: get all sheets name
		'''
		sheet_name_list = []

		if self.workbook:
			sheet_name_list = self.workbook.sheet_names()

		return sheet_name_list

	def get_sheet_object(self,sheet_name='',sheet_index=-1):
		'''
		@summary get sheet object
		'''
		sheet = None

		if self.workbook:  #workbook exist
			sheet_name_list = self.get_sheets_name()
			if sheet_name in sheet_name_list:  # get sheet by sheet name
				sheet = self.workbook.sheet_by_name(sheet_name)
			elif sheet_index>0 and sheet_index<= len(sheet_name_list):  # get sheet by sheet index
				sheet = self.workbook.sheet_by_index(sheet_index-1)

		return sheet

	def _get_row_count(self, sheet):
		'''
		@suummary: get sheet's row total count
		'''
		rows = 0

		if self.workbook and isinstance(sheet,object):
			rows = sheet.nrows

		return rows

	def _get_column_count(self, sheet):
		'''
		@summary: get sheet's column total count
		'''
		columns = 0

		if self.workbook and isinstance(sheet,object):
			columns = sheet.ncols

		return columns

	def get_cell_type(self,sheet,row,column):
		'''
		@summary: get cell value
		'''
		cell_type = None  #ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error

		if isinstance(sheet,object):
			total_row = self._get_row_count(sheet)
			total_column = self._get_column_count(sheet)
			if row<=total_row and column<=total_column and row>=1 and column>=1:
				cell_type = sheet.cell(row-1,column-1).ctype  # -1 for read excel data start from index 0,0

		return cell_type

	def get_cell(self,sheet,row,column):
		'''
		@summary: get cell value
		'''
		cell_data = None

		if isinstance(sheet,object):
			total_row = self._get_row_count(sheet)
			total_column = self._get_column_count(sheet)
			if row<=total_row and column<=total_column and row>=1 and column>=1:
				cell_data = sheet.cell_value(row-1,column-1)  # -1 for read excel data start from index 0,0

		return cell_data

	def get_date_from_cell(self,sheet,row,column):
		'''
		@summary: get date format data from cell
		:param sheet:
		:param row:
		:param column:
		:return:
		'''
		date_cell = ()

		if isinstance(sheet,object):
			if self.get_cell_type(sheet,row,column) == 3:# 3 is date format
				cell_data = self.get_cell(sheet,row,column) # get cell data
				date_cell = xlrd.xldate_as_tuple(cell_data,self.workbook.datemode) # transfer cell data into tuple
				date_cell = self.transfer_data_into_date(date_cell)

		return date_cell

	def transfer_data_into_date(self,date):
		'''
		@summary transfer data into date format
		:param date_cell:
		:return:
		'''
		result = None
		print date
		if isinstance(date,tuple):
			current_time = time.mktime(date)
			print current_time
			result =  time.strftime("%Y-%m-%d %H:%M%S",current_time)

		return result

	def get_row(self,sheet, row):
		'''
		@summary: get specifiled row's data
		:param sheet:
		:param row:
		:return:
		'''
		row_data = [] # store row's all cell data as list

		if isinstance(sheet,object):
			total_row = self._get_row_count(sheet)
			if row <= total_row and row >= 1:
				row_data = sheet.row_values(row-1)

		return row_data

	def get_column(self,sheet,column):
		'''
		@summary: get specifiled column's data
		:param sheet:
		:param column:
		:return:
		'''
		column_data = []  # store row's all cell data as list

		if isinstance(sheet,object):
			total_column = self._get_column_count(sheet)
			if column <= total_column and column >= 1:
				column_data = sheet.col_values(column-1)

		return column_data

	def get_merged_cell(self,sheet,row,column):
		'''
		@summary get merged cell data
		:param sheet:
		:param row:
		:param column:
		:return:
		'''
		pass


class ExcelWriter(object):
	pass

def read_excel():
	sheet_name = 'Sheet1'
	current_dir = os.path.join(os.path.dirname(__file__),'files')
	file_path = current_dir + r"\testcases.xls"
	reader = ExcelReader(file_path)
	# sheet = reader.get_sheet_object(sheet_name=sheet_name)  #get sheet by sheet name
	sheet = reader.get_sheet_object(sheet_index=1)    # get sheet by sheet index
	print reader.get_cell(sheet,1,1)  #get cell value
	print reader.get_cell_type(sheet,1,1)  # get cell type
	print reader.get_row(sheet,1)  # get row data
	print reader.get_column(sheet,1)  # get column data
	print reader.get_date_from_cell(sheet,1,1)  # get date from cell

if __name__ == "__main__":
	read_excel()
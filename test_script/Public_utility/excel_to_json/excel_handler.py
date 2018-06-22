#!/usr/bin/env python
# encoding: utf-8
'''
Create a excel handler to read and write excel file
@author: YQY
@change: 2018-05-22 create script, add excel reader
@change: 2018-05-23 add new function to get sheet by index
@change: 2018-05-28 add new function to write excel and delete data
'''


import time
import os
# import platform
try:
	import xlrd
except:
	os.system("pip install xlrd")
	import xlrd
try:
	import xlwt
except:
	os.system("pip install xlwt")
	import xlwt
try:
	from xlutils.copy import copy
except:
	os.system("pip install xlutils")
	from xlutils.copy import copy
# if 'Windows' == platform.system():
# 	try:
# 		import win32com.client
# 	except:
# 		os.system("sudo -H pip install pywin32")
# 		import win32com.client

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
		current_time=''

		if isinstance(date,tuple):
			current_time = str(date[0])+"-" +str(date[1])+"-"+str(date[2])+" "+str(date[3])+":"+str(date[4])+":"+str(date[5])
			print current_time
			result =  time.strptime(current_time,"%Y-%m-%d %H:%M:%S")

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
		:param row:  if get merged
		:param column:
		:return:
		'''
		cell_data = None

		if isinstance(sheet,object):
			total_row = self._get_row_count(sheet)
			total_column = self._get_column_count(sheet)
			if row <= total_row and column <= total_column and row >= 1 and column >= 1:
				cell_data = sheet.row_values(row - 1)[column-1]  # -1 for read excel data start from index 0,0

		return cell_data


class ExcelWriter(object):
	def __init__(self,file_path):
		self.file_path = file_path
		self.workbook = xlwt.Workbook()

	def set_style(self,name, height, bold=False):
		style = xlwt.XFStyle()  # 初始化样式
		font = xlwt.Font()  # 为样式创建字体
		font.name = name  # 'Times New Roman'
		font.bold = bold
		font.color_index = 8
		font.height = height
		borders= xlwt.Borders() # 创建单元格边框样式
		borders.left= 6
		borders.right= 6
		borders.top= 6
		borders.bottom= 6

		style.font = font
		style.borders = borders

		return style

	def create_sheet(self,sheet_name):
		'''
		@summary create sheet
		:param sheet_name:
		:return:
		'''
		sheet = None

		if sheet_name: # if sheet name not exist, create sheet
			sheet = self.workbook.add_sheet(sheet_name, cell_overwrite_ok=True)

		return sheet

	def copy_exist_excel(self,sheet_name):
		'''
		@summary: read old excel workbook and copy as a new workbook
		:param sheet_name:
		:return: sheet object
		'''
		sheet = None
		new_workbook = None

		if os.path.exists(self.file_path):
			old_workbook = xlrd.open_workbook(self.file_path)  # read old excel workbook and copy as a new workbook
			new_workbook = copy(old_workbook)
			sheet = new_workbook.get_sheet(sheet_name)

		return sheet,new_workbook

	def create_new_excel(self,sheet_name):
		'''
		@summary create new workbook and sheet
		:param sheet_name:
		:return:
		'''
		sheet = None
		new_workbook = None

		if not os.path.exists(self.file_path):
			new_workbook = xlwt.Workbook()
			sheet = new_workbook.add_sheet(sheet_name)

		return sheet,new_workbook

	def write_cell(self,sheet_name, data='', row=0, column=0, is_clear = False):
		'''
		@summary write cell data, new or overwrite
		@param: is_clear, false add data to cell, True clear cell
		'''
		sheet = None
		new_workbook = None

		if os.path.exists(self.file_path):  # copy old workbook if excel file exist
			sheet,workbook = self.copy_exist_excel(sheet_name)
		else:   # create a new workbook and new sheet if excel file doesn't exist
			sheet,workbook = self.create_new_excel(sheet_name)

		if sheet and workbook and row>0 and column>0:
			try:
				if not is_clear:
					sheet.write(row-1,column-1,data,self.set_style('Arial',220,True)) # write excel
				elif is_clear:
					sheet.write(row - 1,column - 1,data) # used for clear cell value
				workbook.save(self.file_path)
			except Exception as e:
				print 'Write sheet failed for: {0}'.format(e)

	def write_row(self,sheet_name,data_list, row):
		'''
		@summary write row
		:param data_list:
		:param row:
		:return:
		'''
		if data_list and row>0 and sheet_name:
			for i in range(len(data_list)):
				column = i+1
				self.write_cell(sheet_name,data_list[i],row,column)

	def write_column(self,sheet_name,data_list,column):
		'''
		@summary:write column
		:param sheet_name:
		:param data_list:
		:param column:
		:return:
		'''
		if data_list and column>0 and sheet_name:
			for i in range(len(data_list)):
				row = i+1
				self.write_cell(sheet_name,data_list[i],row,column)

	def clear_cell(self,sheet_name,row,column):
		'''
		@summary: clear data in cell
		:param sheet_name:
		:param row:
		:param column:
		:return:
		'''
		self.write_cell(sheet_name,row=row,column=column,is_clear=True)

	def clear_row(self,sheet_name,row, column):
		'''
		@summary: clear specifiled row's data, end at column number
		:param sheet_name:
		:param row:
		:param column:
		:return:
		'''
		for i in range(column):
			self.write_cell(sheet_name,row=row,column=i,is_clear=True)

	def clear_column(self,sheet_name,row, column):
		'''
		@summary clear specifiled columns' data, end at row number
		:param sheet_name:
		:param row:
		:param column:
		:return:
		'''
		for i in range(row):
			self.write_cell(sheet_name,row=i,column=column,is_clear=True)

	def merge_cell(self,row,column):
		pass

	def delete_row(self,sheet_name,row):
		pass
		# if os.path.exists(self.file_path):
		# 	if sheet_name and row >0:
		# 		sheet = win32com.client.Dispatch('Excel.Application').Workbooks.Open(self.file_path).Worksheets(sheet_name)
		# 		sheet.Rows(row-1).Delete()

	def delete_column(self,column):
		pass

def write_excel():
	'''
	@summary all method examples for write excel
	:return:
	'''
	sheet_name = 'Sheet1'
	current_dir = os.path.join(os.path.dirname(__file__),'files')
	file_path = current_dir + r"\testdata.xls"
	writer = ExcelWriter(file_path)
	writer.write_cell(sheet_name, data='teaaaaaaaaaaast', row=8, column=1) # write a single cell
	writer.write_row(sheet_name,[1,2,3,4,5,6],row=4)  # write a whole row
	writer.write_column(sheet_name,[1,2,3,4,5,6],column=4)  # write a whole column
	writer.clear_cell(sheet_name,4,4) # clear cell data
	writer.clear_row(sheet_name,4, 4) # clear specifiled row and column
	writer.clear_column(sheet_name,4,4)

def read_excel():
	'''
	@summary read excel's all method, 空行或空列会导致它后面有数据的行或列的下标少一个
	'''
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
	print reader.get_merged_cell(sheet,8,5)  # get merged cell data

if __name__ == "__main__":
	read_excel()
	write_excel()
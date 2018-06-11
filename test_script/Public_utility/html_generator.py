#!/usr/bin/env python
# encoding: utf-8
'''
public function to create html page
@author: YQY
@change: 2018-03-16 create script
@change: 2018-05-24 add function to allow create table which contain unlimited rows
'''
import os
import time

import all_config

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

class HtmlGenerator(object):
	def __init__(self):
		pass

	def create_tr(self, name_list=[], value_list=[], height=40, is_tr=True):
		'''
		@summary: create tr or th or create both tr and th
		'''
		tmp_table = ""
		if value_list and not name_list:
			tmp_table += '<tr>'
			if is_tr:  # create TR
				for value in value_list:
					tmp_table += '<td height=\"{0}px\" <div align=\"center\">{1}</td>'.format(height, value)
			else:  # create TH
				for value in value_list:
					tmp_table += '<th height=\"{0}px\" <div align=\"center\">{1}</th>'.format(height, value)
			tmp_table += "</tr>"
		elif value_list and len(value_list) == len(name_list):  #create two row, first is header,second is value
			tmp_table += '<tr>'
			for name in name_list:
				tmp_table += '<th height=\"{0}px\" <div align=\"center\">{1}</th>'.format(height, name)
			tmp_table += "</tr>"
			tmp_table += "<tr>"
			for value in value_list:
				tmp_table += '<td height=\"{0}px\" <div align=\"center\">{1}</td>'.format(height, value)
			tmp_table += "</tr>"
		elif isinstance(value_list[0], list): # create mutiple rows
			tmp_table += '<tr>'
			for name in name_list:
				tmp_table += '<th height=\"{0}px\" <div align=\"left\">{1}</th>'.format(height, name)
			tmp_table += "</tr>"
			for row in value_list:
				tmp_table += "<tr>"
				for value in row:
						tmp_table += '<td height=\"{0}px\" <div align=\"left\">{1}</td>'.format(height, value)
				tmp_table += "</tr>"
		return tmp_table

	def create_html(self, title, value_list, name_list=[]):
		'''
		@summary: create html page
		'''
		if value_list:
			current_date = time.strftime('%Y%m%d')
			current_time = time.strftime('%Y%m%d%H%M')
			folder = os.path.join(CURRENT_DIR, current_date )
			if not os.path.exists(folder):
				os.makedirs(folder)
			result_html = os.path.join(folder, '{0}_{1}.html'.format(title, current_time))
			tmp_table = '<br>'
			tmp_table += '<table border="{0}" width=\"{1}px\">'.format(all_config.BORDER,all_config.TABLE_WIDTH)
			tmp_table += self.create_tr(name_list=name_list,value_list=value_list,height=all_config.TD_HEIGHT)
			tmp_table += '</table>'
			tmp_table += '<br>'
			with open(result_html, 'a') as f:
				f.writelines(tmp_table)
				print 'genereated html: {0}'.format(result_html)

if __name__ == '__main__':
	pass

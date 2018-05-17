#!/usr/bin/env python
# encoding: utf-8
'''
public function to create html page
@author: YQY
@change: 2018-03-16 create script
@change: 2018-03-30 add function to generate time statistics table
'''
import os

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
		elif value_list and len(value_list) == len(name_list):
			tmp_table += '<tr>'
			for name in name_list:
				tmp_table += '<th height=\"{0}px\" <div align=\"center\">{1}</th>'.format(height, name)
			tmp_table += "</tr>"
			tmp_table += "<tr>"
			for value in value_list:
				tmp_table += '<td height=\"{0}px\" <div align=\"center\">{1}</td>'.format(height, value)
			tmp_table += "</tr>"

		return tmp_table

	def create_html(self, scenario, title, current_date, value_list, name_list=[], current_round=''):
		'''
		@summary: create html page
		'''
		if 0 < len(value_list):
			folder = os.path.join(CURRENT_DIR, current_date + '/' + scenario)
			if not os.path.exists(folder):
				os.makedirs(folder)
			scenario_html = os.path.join(folder, '{0}_{1}_{2}.html'.format(scenario, title, current_date))
			tmp_table = ''
			if '' != current_round:
				tmp_table += '####### {0} round{1} statistics  #######'.format(scenario, current_round)

			tmp_table += '<table border="1" width=\"800px\">'
			tmp_table += self.create_tr(name_list=name_list, value_list=value_list)
			tmp_table += '</table>'
			tmp_table += ''
			with open(scenario_html, 'a') as f:
				f.writelines(tmp_table)
				print 'genereated html: {0}'.format(scenario_html)

def check_file_existence(self, scenario, current_date, source_file_path):
	'''
	@summary: check whether html file exist in specified path
	'''
	file_path = ''
	target_folder = os.path.join(source_file_path, current_date)
	target_file = '{0}_processing_time_{1}.html'.format(scenario, current_date)
	for root, dir, files in os.walk(target_folder):
		for file in files:
			if file == target_file:
				file_path = os.path.join(root, file)
				break

	return file_path


if __name__ == '__main__':
	pass

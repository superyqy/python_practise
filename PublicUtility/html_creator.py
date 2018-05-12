#!/usr/bin/env python
# encoding: utf-8
'''
Create table for html page
@author: Xiuwen Yin
@change: 2017-12-08 create script
'''
import sys
import os
import time
import re
import json

class HTMLCreator(object):
    def __init__(self, source_folder=''):
        self.source_folder = source_folder
        self.current_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        self.result_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'CI_RESULT_{0}.html'.format(self.current_time))
        self.color = 'black'
        self.td_height = '40'
    
    def find_files(self, file_type):
        '''
        @summary: find file
        '''
        db_regex = re.compile(r'^db_statistics_\d+.txt$')
        slam_regx = re.compile(r'^vehicle_quality_summary\.json$')
        result_file = ''
        if 'db' == file_type:
            regx = db_regex
        elif 'vehicle' == file_type:
            regx = slam_regx
        if os.path.exists(self.source_folder):
                for root, dir, files in os.walk(self.source_folder):
                    for file in files:
                        if regx.match(file):
                            result_file = os.path.join(root, file)
                            break
        return result_file
     
    def read_file(self, file_path):
        '''
        @summary: 
        '''
        data = ''
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                if not data.endswith('.json'):
                    data = f.readlines()
                else:
                    data = json.loads(f.read())
        return data
        
        
                
    def create_tr_info(self, module, info):
        '''
        @summary: create table's header 
        '''
        tmp_table = ""    
        tmp_table += ("<tr><th rowspan=%s width=\"16%%\">%s</th><td colspan=\"2\" width=\"84%%\" height=\"" + 
                              self.td_height + "px\"><div style=\"margin-left:10px;\">%s</td></tr>") % (1, module, info)
        return tmp_table
    

    def create_tr_large_scale(self, module, name_list, num_list):
        '''
        @summary: Create table cell and row for statistics
        '''
        tmp_table = ""
        for i in range(0, len(name_list)):
            if i == 0 :
                tmp_table += ("<tr><th rowspan=%s width=\"16%%\">%s</th><td width=\"42%%\" height=\"" + 
                              self.td_height + "px\"><div style=\"margin-left:10px;\">%s</td><td width=\"42%%\" height=\"" + 
                              self.td_height + "px\"><font color=\"%s\"><div align=\"center\">%s</font></td></tr>") % (str(len(name_list)), module, name_list[i], self.color, num_list[i])
            else:
                tmp_table += ("<tr><td width=\"42%%\" height=\"" + self.td_height + "px\"><div style=\"margin-left:10px;\">%s</td><td width=\"42%%\" height=\"" + 
                              self.td_height + "px\"><font color=\"%s\"><div align=\"center\">%s</font></td></tr>") % (name_list[i], self.color, num_list[i])
        return tmp_table
    
    def create_vehicle_slam_statistics_result(self):
        '''
        @summary: create vehicle slam quality result
        '''
        tmp_table = ''  # store html's table
        data = ''  # store db statistic source data
        key_list = []  # store title name
        value_list = []  # store data value 
        result_file = self.find_files('vehicle')
        if '' != result_file:
            data = self.read_file(result_file)
        
        
        
    def create_db_statistics_result(self):
        '''
        @summary: create database's statistic result
        '''
        tmp_table = ''  # store html's table
        data = ''  # store db statistic source data
        key_list = []  # store title name
        value_list = []  # store data value 
        result_file = self.find_files('db')
        if '' != result_file:
            data = sorted(self.read_file(result_file), reverse=True)
        for row in data:
            if '' != row and ":" in row:
                row = row.split(":")
                title = ''  # initial title
                value = ''  # intial value
                if 3 == len(row):
                    title = row[0] + ': ' + row[1]
                    value = row[2]
                elif 2 == len(row):
                    title = row[0]
                    value = row[1]  
                key_list.append(title)
                value_list.append(value)
    
        tmp_table = "<br><br><b>Server database statistics</b><br>"
        tmp_table += '<table border="1" width=\"700px\" >'
        tmp_table += '<tr><th></th><th>Stages& Code</th><th>Total Count</th><tr>'
        tmp_table += self.create_tr_large_scale('Database result', key_list, value_list)
        tmp_table += "</table>"
        
        return tmp_table
    
    def create_large_scale_regression_results(self):
        title_list = []
        result_list = []
        tmp_table = ""
        currenctDir = os.getcwd()
        
        if os.path.exists(currenctDir + "/largeScale_returnCode_statistics.txt"):
            regression_results_file = open(currenctDir + "/largeScale_returnCode_statistics.txt")
            regression_results_list = regression_results_file.read()
            result_split = regression_results_list.split('#')
            for result in result_split:
                split_list = result.split(':')
                title = split_list[0].strip()
                title = title.strip("\'")
                if "Servercordump" in title:
                    title_list.append("CoreDump count")
                if "slam" in split_list[1] or "loc" in split_list[1] or "sdor" in split_list[1]:
                    result_list.append("snippet count: " + split_list[1].strip("\'"))
                else:
                    result_list.append(split_list[1].strip("\'"))
                
            tmp_table = "<br><br><b>Server statistic of large-scale E2E test-date: %s </b><br>" % date
            tmp_table += '<table border="1" width=\"700px\" >'
            tmp_table += '<tr><th></th><th>Device/ Type</th><th>ReturnCode/ SnippetCount</th><tr>'
            tmp_table += self.create_tr_large_scale("Regression Results", title_list, result_list)
            info = "Snippets: /opt/ygomi/roadDB/file_storage/events/uploads<br>" 
            info += "Server Core Dump: /opt/ygomi/roadDB/log/CoreDumpFile<br>"
            info += "ReturnCode: /opt/ygomi/roadDB/file_storage/log<br>"
            tmp_table += self.create_tr_info("Path", info)
            tmp_table += "</table>"
        return tmp_table
    
    def merge_html(self):          
        '''
        @summary: 
        '''
        merge_page = ''
#         merge_page = '<table border="1" width=\"600px\" >'
        merge_page += self.create_db_statistics_result()
#                 merge_page += '</table>'
        with open(self.result_file, "w+") as merge_file:
            merge_file.writelines(merge_page)

    
if __name__ == '__main__':
#     branch = sys.argv[1]
#     merge_html("returncode_%s.html" % branch)
    html_creator = HTMLCreator(source_folder='/home/shawn/workspace/tmpdata')
    html_creator.create_vehicle_slam_statistics_result()
#     html_creator.merge_html()
    pass
    
    

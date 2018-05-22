#!/usr/bin/env python
# encoding: utf-8
'''
auto send email to specified email receiver
@author: YQY
@change: 2018-05-12 create email script
@change: 2018-05-13 add basic functions for email server
'''

import os
import time
import configparser
import smtplib
import shutil
import platform
from email.mime.text import MIMEText
from email.header import Header

CURRENT_DIR = os.path.dirname(__file__) # get current script's path
if 'Windows' == platform.system():
	CURRENT_DIR = CURRENT_DIR.replace("/", "\\")

class EmailSender(object):
	def __init__(self, sender, username, password, email_from, email_path=r'D:\tmpdata', email_server='smtp.qq.com',port='465'):
		self.sender = sender
		self.email_path = email_path
		self.email_server = email_server
		self.email_from = email_from
		self.username = username
		self.password = password
		self.port = port

	def search_email_and_send(self):
		'''
		@summary: search email path for email file and send email
		'''
		if os.path.exists(self.email_path):
			files = os.listdir(self.email_path)
			for file in files:
				summary, branch, email_to_list = self._match_email_config(file)
				if email_to_list:
					subject = "{0}_{1}".format(summary + "_" + branch, time.strftime('%Y-%m-%d_%H:%M:%S'))
					content = self._read_file_content(os.path.join(self.email_path, file))
					self._send_email(content, subject, email_to_list)
					self._move_sent_mail_to_backup_folder(os.path.join(self.email_path, file))


	def _move_sent_mail_to_backup_folder(self, email_file):
		'''
		@summary: move sent mail to backup folder
		'''
		backup_path=os.path.join(CURRENT_DIR, 'sent_backup')
		if not os.path.exists(backup_path): # create backup folder if not exist
			os.makedirs(backup_path)
		if os.path.exists(email_file): # backup email file
			email_name=email_file.split(".")
			email_new_name = email_name[0] + "_" + time.strftime('%Y%m%d%H%M%S') + "." + email_name[1]
			os.rename(email_file, email_new_name) # rename sent email
			shutil.move(email_new_name, backup_path) # move email to backup path

	def _read_file_content(self,email_file,read_type='r'):
		'''
		@summary read file content for email html or attachment image
		'''
		file_content=''

		if os.path.exists(email_file):
			with open(email_file,read_type) as f:
				file_content = f.read()

		return file_content

	def _match_email_config(self, email_file):
		'''
		@summary: analyze email file to get branch and receiver group
		@param email_file:
		@return string summary
		@return: string branch
		@return: list receiver group
		'''
		summary=''
		branch=''
		email_to_list=[]
		email_to_groups = ['group1','group2']

		# read emailconf.ini
		email_config_path = os.path.join(CURRENT_DIR, os.path.join('config','email_config.ini'))
		conf = configparser.ConfigParser()
		#config_file_last_modify = os.path.getmtime(email_config_path)
		conf.read(email_config_path)

		if '_' in email_file:
			name = email_file.split('.')[0].split('_')
			receiver_group=''
			if 3==len(name):
				summary=name[0]
				branch = name[1]
				receiver_group = name[2]
			elif 2==len(name):
				summary = name[0]
				receiver_group = name[1]
			if receiver_group in email_to_groups:
				email_to_list = conf.get('mail',receiver_group).split(';')

		return summary, branch, email_to_list

	def _send_email(self,email_body,subject,email_receiver_list):
		'''
		@summary: send email with smtp protocol
		:param email_body:
		:param subject:
		:param email_receiver_list:
		:return:
		'''
		msg = MIMEText(email_body,'html','utf-8')
		msg['Subject'] = Header(subject,'utf-8')
		msg['From'] = Header(self.email_from, 'utf-8')
		# smtp =smtplib.SMTP()
		smtp=smtplib.SMTP_SSL(self.email_server, self.port)
		smtp.connect(self.email_server)
		smtp.login(self.username,self.password)
		smtp.sendmail(self.sender, email_receiver_list, msg.as_string())
		smtp.quit()

def run_email_server(sender, username, password,email_from):
	'''
	@sumary: run email server
	'''
	email_sender = EmailSender(sender=sender, username=username, password=password, email_from=email_from)
	while 1:
		email_sender.search_email_and_send()
		time.sleep(60)

if __name__ == "__main__":
	sender='XXXXXXXX@qq.com'
	email_from='XXX Email Server'
	username='XXXXXXXX@qq.com'
	password='XXXXXXXX'
	run_email_server(sender, username, password, email_from)

#!/usr/bin/env python
# encoding: utf-8
'''
Search mysql database with sql command
@author: YQY
@change: 2017-11-30 create script
@change: 2018-05-16 modify execute command's logic
'''
import logging
import os
try:
    import MySQLdb
except:
    os.system('sudo -H pip install mysql-python')
    import MySQLdb

class MySqlReader(object):
    def __init__(self, hostname, user, password, db_name):
        '''
        @summary: init params for mysql 
        @param hostname: string hostname for mysql database
        @param user: string username for login mysql database
        @param password: string password for login mysql database
        @param db_name: string database name for operation    
        '''
        self.hostname = hostname
        self.user = user
        self.password = password
        self.db_name = db_name
        self.logger = logging.getLogger("CI")
        
    def connect(self):
        '''
        @summary: create a connection
        '''
        conn = None

        try:
            conn = MySQLdb.connect(self.hostname, self.user, self.password, self.db_name)
        except Exception as e:
            self.logger.error('connect to mysql server failed: {0}'.format(e))
        
        return conn    
    
    def check_mysql_table_existence(self, database='', table=''):
        '''
        @summary: check whether database or table is exist
        '''

        result_db = self.execute_command("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{0}'".format(database))
        
        if 0 < int(result_db[0][0]):
            if '' == table:  # check database only
                return True
            else:  # check table
                result_table = self.mysql_operator.execute_command("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{0}' AND table_name='{1}'".format(database, table))
                if 1 == int(result_table[0][0]):
                    return True
                        
        return False
    
    def execute_command(self, command):
        '''
        @summary: execute sql command in  mysql DB
        '''
        result = ()
        conn = self.connect()
        cursor = None
        operate_type ='SELECT'
        if not command.upper().startswith('SELECT'):
            operate_type = 'OTHER'
        self.logger.info("Execute command: {0}".format(command))

        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute(command)
                if 'OTHER' == operate_type:
                    conn.commit()
                else:
                    result = cursor.fetchall()
                    return result
                # affect_row = cursor.rowcount
            except Exception as e:
                if 'SELECT' != operate_type.lower():
                    conn.rollback()
                self.logger.error("Execute command: {0} failed for: {1}".format(command,e))
            finally:
                cursor.close()
                conn.close()

    def create_table(self):
        '''
        @summary： create table
        '''
        #below database set  is compatible to chinese character
        database = """CREATE DATABASE ci_db
        CHARACTER SET 'utf8'       
        COLLATE 'utf8_general_ci';
        """

        table = """CREATE TABLE EMPLOYEE (
                 FIRST_NAME  CHAR(20) NOT NULL,
                 LAST_NAME  CHAR(20),
                 AGE INT,  
                 SEX CHAR(1),
                 INCOME FLOAT )"""
        pass

if __name__ == '__main__':
    pass
    

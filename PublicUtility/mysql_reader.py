#!/usr/bin/env python
# encoding: utf-8
'''
Search mysql database with sql command
@author: Xiuwen Yin
@change: 2017-11-30 create script
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
            self.logger.error('connect to mysql database failed: {0}'.format(e))
        
        return conn    
    
    def check_mysql_table_existence(self, database='', table=''):
        '''
        @summary: check whether database or table is exist
        '''
        result_db = self.get_result_from_db("select count(*) from information_schema.tables where table_schema='{0}'".format(database)) 
        
        if 0 < int(result_db[0][0]):
            if '' == table:  # check database only
                return True
            else:  # check table
                result_table = self.mysql_operator.get_result_from_db("select count(*) from information_schema.tables where table_schema='{0}' and table_name='{1}'".format(database, table))
                if 1 == int(result_table[0][0]):
                    return True
                        
        return False
    
    def get_result_from_db(self, command):
        '''
        @summary: query mysql DB
        '''
        result = []
        conn = self.connect()
        if conn != None:
            cursor = conn.cursor()  # create cursor
            try:
                cursor.execute(command)  # execute sql command
                result = cursor.fetchall()  # fetch result
            except Exception as e:
                self.logger.error('execute command {0} failed for: {1}'.format(command, e))
            finally:  # release cursor and connection
                cursor.close()
                conn.close()
        return result   
            
if __name__ == '__main__':
    pass
    

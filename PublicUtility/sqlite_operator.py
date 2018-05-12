#!/usr/bin/env python
# encoding: utf-8
'''
@summary: sqlite3 operator
@author: Xiuwen Yin
@change: 2018-02-7 create script
'''
import os
import sqlite3
import set_logging

class SqliteOperator(object):
    def __init__(self, db_name='sqlite.db'):
        self.sqlite_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database/' + db_name)
        self.create_folder()
        self.logger = set_logging.set_logging('sqlite_operator')
    
    def create_folder(self):
        '''
        @summary: create folder to store sqlite db
        '''
        if not os.path.exists(os.path.dirname(self.sqlite_db)):
            os.makedirs(os.path.dirname(self.sqlite_db))
             
    def connection(self):
        '''
        @summary: create a connection
        '''
        conn = None
        self.logger.info("create sqlite connection")
        
        try:
            conn = sqlite3.connect(self.sqlite_db)
        except Exception as e:
            self.logger.error('connect to sqlite database failed: {0}'.format(e))
        
        return conn  
    
    def check_table_row_existence(self, table_name, filed_dictionary):
        '''
        @summary: check whether specifiled condition's row exist
        '''
        is_exist = False
        result = ()
        
        self.logger.info("Check whether table's row exist")
        
        if 0 < len(filed_dictionary.keys()):
            search_condition = ''
            for key in filed_dictionary.keys():
                search_condition += key + "='" + filed_dictionary[key] + "' AND "
            search_condition = search_condition.rstrip('AND ')
            row_exist_command = "SELECT COUNT(*) FROM {0} WHERE {1}".format(table_name, search_condition)

            result = self.execute_command(row_exist_command)

        if 0 < len(result):
            if 0 < result[0][0]:
                is_exist = True
                
        return is_exist
    
    def check_sqlite_table_existence(self, table_name):
        '''
        @summary: check whether table exist
        '''
        is_exist = False
        
        self.logger.info("Check whether sqlite table exist")
        
        table_exist_command = "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='{0}'".format(table_name)
        result = self.execute_command(table_exist_command)

        if 0 < len(result):
            if 1 == result[0][0]:
                is_exist = True
                
        return is_exist
    
    def execute_command(self, command, operate_type='query'):
        '''
        @summary: query data from db file
        '''
        result = []
        
        self.logger.info("Execute command: {0}".format(command))
        conn = self.connection()
        cursor = None
        
        if None != conn:
            try:
                cursor = conn.cursor()
                cursor.execute(command)
                if operate_type.lower() in ['insert', 'update', 'delete', 'create', 'drop']:  
                    conn.commit()
                else:
                    result = cursor.fetchall()
                    return result
            except Exception as e:
                if 'query' != operate_type.lower():
                    conn.rollback()
                self.logger.error(e)
            finally:
                cursor.close()
                conn.close()
        
    def create_table(self, table_name, create_table_command):
        '''
        @summary: create table
        '''
        if not self.check_sqlite_table_existence(table_name):  # table should not exist 
            self.execute_command(create_table_command, operate_type='create')
    
    def check_foreign_key_constraint(self, foreign_key_value, referenced_table, referenced_filed):
        '''
        @summary: check whether foreign key value exist in referenced table
        '''
        is_exist = False
        
        if '' != foreign_key_value and '' != referenced_filed and self.check_sqlite_table_existence(referenced_table):
            result = self.execute_command("SELECT COUNT(*) FROM {0} WHERE {1}='{2}'".format(referenced_table, referenced_filed, foreign_key_value))
            if 0 < len(result):
                if 1 == result[0][0]:
                    is_exist = True
        
        return is_exist
                
def create_all_tables(database_name, single_table_name=''):
    '''
    @summary: create all tables if db not exist
    '''
    command_summary = '''CREATE TABLE snippets_summary
    (version TEXT PRIMARY KEY NOT NULL,
    created_date TEXT NOT NULL,
    slam_total_count INTEGER,
    slam_total_length REAL,
    slam_avg_length REAL,
    incr_slam_total_count INTEGER,
    incr_slam_total_length REAL,
    incr_slam_avg_length REAL,
    rt_total_count INTEGER,
    rt_total_length REAL,
    rt_avg_length REAL,
    sdor_total_count INTEGER,
    sdor_total_length REAL,
    sdor_avg_length REAL)'''
    
    command_snippets = '''CREATE TABLE snippets_detail
      (id INTEGER PRIMARY KEY autoincrement, 
       snippet_type TEXT NOT NULL,
       snippet_name TEXT NOT NULL, 
       snippet_length REAL, 
       affect_divisions TEXT,
       snippet_version TEXT NOT NULL,
       FOREIGN KEY(snippet_version) REFERENCES snippets_summary(version))'''
    
    command_server = '''CREATE TABLE server_detail
    (id INTEGER PRIMARY KEY autoincrement, 
     logic_road_line_total_length REAL,
     logic_road_line_ratio TEXT,
     theoretical_logic_road_line_total_length REAL,
     server_version TEXT NOT NULL,
     FOREIGN KEY(server_version) REFERENCES snippets_summary(version))'''

    command_history_best = '''CREATE TABLE best_in_history_logic_road_line 
    (best_history_logic_road_line_total_length TEXT NOT NULL,
    best_history_logic_road_line_ratio TEXT NOT NULL,
    version TEXT NOT NULL,
    update_time TEXT NOT NULL,
    branch TEXT NOT NULL
    )'''
    
    command_time_statistics = '''CREATE TABLE time_statistics
    (time_version TEXT NOT NULL,
    update_time TEXT NOT NULL,
    current_round TEXT NOT NULL,
    total_worktime_server_framework TEXT,
    rdb_server_genLogicDB_cmd TEXT,
    rdb_server_snippetAnalyzer_cmd TEXT,
    rdb_server_foregroundDBMerger_cmd TEXT,
    rdb_server_vehicleDBGenerate_cmd TEXT,
    offline_tool_backendDB_import TEXT,
    total_worktime_server_algo TEXT,
    repairDivision TEXT,
    rdbMasterInfoExtractor TEXT,
    logicInfoExtractor TEXT,
    foregroundDBMerger TEXT,
    vehicleDBGenerator TEXT,
    foregroundDBUpdater TEXT,
    rdbDataExtractor TEXT,
    snippetAnalyzer TEXT,
    total_worktime_vehicle TEXT,
    SLAM TEXT,
    SDOR TEXT,
    PRIMARY KEY(time_version, current_round),
    FOREIGN KEY(time_version) REFERENCES snippets_summary(version)
    )
    '''
    
    command_rf_elapsed_time = '''CREATE TABLE robotframework_testcase_elapsed_time
    (rf_version TEXT NOT NULL,
    branch TEXT NOT NULL,
    scenario TEXT NOT NULL,
    elapsed_time TEXT NOT NULL,
    PRIMARY KEY(rf_version, scenario),
    FOREIGN KEY(rf_version) REFERENCES snippets_summary(version)
    )
    '''
    
    
    table_dict = {'snippets_summary': command_summary, 'snippets_detail':command_snippets, 'server_detail': command_server, 'best_in_history_logic_road_line': command_history_best, 'time_statistics': command_time_statistics, 'robotframework_testcase_elapsed_time':command_rf_elapsed_time}
    
    sqlite = SqliteOperator(database_name)
    if '' == single_table_name:  # create all table
        for key in table_dict:
            sqlite.create_table(key, table_dict[key])
    elif single_table_name in table_dict.keys():  # create specifiled table
        sqlite.create_table(single_table_name, table_dict[single_table_name])
    
def query_database(table, database_name, query_condition={}):
    '''
    @summary: query database
    '''
    result = []
    
    sqlite = SqliteOperator(database_name)
    if 0 == len(query_condition.keys()):
        command = 'SELECT * FROM {0}'.format(table)
    else:
        search_condition = ''
        for key in query_condition.keys():
            search_condition += key + "='" + query_condition[key] + "' AND "
        search_condition = search_condition.rstrip('AND ')
        command = 'SELECT * FROM {0} WHERE {1}'.format(table, search_condition)
    
    result = sqlite.execute_command(command)
        
    return result

def insert_data_into_database_without_constraint(database_name, table, data=[]):
    '''
    @summary: insert data into database which has no constraint
    '''
    sqlite = SqliteOperator(database_name)
    
    if '' != table and 0 < len(data):
        if sqlite.check_sqlite_table_existence(table):
            values = "','".join(data[:])
            values = "'" + values + "'"
            command = '''INSERT INTO {0} values({1})'''.format(table, values)
            print command
            sqlite.execute_command(command, 'insert')
            
def insert_data_into_database_with_constraint(database_name, table, foreign_key_value, referenced_table, referenced_filed, data_list):
    '''
    @summary: insert data into database whic has constraint
    '''
    sqlite = SqliteOperator(database_name)
    
    if '' != table and 0 < len(data_list):
        if sqlite.check_sqlite_table_existence(table):
            if sqlite.check_foreign_key_constraint(foreign_key_value, referenced_table, referenced_filed):
                
                if data_list[0] is None:
                    values = "','".join(data_list[1:])
                    values = "'" + values + "'"
                    command = '''INSERT INTO {0} values(NULL,{1})'''.format(table, values)
                else:
                    values = "','".join(data_list[:])
                    values = "'" + values + "'"
                    command = '''INSERT INTO {0} values({1})'''.format(table, values)
                print 'Start insert for database {0} table {1}: {2}'.format(database_name, table, command)
                sqlite.execute_command(command, 'insert')
            else:
                print 'referenced foreign key value [{0}] does not exist in table [{1}], can not insert data!'.format(referenced_filed, referenced_table)
    
def delete_data_from_table(database_name, table_name, filed_name='', value=''):
    '''
    @summary: delete table row
    '''
    command = ''

    sqlite = SqliteOperator(database_name)
    if sqlite.check_sqlite_table_existence(table_name):
        if '' == filed_name:
            command = 'DELETE FROM {0}'.format(table_name)
        elif '' != filed_name and '' != value:
            command = 'DELETE FROM {0} WHERE {1} ="{2}"'.format(table_name, filed_name, value)
    sqlite.execute_command(command, operate_type='delete')

def update_table(database_name, table_name, original_dictionary, update_dictionary):
    '''
    @summary: update table
    '''
    command = ''
    update_condition = ''
    update_value = ''
    
    sqlite = SqliteOperator(database_name)
    if sqlite.check_sqlite_table_existence(table_name):         
        if sqlite.check_table_row_existence(table_name, original_dictionary):
            if 0 < len(update_dictionary.keys()):
                update_value = ''
                for key in update_dictionary.keys():
                    update_value += key + "='" + update_dictionary[key] + "',"
                update_value = update_value.rstrip(',')
            if 0 < len(original_dictionary.keys()):
                update_condition = ''
                for key in original_dictionary.keys():
                    update_condition += key + "='" + original_dictionary[key] + "' AND "
                update_condition = update_condition.rstrip('AND ')
                
            command = 'UPDATE {0} SET {1} WHERE {2}'.format(table_name, update_value, update_condition)
            sqlite.execute_command(command, operate_type='update')
            

if __name__ == "__main__":
    pass
#     database_name = 'CI_ccdemo.db'  # set database name
#################examples#################################
#     create_all_tables(database_name)  # create all tables
    
#     query_condition = {'version':'2.3.0.5', 'slam_total_count':'100000'}  # query database with condition
#     print query_database('snippets_summary', database_name, query_condition)
    
#     print query_database('snippets_summary', database_name)  # query specifiled table all data

#     insert_data_into_database_without_constraint(database_name, 'snippets_summary', '2.3.0.5', '22.15', '30', '4466.5', '12', '21231232.15', '10', '66232.15', '4')

#     insert_data_into_database_with_constraint(database_name, 'snippets_detail', '2.3.0.5', 'snippets_summary', 'version', None, 'SLAM', 'rdb-2017-12-11-device03-slam.out', '2222222344442.22', '1234534544,55443537211', '2.3.0.5')

#     delete_data_from_table(database_name, 'snippets_summary')  # delete all data
#     delete_data_from_table(database_name, 'snippets_summary', filed_name='version', value='2.3.0.5')  # delete specifiled data
     
#     original_dictionary = {'version':'2.3.0.5', 'slam_total_count':'30'}  # update table specifiled row data
#     update_dictionary = {'slam_total_count':'100000', 'slam_total_length':'200000'}
#     update_table(database_name, 'snippets_summary', original_dictionary, update_dictionary)
##########################################################

    

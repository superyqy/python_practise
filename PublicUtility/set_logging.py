#!/usr/bin/env python
# encoding: utf-8
'''
Log writer, can be invoked by other modules
@author: Xiuwen Yin
@change: 2017-11-29 create script
'''
import logging
import os
import time
        
def set_logging(log_name=''):
    '''
    @summary: set logging format
    @param log_name: used to specify log name, optional 
    @param log level: DEBUG, INFO, WARNING, ERROR, CRITICAL , when invoke set_logging, should set log level
    '''
    log_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'log')
    log_format = logging.Formatter('%(asctime)s %(filename)s:%(funcName)s %(levelname)s [line:%(lineno)d] %(message)s')
    now = time.strftime('%Y-%m-%d %H:%M', time.localtime(time.time()))
    log_file = ''
    
    if not os.path.exists(log_folder):  # create log folder
        os.makedirs(log_folder)
        
    if '' != log_name:  # init log file name
        log_file = os.path.join(log_folder, now + '_' + log_name + '.log')
    else:
        log_file = os.path.join(log_folder, now + '_' + 'runing.log')
    
    logger = logging.getLogger("CI")  # create one logger object, use CI to specifly from root logging
    logger.setLevel(logging.ERROR)  # set log level switch  critical > error > warning > info > debug,notset
     
    file_handler = logging.FileHandler(log_file, mode='w')  # create a handler to write log file
    console_handler = logging.StreamHandler()  # create a handler to display log in console UI
    
    file_handler.setFormatter(log_format)  # set log format
    console_handler.setFormatter(log_format)
    
    logger.addHandler(file_handler)  # add logger into handler
    logger.addHandler(console_handler)
    
    return logger
    
if __name__ == '__main__':
    pass
    

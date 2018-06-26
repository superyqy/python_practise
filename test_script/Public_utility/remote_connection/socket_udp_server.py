#!/usr/bin/env python2.7
# encoding: utf-8
import os
import socket
import time


'''
Created on June 15, 2017
@author: YQY
@note: UDP SOCKET server
'''

def socketserver(host='0.0.0.0', port=2017):
    master_rf_url = 'http://127.0.0.1:8010/datacenter/trs?action=save'
    master_db_url = 'http://127.0.0.1:8010/datacenter/trs/count?action=save'
    master_length_url = 'http://127.0.0.1:8010/datacenter/trs/length?action=save'
    release_rf_url = 'http://127.0.0.1:8010/datacenter/reltrs?action=save'
    release_db_url = 'http://127.0.0.1:8010/datacenter/reltrs/count?action=save'
    release_length_url = 'http://127.0.0.1:8010/datacenter/reltrs/length?action=save'
    kill_browser = "ps -ef|grep firefox|grep -v grep|awk '{print $2}'|xargs -I {} kill -15 {}"
    server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server.settimeout(30)
    server.bind((host, port))
    while True:
        try:
            msg, addr = server.recvfrom(2048)
            if len(msg) > 0:
                print "Received message from client: ", msg
                if msg == 'downloadechartformaster':
                    os.system('firefox %s &' % master_rf_url)
                    time.sleep(20)
                    os.system(kill_browser)
                    os.system('firefox %s &' % master_db_url)
                    time.sleep(20)
                    os.system(kill_browser)
                    os.system('firefox %s &' % master_length_url)
                    time.sleep(20)
                    os.system(kill_browser)
                elif msg == 'downloadechartforrelease':
                    os.system('firefox %s &' % release_rf_url)
                    time.sleep(20)
                    os.system(kill_browser)
                    os.system('firefox %s &' % release_db_url)
                    time.sleep(20)
                    os.system(kill_browser)
                    os.system('firefox %s &' % release_length_url)
                    time.sleep(20)
                    os.system(kill_browser)
                server.sendto("execute download completed", addr)
        except:
            pass
    server.close()

if __name__ == '__main__':
    socketserver()

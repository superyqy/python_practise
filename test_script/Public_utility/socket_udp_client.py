#!/usr/bin/env python2.7
# encoding: utf-8
'''
Created on June 15, 2017

@author: YQY
@note: UDP SOCKET'S client
@version: 1.0
'''

import socket
import sys

def clientSend(host,port,messageForServer):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.connect((host,port))
    client.sendall(messageForServer)  #messageForServer can only be startTestForMaster  or startTestForRelease
    
    serverMsg = ''
    while True:
        try:
            buf = client.recv(1024)
            if len(buf) > 0:
                if buf =="execute completed":
                    serverMsg =  "execute completed"
                else:
                    serverMsg = "test failed"                  
                break           
        except:
            pass
    client.close()
    return serverMsg

if __name__ == '__main__':
    clientSend('127.0.0.1', 2017, sys.argv[1])
    print 'client exited!'
    
    

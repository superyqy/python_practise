#!/usr/bin/env python
# encoding: utf-8
'''
@summary: SSH connect and FTP transport
@author: YQY
@changed: 2018-03-01 create script
'''
import paramiko



class SSHConnector(object):
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.conn = self.create_connect()

    def create_connect(self):
        conn = None
        conn = paramiko.SSHClient()
        conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         conn.connect(hostname, port, username, password, pkey, key_filename, timeout, allow_agent, look_for_keys, compress, sock, gss_auth, gss_kex, gss_deleg_creds, gss_host, banner_timeout)
        conn.connect(self.hostname, self.port, self.username, self.password, timeout=30)
    
        return conn
    
    def ssh_operator(self, command):
        if self.conn:
            stdin, stdout, stderr = self.conn.exec_command(command, bufsize=1024, timeout=20)
#             print stdin.read()
#             print stdout.read()
            print stdout.readLine()
            print "############"
            print stderr.read()
    
if __name__ == "__main__":
   pass
    
    
    

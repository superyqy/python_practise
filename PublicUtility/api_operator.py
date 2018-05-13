#!/usr/bin/env python
# encoding: utf-8
'''
@summary: API operator
@author: YQY
@change: 2018-03-09 create script
'''
import requests

class APIOperator(object):
    def __init__(self, server_ip='127.0.0.1', port='8080'):
        self.server_ip = server_ip
        self.port = port
    
    def assemble_url(self, url_part, params={}):
        '''
        @summary: assemble api's url
        '''
        url = ''

        if '' not in [self.server_ip, self.port, url_part]:
            url = 'http://{0}:{1}{2}'.format(self.server_ip, self.port, url_part)
            if 0 < len(params):
                param_str = "?"
                for key in params.keys():
                    param_str += key + '=' + params[key] + '&'
                param_str = param_str.rstrip('&')
                url = url + param_str

        return url
    
    def get(self, url, payload={}, auth=()):
        '''
        @summary: create GET request
        @param params dictionary store input parameters
        @param auth: tuple store username and password 
        @return: response tuple, first element is status_code, second is response body 
        '''
        response = None
        
        if 0 < len(auth):   
            response = requests.get(url, auth=auth)
        elif 0 == len(auth):
            response = requests.get(url)
            
        status_code = response.status_code
        response_body = response.json()
        
        return status_code, response_body
    
    def post(self, url, payload):
        '''
        @summary: create POST request
        @param url: string request's url
        @param payload: dictionary request's paload data
        @return response: tuple, first element is status_code, second is response body 
        '''
        response = None

        if 0 < len(payload):
            response = requests.post(url, data=payload)
            
        return response

def operate_api(url_part, server_ip={}, port={}, params={}, request_type='get'):
    '''
    @summary: operate API and get response code and body
    '''
    status_code = ''
    response_body = ''
    
    api_operator = APIOperator(server_ip=server_ip)
    
    if 'get' == request_type.lower():
        url = api_operator.assemble_url(url_part, params=params)
        status_code, response_body = api_operator.get(url)
    elif 'post' == request_type.lower():
        pass
    
    return status_code, response_body
        
if __name__ == '__main__':
    params = {'id':'11886157901', 'type':'incr', 'category':'Full'}
    print operate_api('/debugdb/geo_in_db', '127.0.0.1', params=params)


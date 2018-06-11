#!/usr/bin/env python
# encoding: utf-8
'''
@summary: API automation test
@author: YQY
@change: 2018-02-24 create script
 TestCase：所有测试用例的基本类，给一个测试方法的名字，就会返回一个测试用例实例；
 TestSuit：组织测试用例的实例，支持测试用例的添加和删除，最终将传递给  testRunner进行测试执行；
 TextTestRunner：进行测试用例执行的实例，其中Text的意思是以文本形式显示测试结果。测试的结果会保存到TextTestResult实例中，包括运行了多少测试用例，成功了多少，失败了多少等信息；
 TestLoader：用来加载TestCase到TestSuite中的，其中有几个  loadTestsFrom__()方法，就是从各个地方寻找TestCase，创建它们的实例，然后add到TestSuite中，再返回一个TestSuite实例；
'''
import requests
import unittest
import hashlib


class EncryptString(object):
    def __init__(self):
        pass
    
    def encrypt(self, sign_str):
        '''
        @summary: encrypt string with md5 algorithm
        '''
        md5 = hashlib.md5()
        sign_bytes_utf8 = sign_str.encode(encoding="utf-8") 
        md5.update(sign_bytes_utf8)
        sign_md5 = md5.hexdigest()
        print(sign_md5)
        
        return sign_md5

class APIOperator(object):
    def __init__(self):
        pass
    
    def get(self, url, params={}, auth=()):
        '''
        @summary: create GET request
        @param params dictionary store input parameters
        @param auth: tuple store username and password 
        @return: response tuple, first element is status_code, second is response body 
        '''
        response = None
        
        if 0 < len(auth) and 0 < len(params):   
            response = requests.get(url, auth=auth, params=params)
        elif 0 == len(auth) and 0 < len(params):
            response = requests.get(url, params=params)
        elif 0 < len(auth) and 0 == len(params):
            response = requests.get(url, auth=auth)
        elif  0 == len(auth) and 0 == len(params):
            response = requests.get(url)
            
        return response
    
    def post(self, url, payload):
        '''
        @summary: create POST request
        @param url: string request's url
        @param payload: dictionary request's paload data
        @return response: tuple, first element is status_code, second is response body 
        '''
        response = None
        response = requests.post(url, data=payload)
    
        return response
    
class vehicleAPITest(unittest.TestCase):
    '''
    @summary: vehicle API testcases
    '''
    def setUp(self):
        '''
        @summary: rewrite unittest's setUp method
        '''
        self.url = 'http://10.74.13.76:8080/devices'
        self.api_operator = APIOperator()
       
    def test_get_devices_list(self):
        '''
        @summary: unittest will execute testcase which name starts with 'test'
        '''
        response = self.api_operator.get(self.url)

        self.result = response.json()
        self.assertEqual(response.status_code, 200) 
        self.assertIn('online', self.result['data'][0]['status'])
    
    def test_get_devices_list2(self):
        '''
        @summary: unittest will execute testcase which name starts with 'test'
        '''
        response = self.api_operator.get(self.url)

        self.result = response.json()
        self.assertNotIn('offline', self.result['data'][0]['status'])

    # def test():
    #     r = requests.get('https://api.github.com/user', auth=('username', 'password'))
    #     print r.status_code
    #     print r.headers['content-type']
    #     print r.json()
    #     print r.text
    #     assert r.status_code == 403

    def tearDown(self):
        '''
        @summary: rewrite tear down method
        '''
        print self.result


           
if __name__ == "__main__":
    pass
############one way to run testcase#################
#     unittest.main()  

###########another way to run testcase##############
#     test_unit = unittest.TestSuite()  
#     test_unit.addTest(vehicleAPITest("test_get_devices_list"))
#     test_unit.addTest(vehicleAPITest("test_get_devices_list2"))
#     runner = unittest.TextTestRunner()
#     runner.run(test_unit)
    
###########use discover to find testcases########### 
#     test_unit = unittest.TestSuite()  
#     test_dir = '/home/shawn/workspace/rdb_test_solution_test_tools/Statistic/DataCenter'
#     discover = unittest.defaultTestLoader.discover(test_dir, pattern='test*.py', top_level_dir=None)
#     for testcase in discover:
#         test_unit.addTest(testcase)
#     runner = unittest.TextTestRunner()
#     runner.run(test_unit)

#############way to test mutiple class##########
#     test_unit = unittest.TestSuite() 
#     suite_one = unittest.TestLoader().loadTestsFromTestCase(vehicleAPITest)
#     unittest.TextTestRunner(verbosity=1).run(suite_one)
    #     suite_two = unittest.TestLoader().loadTestsFromTestCase(vehicleAPITest2)
    #     suite = unittest.TestSuite([suite_one,suite_two])
    #     unittest.TextTestRunner(verbosity=2).run(suite)





工具名：douban API自动化测试框架
作者：殷秀文
创建时间：2018-06-23
主要功能：遍历目标文件夹，读取.xls后缀的excel文件，将除开template的其他sheet中的API测试用例读取URL,Method, request parameter, to be check response parameter, 调用API访问接口，验证
API返回是否正确，并将每个用例结果转换为Json格式并存储在TXT文本中（后续将使用testcase.xls作为模板来生成测试结果，给每个sheet用例的每个response参数作检查并返回成功还是失败，只要有一
个response parameter不是pass, Test Result字段就是Fail, 但由于周末时间匆忙，暂无时间来实现写excel的功能，所以目前只是展示思路）
应用场景：批量API用例检查

开发脚本：Python


前提：
1.excel表格格式使用.xls
2.按照template格式，组装测试用例，并放到脚本所在路径的testcase文件夹下
3.避免未知错误，请传入excel文件名及所在路径使用英文


脚本使用方法：  python run_testcase.py

脚本输出：
自动创建文件夹层级： 时间\testresult


Excel用例写法: 参照testcase/testcase_douban.xls中template sheet的描述


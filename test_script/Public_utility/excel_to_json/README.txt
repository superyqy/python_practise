工具名：API json格式参数表生成脚本
作者：殷秀文
创建时间：2018-06-22
主要功能：遍历目标文件夹，读取.xls后缀的excel文件，将除开template的其他sheet中的API测试用例数据转换为Json格式并存储在TXT文本中
应用场景：API需要post数据，但post数据中字段很多，通过调用脚本自动生成json体，解决了人工组装Json格式效率低、易出错的问题
开发脚本：Python


前提：
1.excel表格格式使用.xls
2.按照template格式，组装测试用例
3.通过命令行方式调用脚本
4.避免未知错误，请传入excel文件名及所在路径使用英文


脚本使用方法：
例1. 输入测试用例所在文件夹
python E:\excel_to_json\excel_to_json.py E:\excel_to_json\testcase
python E:\excel_to_json\excel_to_json.py E:\\excel_to_json\\testcase  ##调用脚本所在环境是windows系统时，在外部传入参数路径中，使用双斜线
例2. 输入测试用例所在文件路径
python E:\excel_to_json\excel_to_json.py E:\excel_to_json\testcase\api_testcase_template.xls

脚本输出：
1. 自动创建文件夹层级： 测试用例所在文件夹\时间\excel文件名\
2. 按照sheet名称，创建sheet.txt，每个TXT中包含当前sheet下所有的测试用例输出的json数据


Excel用例写法(需严格按照template中单元格标有颜色的格式录入测试用例参数名及用例层级结构)：
1. Test case Name: 测试用例名，必填，而且不能存在相同重复的用例名称
2. 1st_level: 第一层级，如果json体无层级之分，直接删除1st_level参数名的单元格，如存在，需在用例名所在行添加，而且用例中对应单元格需要填写第一级的值。 第一层级后可存在第二层级，也可不存在
3. 2rd_level: 第二层级，只有第一层级存在，才能增加第二层级，用例中第二层级对应单元格不需填写任何内容，
4. 跟在1st_level和2rd_level之后的是对应的参数名及参数值

生成结果示例：
测试用例1：无层级_1:{"overdueAmount": -10000.05, "cardType": "credit card", "cardid": 12332145698754656, "creditCardCount": 3, "bankName": "ZhaoShang Bank"}

测试用例2： 存在两个层级，第二个层级有多个:{"creditBankCardInfoList_one": [{"overdueAmount": -10000.05, "cardid": 111111145698754656, "bankName": "招商银行"}, {"overdueAmount": 5000, "cardid": 22222222416456165156, "bankName": "农业银行"}], "creditBaseInfo": [{"cardNo": "CD1234", "cardType": "ID Card", "creditCardCount": 3}]}

测试用例3： 两个层级和一个层级并存的用例:{"creditBankCardInfoList": [{"overdueAmount": -10000.05, "cardid": 12333333333333388, "bankName": "工商银行"}, {"overdueAmount": 5000, "cardid": 12314545416456165156, "bankName": "光大银行"}], "creditBaseInfo": {"cardNo": "CD1234", "cardType": "ID Card", "creditCardCount": 3}}

测试用例4：只存在一个层级，但有多个:{"creditBankCardInfoList": {"overdueAmount": -10000.05, "cardid": 12332145698754656, "bankName": "农业银行"}, "anotherBankcardinfolist": {"overdueAmount": 5000, "cardid": 12314545416456165156, "bankName": "光大银行"}, "creditBaseInfo": {"cardNo": "CD1234", "cardType": "ID Card", "creditCardCount": 3}}
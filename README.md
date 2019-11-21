# yqy_ci
 Yin’public repository, to store all practise scripts and other information, created at 20180512

test_case，存测试用例 
test_data，存测试数据，用于作为数据准备
test_script, 存测试脚本
output, 存测试结果，按date/module/testsuite 层级存放 1. 使用用例文件作为模板，输出为各个用例执行的结果 2. 存测试用例其他结果数据，如json+txt， sqlitedb,  3. 存生成测试结果的html文件 4. 存用例截图文件
backup： 存当前版本测试后的备份的文件，sqlitedb、MySQL库备份文件等
deploy: 存储安装包
tool: 存储需要安装的工具、插件，robotframework安装、selenium webdriver安装、浏览器驱动、python第三方库安装包等



Public functions:
1. api_accessor: 基于Python Requests库来访问API的公共类
2. auto_mail_sender: 基于Python smtp和email来自动发送邮件
3. database_accessor: 用于接入Mysql和Sqlite数据库
4. excel_handler: 基于Python xlrd和xlwt的读写xls格式Excel表格的公共类
5. excel_to_json: 用于将写在Excel表格中的API测试用例复杂的request自动组装为json字符串的格式
6. homework: 基于selenium webdriver的UI测试、基于excel+requests的API测试
7. remote_connect: paramiko以及socket UDP的远程连接
8. report_generator: 生成HTML格式报表
9. set_loggig: 封装了python logging模块，用于日志记录
10. xml_analyzer: 解析XML
其他测试脚本，包含禅道Bug报表生成，mock api, gps calculate......

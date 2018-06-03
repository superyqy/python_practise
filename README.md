# yqy_ci
 Yin’public repository, to store all practise scripts and other information, created at 20180512

test_case，存测试用例 
test_data，存测试数据，用于作为数据驱动
test_script, 存测试脚本
output, 存测试结果，按date/module/testsuite 层级存放 1. 使用用例文件作为模板，输出为各个用例执行的结果 2. 存测试用例其他结果数据，如json+txt， sqlitedb,  3. 存生成测试结果的html文件 4. 存用例截图文件
backup： 存当前版本测试后的备份的文件，sqlitedb、MySQL库备份文件等
deploy: 存储安装包
tool: 存储需要安装的工具、插件，robotframework安装、selenium webdriver安装、浏览器驱动、python第三方库安装包等



Public functions:
0. all knowledge summary for daily practise, can be open by "My base" software
1. auto mail sender: search specifiled folder for email html file each minute, and send to receiver by email name rules
2. excel handler: all common methods to read or write or clear excel xls file
3. api accessor: common ways to get/post api
4. bug recorder: a scripts to get different kinds of bug list from 禅道系统's API and create a html table to display it
5. html generator: a common way to create html tables
6. mysql reader: a common way to select/insert/update/delete in mysql server, and check existence of database and table
7. sqlite operator:a common way to create sqlite database, table and  select/insert/update/delete in mysql server, and check existence of database and table
8. set logging: packing by logging module, a common way to write log into file and display in console
9. unittest practise: all way to invoke testcase
10.gps length caculator: a way to calculate the distance between two gps points
11.all config: use python scripts to store public parameters and values
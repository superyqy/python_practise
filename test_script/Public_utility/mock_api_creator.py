#!/usr/bin/env python
#encoding: utf-8
'''
@summary: create mock api
@author: YQY
@changed: 2018-06-13 created
refered link: https://blog.csdn.net/u011054333/article/details/70151857/
延迟返回、生成随机数、数据库请求、加密
'''
import os
try:
	from flask import Flask, jsonify, request
except:
	os.system("pip install flask")
	from flask import Flask, jsonify, request

method_err = {
	"code": 301,
	"msg": "请求方式不正确，只支持post请求",
	"other":"test123"
}

# 成功的信息
success_msg = {
	"code": 200,
	"msg": "支付成功",
	"tester":"123123"
}

success_msg_query = {
	"code":200,
	"msg:":"query success",
	"tester":"123123",
	"成功":"成功123!"
}

# 数据库异常
db_err = {
	"code": 306,
	"msg": "数据库错误"
}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route("/")
def root():
	return "Hello Flask"

@app.route("/logger")
def test_log():     # app自带logging功能
	app.logger.debug("test logger")
	return 'test log'

@app.route("/user/<int:user_id>")   #URL中带参数值传递
def request_with_param(user_id):
	return str(user_id)  # 返回值不能是int，否则页面会报错


@app.route('/query', methods = ["GET"])
def query():
	if request.method == "GET":
		return jsonify(success_msg_query)


@app.route('/pay',methods=['POST','GET'])
def pay():        # 函数里面写的就是接口的业务逻辑了
	if request.method == 'POST':
		return jsonify(method_err)
	# return 就返回数据了，jsonify就是把python里面的数据类型（字典、list）转成json串
	elif request.method == 'GET':
		user_id = request.values.get('user_id')  # 使用request.values.get获取到传入的参数，user_id
		price = request.values.get('price')  # 使用request.values.get获取到传入的参数，price
		if user_id and price:
			if price.isdigit():  # 如果价格是整数的话
				return jsonify(success_msg)
			else:  # 如果不是整数也不是小数，返回价格错误
				return jsonify(param_err)
		else:  # 如果name或者价格获取不到的话，返回参数错误
			return jsonify(param_err)

if __name__ == '__main__':
    app.run(debug=True, host ="10.1.4.130", port=8888)  	# 运行程序，debug的意思是调试模式运行，可以看到请求，默认端口号是5000，可以使用port参数指定端口号
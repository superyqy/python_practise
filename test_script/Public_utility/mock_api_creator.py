#!/usr/bin/env python
#encoding: utf-8
from flask import Flask,jsonify,request

method_err = {
	"code": 301,
	"msg": "请求方式不正确，只支持post请求"
}
# 参数错误
param_err = {
	"code": 302,
	"msg": "请求参数错误，请检查入参"
}
# 余额不足
money_err = {
	"code": 303,
	"msg": "账户余额不足"
}

# 价格错误
price_err = {
	"code": 304,
	"msg": "价格不合法"
}

# 用户不存在
user_err = {
	"code": 305,
	"msg": "该用户不存在"
}

# 成功的信息
success_msg = {
	"code": 200,
	"msg": "支付成功"
}

# 数据库异常
db_err = {
	"code": 306,
	"msg": "数据库错误"
}

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

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

if __name__=='__main__':
    app.run(debug=True,port=8888)#运行程序，debug的意思是调试模式运行，可以看到请求，默认端口号是5000，可以使用port参数指定端口号
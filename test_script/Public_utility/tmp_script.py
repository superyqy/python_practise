#!/usr/bin/env python
#encoding:utf-8

import requests


if __name__ == "__main__":
	url = "http://127.0.0.1:8888/pay"
	parameter = {"user_id":"2","price":"10"}
	r=requests.post(url=url,params=parameter)
	print r.status_code
	print r.json()
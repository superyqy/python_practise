#!/usr/bin/env python
#encoding:utf-8

import requests


if __name__ == "__main__":
	movie_id = '1304102'
	url = "http://api.douban.com/v2/movie/subject/{0}".format(movie_id)
	r=requests.post(url=url)
	print r.status_code
	print r.json()



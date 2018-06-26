import xml.dom.minidom
import datetime
import time
import sys
import csv

reload(sys)
sys.setdefaultencoding('utf8')
from xml.dom.minidom import Document

suite_list = []
test_list = []
count1 = [0,]
count2 = [0,]
status = []
casetime = []
msg = []


def date2sce(date):
	d = datetime.datetime.strptime(date,"%Y%m%d %H:%M:%S.%f")
	ms = (float(d.microsecond) / 1000)
	return (time.mktime(d.timetuple()) * 1000) + ms


def readXML(file):
	global suite_list
	global test_list
	global count1
	global count2
	global status
	global casetime
	global msg

	dom = xml.dom.minidom.parse(file)
	root = dom.documentElement

	suite_list = root.getElementsByTagName("suite")
	test_list = root.getElementsByTagName("test")
	status_list = root.getElementsByTagName("status")

	status_list0 = []
	for i in range(0,len(status_list)):
		if status_list[i].getAttribute("critical") != '':
			status_list0.append(status_list[i])
			status.append(status_list[i].getAttribute("status"))
			casetime.append(
				date2sce(status_list[i].getAttribute("endtime")) - date2sce(status_list[i].getAttribute("starttime")))

	for i in range(0,len(status_list0)):
		if status_list0[i].firstChild is not None:
			msg.append(status_list0[i].firstChild.data)
		else:
			msg.append("right")

	for a in range(1,len(suite_list) - 1):
		x = 0
		y = 0
		for b in range(0,len(test_list)):
			if str(suite_list[a].getAttribute("id")) in str(test_list[b].getAttribute("id")):
				x += 1
				if status[b] == 'FAIL':
					y += 1
		count1.append(x)
		count2.append(y)


# for a in range(1,len(suite_list)-1):
#         print test_list[a].getAttribute("name")
#         print status[a]

def writeCSV(filename):
	csvfile = file(filename,'wb')
	writer = csv.writer(csvfile,dialect='excel',delimiter=',')
	writer.writerow(['Issue_Key','Test_Summary','Status'])
	data = []

	#     for i in range(1,len(suite_list)-1):
	#         for j in range(0,len(test_list)):
	#             if  str(suite_list[i].getAttribute("id")) in str(test_list[j].getAttribute("id")):
	#                 name = test_list[j].getAttribute("name").replace(' ', '_')
	#                 line = (name.split('_')[0],str(name),status[j])
	#                 data.append(line)

	for i in range(1,len(test_list)):
		name = test_list[i].getAttribute("name").replace(' ','_').replace(':',"_").replace(';',"_")
		line = (name.split('_')[0],str(name),status[i])
		data.append(line)
	writer.writerows(data)
	csvfile.close()


if '__main__' == __name__:
	read_file = sys.argv[1]
	readXML(read_file)
	write_file = sys.argv[2]
	writeCSV(write_file)
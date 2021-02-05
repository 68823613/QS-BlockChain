# -*- coding: utf-8 -*-
# @Author: ZYSama
# @Created Date: 2019-10-31 10:45:28
# @Last Modified time: 2019-11-04 10:25:07
# @Software: Sublime
import sys
sys.path.append('../ntrusign')
sys.path.append('../Server')
import poly
import json,os,time

# read the data of patient
def readjsonuser(i):
	path = 'D:/Workspace/java/test-master/data/database.json'
	with open(path,'r') as fr:
		datas = json.load(fr)
		print len(datas)
	for data in datas:
		print data["username"]
	print datas
	return datas

#read the data of doctor
def readjsondoctor():
	path = 'D:/Workspace/java/test-master/data/doctor-database.json'
	with open(path,'r') as fr:
		datas = json.load(fr)
	# print s
	return datas




if __name__ == '__main__':
	readjsondoctor()
	readjsonuser(0)
	count = 0

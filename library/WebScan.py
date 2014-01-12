#!/usr/bin/python2.7

import os
import sys
import zap
import time

foldername = sys.argv[1]
filein = open("../tmp/"+foldername+"/domains", "r")
urltest = filein.read()
urltest = urltest.split("\n")

scanner = zap.ZAP()
outfile = open("../tmp/"+foldername+"/WebVulns.txt", "w")

if len(urltest) != 1:
	print("DAMNIT")
else:
	for url in urltest:
		urlname = url.split(".")[0]
		
		if url.startswith("http://"):
			x = 1
		else:
			url = "http://"+url
		#open url and force proxy to be used
		scanner.urlopen(url+"/")
		scanner.start_spider(url)
		while scanner.spider_status != [u'100']:
			time.sleep(4)
		print("Done Spider")
		scanner.start_scan(url)
		while scanner.scan_status != [u'100']:
			time.sleep(4)
		print("Done Active Scan")
		issues = scanner.alerts
		oldalert = ""
		mycontent = []
		urllistDesc = []
		for item in issues:
			alert = item['alert']
			if oldalert != alert:
				description = item['description']
				parameter = item['param']
				reference = item['reference']
				reliability = item['reliability']
				solution = item['solution']
				mycontent.append({'alert':alert,'description':description, 'param':parameter, 'reference':reference, 'reliability':reliability, 'solution':solution})
				oldalert = alert
			else :
				description = item['description']
			url = item['url']	
			urllistDesc.append({'description':description, 'url':url})
outfile.write("<Content>\n")
for item in mycontent:
	outfile.write(str(item)+"\n")
outfile.write("</Content>\n<UrlList>\n")
for item in urllistDesc:
	outfile.write(str(item)+"\n")
outfile.write("</UrlList>")
outfile.close()
scanner.shutdown()

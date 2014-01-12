#/usr/bin/python3.2

import os
import sys

foldername = sys.argv[1]
filein = open("../tmp/"+foldername+"/nessOut.html", "r")
content1 = filein.readlines()
filein.close()
filein = open("../tmp/"+foldername+"/nmap.txt", "r")
nmapContent = filein.read()
nmapContent = str(nmapContent).replace("\n", "<br/>")
filein.close()
filein = open("../tmp/"+foldername+"/metagoofil.txt", "rb")
metaContent =[]
for line in filein:
	metaContent.append(str(line).replace("b'", "").replace("'","").replace("\\x00", "").replace("\\xff", "").replace("\\xfe", "").replace("\\n", "<br/>"))
#metagoofilContent = str(metagoofilContent).replace("\\n", "<br/>")
filein.close()
metagoofilContent = ""
for line in metaContent:
	metagoofilContent = metagoofilContent + str(line)
filein = open("../tmp/"+foldername+"/theHarvester.txt", "r")
theHarvesterContent = filein.read()
theHarvesterContent = str(theHarvesterContent).replace("\n", "<br/>")
filein.close()
fileout = open("../tmp/"+foldername+"/Output.html", "w")
content2 = []
for line in content1:
	#print(line)
	if line.startswith("<h1>ThisCompanyName"):
		content2.append(line.replace("ThisCompanyName", foldername))
	elif line.startswith("<p>HarvesterOutputList"):
		content2.append(line.replace("HarvesterOutputList", theHarvesterContent))
	elif line.startswith("<p>NmapOutput"):
		content2.append(line.replace("NmapOutput", nmapContent))
	elif line.startswith("<p>MetagoofilOutputList"):
		content2.append(line.replace("MetagoofilOutputList", metagoofilContent))
	else :
		content2.append(line.replace("\n", ""))
#print(content2)
for line in content2:
	fileout.write(line)
fileout.close



import string, sys, re, time
import http.client
'''
This is the first library I created but it works for what I needed
By:Kevin Haubris
If you find it use it as you wish but I probably won't maintain it.
'''

def test(test):
	print("HELLO"+test)

def cleanResponse(contentClean):
	thisList = []
	content2 = contentClean.split('<li class="g">')
	count = 0
	for item in content2:
		count +=1
		counter2 =0
		if count == 1:
			counter2 +=1
		else :
			link = item.split('<h3 class="r"><a href="/url?q=')
			link = link[1].split('&amp;sa=U&amp;')
			header = link[1].split('">')
			header = header[1].split('</a>')
			header = header[0]
			link = link[0]
			bcontent = item.split('<div class="s">')
			bcontent = bcontent[1].split('<br>')
			bcontent = bcontent[0]
			header = header.replace("<b>", "").replace("</b>", "")
			bcontent = bcontent.replace("<b>", "").replace("</b>", "")
			#print(header+"\n"+link+"\n"+bcontent+"\n===========================================================")
			#partsDict[header] = "<link>"+link+"</link><content>"+content+"</content>"
			thisListentry = "<header>"+header+"</header><link>"+link+"</link><content>"+bcontent+"</content>"
			thisList.append(thisListentry)
	return thisList

def Search(test,pages):
	#test = sys.argv[1]
	#test = sys.argv[1].replace(" ", "+")
	ListFinal = []
	partsDict = {}
	#test = "Kevin Haubris"
	#search multiple pages "&start=10" increase intervals of 10
	x = 0
	while x<pages:
		conn = http.client.HTTPConnection("www.google.com")
		conn.request("GET", "/search?q="+test+"&start="+str(x)+"0")
		response = conn.getresponse()
		content = ""
		for line in response:
			content = content + str(line)
		List = cleanResponse(content)
		x +=1
		ListFinal = ListFinal + List[:]
	return ListFinal


#!/usr/bin/python3.2
import msgpack, urllib, time 
import urllib.request

class Core: 
	def __init__(self, host='127.0.0.1', port=55552, user='msf', password='Password1!'):
		self.host = host
		self.port = port
		self.user = user
		self.password = password
		self.auth_token = self.mylogin()
		self.console_id = self.create_console()
		# Used to generate a template of an MSF RPC request
	def set_request(self):
		base_url = "http://" + self.host + ":" + str(self.port) + "/api/"
		base_request = urllib.request.Request(base_url)
		base_request.add_header('Content-type', 'binary/message-pack')
		return base_request
	def create_console(self):
		options = ['console.create']
		options.insert(1, self.auth_token)
		request = self.set_request()
		query_params = msgpack.packb(options)
		request.add_data(query_params)
		response = msgpack.unpackb(urllib.request.urlopen(request).read())
		#print(response)
		if response.get(b'id') is None:
			print("ERROR!!!!!") 
			exit() 
		print("#Console #"+str(response.get(b'id')).replace("b'", "").replace("'","")+" Created") 
		return response.get(b'id')
		
	def run(self, params=[], auth=True, console=True): 
		params.insert(1, self.auth_token)  
		if params[0] != 'session.list':
			params.insert(2, self.console_id)
		#print(params) 
		request = self.set_request() 
		query_params = msgpack.packb(params) 
		request.add_data(query_params) 
		response = msgpack.unpackb(urllib.request.urlopen(request).read()) 
		return response 

	def mylogin(self):
		options = ['auth.login', self.user, self.password] 
		token = None 
		request = self.set_request() 
		query_params = msgpack.packb(options) 
		request.add_data(query_params) 
		response = msgpack.unpackb(urllib.request.urlopen(request).read()) 
		#print(response)
		if response.get(b'result') == b'success':
			print("#Authed") 
			token = response.get(b'token') 
		else: 
			print("#GTFO!!!!!!")
			exit() 
		return token

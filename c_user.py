#!/usr/bin/env python3

"""c_user.py: User class source file"""

#import 		threading
import 		json
import 		time

import 		settings 			as 			C
from 		l_logging 			import 		log
#from 		l_files 			import 		load_json, save_json
from 		c_bytes_strings		import 		Message, Signature, Cipher, PublicKey, PrivateKey, Ip, UdpPort, TcpPort
#from 		c_node				import 		Node


"""

class GuestGroup():
	
	def __init__(self):
		self.guests = set()
		



class Peer():

	def __init__(self, publicKey, ip=None, udpPort=None):#, tcpPort=None):
		self.touch()
		assert isinstance(publicKey, PublicKey)
		self.publicKey = publicKey
		assert type(ip) == Ip
		self.ip = ip
		assert type(udpPort) == UdpPort
		self.udpPort = udpPort
		#assert type(tcpPort) == TcpPort
		#self.tcpPort = tcpPort

	def __str__(self):
		return "enode://{}@{}:{}".format(self.publicKey, self.ip, self.udpPort)

	def __repr__(self):
		return "<Peer: {}@{}:{}>".format(self.publicKey, self.ip, self.udpPort)


	def is_contactable(self):
		return type(self.ip) == Ip and type(self.udpPort)==UdpPort# and type(self.tcpPort)==TcpPort 

	def disconnect(self)
		self.touch()
		self.ip = None
		self.udpPort = None
		#self.tcpPort = None

	def update(self, *args):
		self.touch()
		allowedArgType = [Ip, UdpPort]
		for arg in args:
			allowedArgType.remove(type(arg))
			if   type(arg) == Ip:
				self.ip = arg
			elif type(arg) == UdpPort:
				self.udpPort = arg
			#elif type(arg) == TcpPort:
			#	self.tcpPort = arg

	def touch(self):
		self.timestamp = time.time()

	def time(self):
		return time.time() - self.timestamp






class User():

	def __init__(self, username):
		self.username = username.lower()
		self.userDirectory = C.MAIN_DIRECTORY + C.USERS_DIRECTORY + self.username + "/"
		self.config = load_json(self.userDirectory + C.USER_CONFIG_FILENAME)
		keyString = self.config.get("key","")
		if keyString == "":
			self.key = PrivateKey.generate()
			self.config["key"] = str(self.key)
			save_json(self.config, self.userDirectory + C.USER_CONFIG_FILENAME)
		else:
			self.key = PrivateKey(keyString)

		self.node = Node([],self.key.public_key())

	def __del__(self):
		save_json(self.config, self.userDirectory + C.USER_CONFIG_FILENAME)


	def __repr__(self):
		return "<User: (name: {0}, pubkey: {1}...)>".format(self.username, self.key.public_key().get_only_key()[:8])



"""
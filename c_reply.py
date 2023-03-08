

import 		constants 			as 			C
from 		l_logging 			import 		log
#from 		l_files 			import 		load_json, save_json
from 		c_bytes_strings		import 		Message, Signature, Cipher, PublicKey, PrivateKey, Ip, Port, Timestamp
from 		l_crypto 			import 		CryptoTool





class Reply:
	pass




class Identity(Reply):
	def __init__(self, publicKey, ip, port, builtTimestamp, signature):
		assert type(publicKey) == PublicKey
		self.publicKey = publicKey
		assert type(ip) == Ip
		self.ip = ip
		assert type(port) == Port
		self.port = port
		assert type(builtTimestamp) == Timestamp
		self.builtTimestamp = builtTimestamp
		self.timestamp = Timestamp()		
		assert type(signature) == Signature
		self.signature = signature

		if self.is_not_valid():
			log.warn("Identity is not valid")


	def __eq__(self, other):
		if   type(other)==tuple and len(other)==2 and type(other[0])==str and type(other[1])==int:
			return self.ip==other[0] and self.port==other[1]
		elif type(other)==Identity:
			return self.publicKey==other.publicKey
		else:
			log.imp_error()


	def touch(self):
		self.timestamp = Timestamp()

	def update(self, *args):
		self.touch()
		allowedArgType = [Ip, Port]
		for arg in args:
			try:
				allowedArgType.remove(type(arg))
				if   type(arg) == Ip:
					self.ip = arg
				elif type(arg) == Port:
					self.port = arg
			except:
				log.error("unable to update Identity with {}".format(type(arg).__name__))


	def is_valid(self):
		return self.signature.verify(Message(self.publicKey + self.ip + self.port + self.builtTimestamp), self.publicKey)

	def is_not_valid(self):
		return not self.is_valid()


	def generate(privateKey, ip, port):
		publicKey = privateKey.public_key()
		builtTimestamp = Timestamp()
		tempMessage = Message(publicKey + ip + port + builtTimestamp)
		signature = tempMessage.sign(privateKey)

		return Identity(publicKey, ip, port, builtTimestamp, signature)

	def __str__(self):
		print("Identity")




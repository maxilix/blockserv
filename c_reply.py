

import 		settings 			as 			C
from 		l_logging 			import 		log
#from 		l_files 			import 		load_json, save_json
from 		c_bytes_strings		import 		Message, Signature, Cipher, PublicKey, PrivateKey, Ip, Port, Timestamp
from 		t_crypto 			import 		CryptoTool
from 		t_main				import 		now





class Reply:
	pass




class Identity(Reply):
	def __init__(self, publicKey, ip, port, timestamp, signature):
		# in Reply/Identity, ip and udpPort are tramsmit via socket
		assert type(publicKey) == PublicKey
		self.publicKey = publicKey
		assert type(ip) == Ip
		self.ip = ip
		assert type(port) == Port
		self.port = port
		assert type(timestamp) == Timestamp
		self.timestamp = timestamp
		assert type(signature) == Signature
		self.signature = signature

		if self.is_not_valid():
			log.warn("Identity is not valid")


	def is_valid(self):
		return self.signature.verify(Message(self.publicKey + self.ip + self.port + self.timestamp), self.publicKey)


	def is_not_valid(self):
		return not self.is_valid()


	def generate(privateKey, ip, port):
		publicKey = privateKey.public_key()
		timestamp = Timestamp()
		tempMessage = Message(publicKey + ip + port + timestamp)
		signature = tempMessage.sign(privateKey)

		return Identity(publicKey, ip, port, timestamp, signature)

	def __str__(self):
		print("Identity")


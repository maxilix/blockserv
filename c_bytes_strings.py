#!/usr/bin/env python3

"""c_bytes_string.py: define specialized bytes-like objects"""


import 		time
from 		math				import 		ceil


import 		settings 			as 			C
from 		l_logging 			import 		log
from 		t_crypto 			import 		CryptoTool




class SimpleBytesString():

	def __init__(self, data):
		if   type(data) == bytes:
			self.data = data
		elif type(data) == str:
			self.data = data.encode(STRING_ENCODER)
		elif type(data) == int:
			self.data = data.to_bytes(ceil(data.bit_length() / 8), byteorder=BYTEORDER)
		else:
			log.error("invalid type: '{}' can't be convert in 'bytes'".format(type(data).__name__), ex=TypeError)

	def __repr__(self):
		return "<{0}: ({1})>".format(self.__class__.__name__, str(self))

	def __str__(self):
		return "0x" + self.data.hex()

	def __int__(self):
		return int.from_bytes(self.data, byteorder=BYTEORDER)

	def __len__(self):
		return len(self.data)

	def __getitem__(self, key):
		return self.data[key]

	def __eq__(self, other):
		other = self.__class__(other)
		return self.data == other.data

	def __add__(self, other):
		if not isinstance(other, SimpleBytesString):
			other = SimpleBytesString(other)
		return self.data + other.data

	def __radd__(self, other):
		return self + other

	def __iadd__(self, other):
		return self + other



class CryptoBytesString(SimpleBytesString):
	pass



class Key(CryptoBytesString):
	pass


class PrivateKey(Key):

	def generate():
		return PrivateKey(CryptoTool.generate_private_key())

	def public_key(self):
		return PublicKey(CryptoTool.derive_public_key(self.data))

	def check(self, publicKey):
		if type(publicKey) != PublicKey:
			log.error("invalid type: PrivateKey.check() expect a PublicKey", ex=TypeError)
		return CryptoTool.check_keys(self.data, publicKey.data)




class PublicKey(Key):

	def check(self, privateKey):
		if type(privateKey) != PrivateKey:
			log.error("invalid type: PublicKey.check() expect a PrivateKey", ex=TypeError)
		return CryptoTool.check_keys(privateKey.data, self.data)











class Timestamp(SimpleBytesString):

	def __init__(self, data=None):
		if data is None:
			data = time.time()
		if   type(data) == Timestamp:
			self.data = data.data
		elif type(data) == int or type(data) == float:
			super().__init__(round(1000*data))
		else:
			log.error("invalid Timestamp type: '{0}' instead of 'int' or 'float'".format(type(data).__name__), ex=TypeError)

	def __str__(self):
		milliseconde = int(self)
		return "{}.{}s".format(milliseconde//1000, milliseconde%1000)




class Ip(SimpleBytesString):

	def __init__(self, data):
		if   type(data) == Ip:
			self.data = data.data
		elif type(data) == bytes:
			if   len(data) == 4:
				super().__init__(data)
			else:
				log.error("invalid length for Ip: {0} instead of 4 bytes expected".format(len(data)), ex=Exception)
		elif type(data) == str:
			data = [int(e) for e in data.split(".")]
			if len(data) == 4 and data[0]>=0 and data[0]<=255 and data[1]>=0 and data[1]<=255 and data[2]>=0 and data[2]<=255 and data[3]>=0 and data[3]<=255:
				super().__init__(bytes(data))
			else:
				log.error("invalid Ip string: '255.255.255.255' format expected ", ex=Exception)
		else:
			log.error("invalid Ip type: '{0}' instead of 'bytes' or 'str'".format(type(data).__name__), ex=TypeError)

	def __str__(self):
		return ".".join([str(byte) for byte in self.data])



class Port(SimpleBytesString):

	def __init__(self, data):
		if   type(data) == Port:
			self.data = data.data
		elif type(data) == bytes:
			if   len(data) == 2:
				super().__init__(data)
			else:
				log.error("invalid length for Port: {0} instead of 2 bytes expected".format(len(data)), ex=Exception)
		elif type(data) == int:
			if data > 0 and data < 65536:
				super().__init__(data)
			else:
				log.error("invalid Port number: {0} cannot be a port".format(data), ex=Exception)
		else:
			log.error("invalid Port type: '{0}' instead of 'bytes' or 'int'".format(type(data).__name__), ex=TypeError)

	def __str__(self):
		return str(int(self))


"""
class UdpPort(Port):
	pass

class TcpPort(Port):
	pass
"""



class Message(CryptoBytesString):

	def __str__(self):
		return self.data.decode(STRING_ENCODER)

	def sign(self, key):
		if   type(key) == PrivateKey:
			return Signature(CryptoTool.sign(m=self.data, k=key.data))
		elif type(key) == PublicKey:
			log.error("can't sign with public key", ex=Exception)
		else:
			log.error("invalid type: '{}' instead of 'PrivateKey'".format(type(key).__name__), ex=TypeError)

	def encrypt(self, key):
		#return Cipher()
		pass

	def hash(self):
		return CryptoTool.hash(self.data)




class Signature(CryptoBytesString):

	def verify(self, message, key):
		if   type(key) == PrivateKey:
			return CryptoTool.prverify(m=message.data, s=self.data, k=key.data)
		elif type(key) == PublicKey:
			return CryptoTool.verify(m=message.data, s=self.data, k=key.data)
		else:
			log.error("invalid type: '{}' instead of 'Key'".format(type(key).__name__), ex=TypeError)




class Cipher(CryptoBytesString):
	
	def decrypt(self, key):
		#return Message()
		pass











"""
30 740201010420 1d46fa348b42d4222643d35312ddc711871c2db180a76ca69021a1d45df3c6c1 a007 06052b8104000a a144 03420004 ef50935775ca6720ed136131f43176b5d0ca9c6fcec13849cf762f36d5c941725d2578044e06f2313552d73f34baa333f52ea185661ae43e46bc0ccb468f2f18
                1d46fa348b42d4222643d35312ddc711871c2db180a76ca69021a1d45df3c6c1

30 740201010420 78ba5d4b1fecd5bc0dd8f2a3fa96e6fc1f8366960ad058dcc76fea27e81adc9a a007 06052b8104000a a144 03420004 a6a47f44e786fe93c5384a41d7e2c6f3d14d30c02565158c4e9f87fab113bf98cff9f227e16e715b4034d0f2ca8ae9b58691991b94523f33abd9067bc1c52244
30 56301006072a8648ce3d0201                                                           06052b8104000a      03420004 a6a47f44e786fe93c5384a41d7e2c6f3d14d30c02565158c4e9f87fab113bf98cff9f227e16e715b4034d0f2ca8ae9b58691991b94523f33abd9067bc1c52244
30 740201010420 69b6cb187afbb92b77a143973cd2928e6c6c5e8765d32b0e8faeeb99896be7e0 a007 06052b8104000a a144 03420004 4415385a963a4933368cdd38691af1a294195aae5f68879b8e8b347ea42b6a2b77cc536cda525509ace5169f543db398f555d94df5c8b68c67d5f7c6039e3e14
30 56301006072a8648ce3d0201                                                           06052b8104000a      03420004 4415385a963a4933368cdd38691af1a294195aae5f68879b8e8b347ea42b6a2b77cc536cda525509ace5169f543db398f555d94df5c8b68c67d5f7c6039e3e14


30 740201010420 5d4b2b48646193560c89c3e76fd58277fe49e40248493fcbde5d563292f153e0 a007 06052b8104000aa144 03420004 c34908c081193742c07236dfb28f9cf43137cfafc8737f54885da3e5bc1e46e1280672006d766fe050bd9d63d5758b3b759ac011a1b9eeeea24a9261aea460a4
                5d4b2b48646193560c89c3e76fd58277fe49e40248493fcbde5d563292f153e0                                  c34908c081193742c07236dfb28f9cf43137cfafc8737f54885da3e5bc1e46e1280672006d766fe050bd9d63d5758b3b759ac011a1b9eeeea24a9261aea460a4


"""

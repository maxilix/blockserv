#!/usr/bin/env python3

"""l_crypto.py: define CryptoTool for cryptography managment
Uses only bytes object that can be integrated in bytes-like object
These methods use openssl subprocess and temp files to sign, cypher and verify"""




import 		subprocess

from 		l_logging 			import 		log
from 		l_files 			import 		temp_file_name


ecdsaCurveName 							= "secp256k1"
privateKeyLength 						= 118
privateKeyOnlyLength 					= 32
privateKeyOnlyStartIndex 				= 7
publicKeyLength 						= 88
publicKeyOnlyLength 					= 64
publicKeyOnlyStartIndex 				= 24
publicKeyOnlyStartIndexInPrivateKey 	= 54
ecdsaHashName 							= "sha256"
standardHashName 						= "sha256"


class CryptoTool():

	def __new__(cls):
			log.error("CryptoTool must not be instanced", who="CryptoTool")

	def generate_private_key():
		cmd = ["openssl", "ecparam", "-name", ecdsaCurveName, "-genkey", "-outform", "DER", "-noout"]
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		(result, error) = process.communicate()
		if error != b'':
			log.error(error.decode().replace("\n"," \\n "), who="CryptoTool")
		log.info("New private key generated", who="CryptoTool")
		return result
		


	def derive_public_key(privateKey):
		cmd = ["openssl", "ec", "-inform", "DER", "-outform", "DER", "-pubout"]
		process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		process.stdin.write(privateKey)
		(result, error) = process.communicate()
		if error != b'read EC key\nwriting EC key\n':
			log.error(error.decode().replace("\n"," \\n "), who="CryptoTool")
		log.info("Public key derivated", who="CryptoTool")
		return result



	def check_keys(privateKey, publicKey):
		return privateKey[publicKeyOnlyStartIndexInPrivateKey:publicKeyOnlyStartIndexInPrivateKey+publicKeyOnlyLength] == publicKey[publicKeyOnlyStartIndex:publicKeyOnlyStartIndex+publicKeyOnlyLength]



	def sign(*, m, k):

		# create key temp file
		keyFileName = temp_file_name()
		keyFile = open(keyFileName, 'wb')
		keyFile.write(k)
		keyFile.close()

		# sign message
		cmd = ["openssl", "dgst", "-"+ecdsaHashName, "-sign", keyFileName, "-keyform", "DER"]
		process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		process.stdin.write(m)
		(result, error) = process.communicate()
		if error != b'':
			log.error(error.decode().replace("\n"," \\n "), who="CryptoTool")

		# remove temp files
		subprocess.run(["rm", keyFileName])

		return result



	def verify(*, m, s, k):

		# create signature temp file
		signatureFileName = temp_file_name()
		signatureFile = open(signatureFileName, 'wb')
		signatureFile.write(s)
		signatureFile.close()

		# create key temp file
		keyFileName = temp_file_name()
		keyFile = open(keyFileName, 'wb')
		keyFile.write(k)
		keyFile.close()

		# verify signature
		cmd = ["openssl", "dgst", "-"+ecdsaHashName, "-verify", keyFileName, "-keyform", "DER", "-signature", signatureFileName]
		process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		process.stdin.write(m)
		(result, error) = process.communicate()
		#if error != b'':
		#	log.error(error.decode().replace("\n"," \\n "), who="CryptoTool")

		# remove temp files
		subprocess.run(["rm", signatureFileName, keyFileName])

		return "Verified OK" in result.decode()



	def prverify(*, m, s, k):
		log.error("prverify is not yet implemented", who="CryptoTool")



	def key_to_hex(key):
		if type(key) != bytes:
			raise TypeError("invalid type: '{}' instead 'bytes'".format(type(key).__name__))
		if   len(key) == privateKeyLength:
			return key[privateKeyOnlyStartIndex:privateKeyOnlyStartIndex+privateKeyOnlyLength].hex()
		elif len(key) == publicKeyLength:
			return key[publicKeyOnlyStartIndex:publicKeyOnlyStartIndex+publicKeyOnlyLength].hex()
		else:
			raise Exception("argument does not seem to be a key: wrong length")


	def hash(datas):
		cmd = ["openssl", "dgst", "-"+standardHashName]
		process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		process.stdin.write(datas)
		(result, error) = process.communicate()
		if error != b'':
			log.error(error.decode().replace("\n"," \\n "), who="CryptoTool")
		hexString = result.decode().split("= ")[1]    # select the string after the "= "
		hexString[:-1]                                # remove \n at the end
		return bytes.fromhex(hexString)


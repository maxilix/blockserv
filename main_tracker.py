#!/usr/bin/env python3

"""main_tracker.py: tracker script to provide minimal tracker behavior"""


import 		socket
import 		pickle


import		constants			as			C
from		l_logging			import		log
from 		c_bytes_strings		import 		Message, Signature, Cipher, PublicKey, PrivateKey, Ip, Port
from 		c_request 			import 		*
from 		c_reply 			import 		*





def receive_identity(addressFrom, identity):
	print(C.INDENT + "identity received")
	if identity.is_valid():
		if identity == addressFrom:
			print(C.INDENT + C.INFO + "valid identity of sender")
			if identity in peerList:
				index = peerList.index(identity)
				peerList[index].update(Ip(addressFrom[0]), Port(addressFrom[1]))
				print(C.INDENT + C.INFO + "peer already known, updated")
			else:
				peerList.append(identity)
				print(C.INDENT + C.INFO + "new peer added")

		else:
			print(C.INDENT + C.WARN + "valid identity but not from sender")
	else:
		print(C.INDENT + C.WARN + "invalid identity")



def request_peers(addressFrom, peerRequest):
	print(C.INDENT + "peerRequest received")
	try:
		index = peerList.index(addressFrom)
	except:
		print(C.INDENT + C.WARN + "request from unknown sender")
		return
	print(C.INDENT + C.INFO + "request known peer")
	number = peerRequest.number
	print(C.INDENT + C.INFO + "send {} identities".format(number))
	# SEND













peerList = []


# Create a datagram socket
UdpTrackerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UdpTrackerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
UdpTrackerSocket.bind(("", C.DEFAULT_TRACKER_PORT))

print("UDP Tracker up and listening")

while(True):
	rawData, address = UdpTrackerSocket.recvfrom(C.TRANSMISSION_LENGTH)
	print("data from {}".format(address))
	try:
		data = pickle.loads(rawData)
	except:
		print(C.INDENT + C.ERROR + "unable to deserialization")
		continue

	if   isinstance(data, Reply):
		match type(data):
			case Identity:
				receive_identity(address, data)

	elif isinstance(data, Request): 
		match type(data):
			case Peers:
				request_peers(address, data)










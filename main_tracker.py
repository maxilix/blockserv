#!/usr/bin/env python3

"""main_tracker.py: tracker script to provide minimal tracker behavior"""


import 		socket
import 		pickle


import		constants			as			C
from		l_logging			import		log
from 		c_bytes_strings		import 		Message, Signature, Cipher, PublicKey, PrivateKey, Ip, Port
from 		c_request 			import 		*
from 		c_reply 			import 		*


def sort_peer_list():
	pass



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

	match type(data):
		case Identity:
			if data.is_valid():
				print(C.INDENT + "identity received")
				if data.ip == address[0] and data.port == address[1]:
					print(C.INDENT + C.INFO + "valid identity of sender")
				else:
					print(C.INDENT + C.WARN + "valid identity but not from sender")







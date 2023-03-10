#!/usr/bin/env python3

"""main.py: main script"""

import 		sys
import 		socket
import 		threading
import 		pickle
import 		time

import 		constants 			as 			C
import 		tools
from 		l_logging 			import 		log
from 		c_bytes_strings		import 		Message, Signature, Cipher, PublicKey, PrivateKey, Ip, Port, Timestamp
from 		c_request 			import 		*
from 		c_reply 			import 		*





"""

class A():
	def __init__(self, dataA):
		self.dataA = dataA

	def upgrade_to_B(self, dataB):
		if 	self.__class__ == A:
			self.__class__ = B
			self.__init__(self.dataA, dataB)
		else:
			print("nothing to do")


class B(A):
	def __init__(self, dataA, dataB):
		super().__init__(dataA)
		self.dataB = dataB
"""

myIp     = C.LOCALHOST
myPort   = tools.next_free_port()
sk = PrivateKey.generate()
identity = Identity.generate(sk, Ip(myIp), Port(myPort))

peerRequest = Peers(10)

#time.sleep(0.5)
#identity.timestamp = Timestamp()




# Create a datagram socket
UdpMySocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
UdpMySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind to address and ip
UdpMySocket.bind((myIp, myPort))


tracker = (C.LOCALHOST, C.DEFAULT_TRACKER_PORT)

#UdpMySocket.sendto(pickle.dumps(identity), tracker)
#input()

UdpMySocket.sendto(pickle.dumps(peerRequest), tracker)
input()

UdpMySocket.sendto(pickle.dumps(identity), tracker)
input()

UdpMySocket.sendto(pickle.dumps(peerRequest), tracker)
input()

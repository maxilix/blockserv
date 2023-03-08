import 		socket


import		constants			as			C




def next_free_port():
	port = C.DEFAULT_PEER_PORT
	while True:
		try:
			s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			s.bind(('', port))
			s.close()
			break
		except:
			port += 1
			continue
	return port
class Request():
	pass



class Peers(Request):
	def __init__(self,number=1):
		assert type(number)==int
		self.number = number




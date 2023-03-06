#!/usr/bin/env python3

"""l_logging.py: Simple log library to write formatted log in file

	from l_logging import logger as log
	log.print(formatedString)			# to log without flag
	log.info(formatedString)			# to log with info flag
	log.warn(formatedString)			# to log with warning flag
	log.error(formatedString)			# to log with error flag and raise an error"""


#####    Define some constants    ########################################################################
##########################################################################################################
DEFAULT_FILENAME			= ".log"					# default filename
DEFAULT_MODE 				= 'w' 						# 'w' to erase previous log file, 'a' to always append log file
DEFAULT_VERBOSITY			= 3 						# default verbosity
														#	
														#	
WRITE_FLAG 					= True						# write flag in prompt
FLAG_ERROR					= 0 						# only Error
FLAG_WARN					= 1 						# Warn and Error
FLAG_INFO					= 2 						# Warn, Error and Info
FLAG_NOFLAG					= 3 						# Warn, Error, Info and NoFlag
FLAG_ERROR_RAISE			= True 						# Error log raise an error
DEFAULT_EXCEPTION 			= Exception 				#
														#
														#
WRITE_TIMESTAMP				= False						# write timestamp in prompt
TIMESTAMP_FORMAT			= "%H:%M:%S"				# timestamp format :
														#     %Y : year
														#     %m : month
														#     %d : day
														#     %H : hour (00-23)
														#     %I : hour (00-11)
														#     %M : minute
														#     %S : second
														#
														#
WRITE_WHO					= True						# write mandatory or thread name in prompt
WHO_LENGTH 					= 11 						# max length for 'who' argument string
MAIN_THREAD_WHO_NAME 		= "interpretor"				# string for who field if main thread emit logs without 'who' argument
##########################################################################################################



from 		threading 	import 	current_thread, main_thread
from 		datetime 	import 	datetime


class Logger():

	def __init__(self, logFileName=DEFAULT_FILENAME, mode=DEFAULT_MODE, verbosity=DEFAULT_VERBOSITY):
		self.logFile = open(logFileName, mode)
		self.verbosity = verbosity
		self.__write(FLAG_NOFLAG, "log file opened")

	def __del__(self):
		self.__write(FLAG_NOFLAG, "log file closed")
		self.logFile.close()

	def error(self, message, who=None, ex=DEFAULT_EXCEPTION):
		if (self.verbosity >= FLAG_ERROR):
			self.__write(FLAG_ERROR, message, who=who)
		if (FLAG_ERROR_RAISE):
			raise ex(message)
		return

	def warn(self, message, who=None):
		if (self.verbosity >= FLAG_WARN):
			self.__write(FLAG_WARN, message, who=who)
		return

	def info(self, message, who=None):
		if (self.verbosity >= FLAG_INFO):
			self.__write(FLAG_INFO, message, who=who)
		return

	def print(self, message, who=None):
		if (self.verbosity >= FLAG_NOFLAG):
			self.__write(FLAG_NOFLAG, message, who=who)
		return

	def subprocess_result(self, result, subprocessName):
		self.print(result.decode().replace("\n", " \\n "), who=subprocessName)

	def subprocess_error(self, error, subprocessName):
		self.error(error.decode().replace("\n", " \\n "), who=subprocessName)


	def __write(self, flag, message, who=None):

		# flag
		if WRITE_FLAG:
			if   (flag == FLAG_ERROR):
				self.logFile.write("\033[31m[ERROR] \033[0m")
			elif (flag == FLAG_WARN):
				self.logFile.write("\033[33m [WARN] \033[0m")
			elif (flag == FLAG_INFO):
				self.logFile.write("\033[32m [INFO] \033[0m")
			elif (flag == FLAG_NOFLAG):
				self.logFile.write("        ")
			else:
				raise Exception("loglib: flag no supported")

		# timestamp
		if WRITE_TIMESTAMP:
			self.logFile.write(datetime.now().strftime(TIMESTAMP_FORMAT))
			self.logFile.write(" ")

		# who
		if WRITE_WHO:
			if who is None:
				if current_thread() == main_thread():
					who = MAIN_THREAD_WHO_NAME
				else:
					who = current_thread().name
		if len(who)>WHO_LENGTH:
			who = who[:WHO_LENGTH-3] + "..."
		else:
			who += "".join([" "]*(WHO_LENGTH-len(who)))
		self.logFile.write(who)
		self.logFile.write(": ")

		# message
		self.logFile.write(message + "\n")

		# flush
		self.logFile.flush()

		return




log = Logger()

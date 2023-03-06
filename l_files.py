#!/usr/bin/env python3

"""tools_files.py: tools for files managment"""



import 		os
import 		json
import 		random

from 		l_logging 			import 		log






def temp_file_name(prefix=".", suffix=".temp", alphabet="0123456789abcdef", length=8):
	tempFileName = "./"
	while os.path.exists(tempFileName):
		tempFileName = prefix + "".join([random.choice(alphabet) for _ in range(length)]) + suffix
	tempFile = open(tempFileName,"w")
	tempFile.close()
	return tempFileName







def __save_file(datas, filename, force=True):
	if os.path.exists(filename):
		if not (force or input("overwrite {0} file ? ".format(filename)).lower() == 'y'):
			log.warn("{0} already exists, save aborted".format(filename))
			return False
	if   type(datas) == str:
		mode = 'w'
	elif type(datas) == bytes:
		mode = 'wb'
	else:
		TypeError("unsuported save type: '{0}' instead 'str' or 'bytes'".format(type(datas).__name__))
	file = open(filename, mode)
	file.write(datas)
	file.close()
	log.info("{0} save completed".format(filename))
	return True

def save_bytes(datas, filename, force=True):
	return __save_file(datas, filename, force)

def save_string(datas, filename, force=True):
	return __save_file(datas, filename, force)

def save_json(dictionnary, jsonFilename, force=True):
	return __save_file(json.dumps(dictionnary, indent=4), jsonFilename, force)





def __load_file(filename):
	file = open(filename, 'rb')
	rop = file.read()
	file.close()
	return rop

def load_bytes(filename):
	return __load_file(filename)

def load_string(filename):
	return __load_file(filename).decode("utf-8")

def load_json(jsonFilename):
	return json.loads(__load_file(jsonFilename).decode("utf-8"))


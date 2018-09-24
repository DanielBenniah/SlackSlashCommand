import datetime

def log_error (message):
	error_log = open ("errors.log", "a+")
	error_log.write("{0}: {1}\n".format(str(datetime.datetime.now()), message))

def log_message (message):
	log = open ("logs.log", "a+")
	log.write ("{0}: {1}\n".format(str(datetime.datetime.now()), message))
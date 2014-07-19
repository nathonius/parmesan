import time
import os.path
import sys

class ParmLogger:
	"""Parmesan logger. Log files are created based on the date."""

	def __init__(self, verbose):
		"""Figure out the filepath for the log file and if we are writing or appending"""
		log_basepath = os.path.dirname(__file__)
		log_basepath = os.path.join(log_basepath, 'logs')
		timestamp = time.strftime('%y-%m-%d')
		log_filename = 'log-'+timestamp+'.txt'
		self.log_filepath = os.path.join(log_basepath, log_filename)
		self.verbose = verbose

	def timestamp(self):
		"""Return the time in the format [yy-mm-dd hh:mm:ss]"""
		form = '[%y-%m-%d %H:%M:%S]'
		timestamp = time.strftime(form)
		return timestamp

	def log(self, message):
		"""Log a message"""
		#format the message
		timestamp = self.timestamp()
		message = timestamp+' '+message.strip()
		#if we are verbose, output the message
		if(self.verbose):
			print(message)
		message = message + '\n'
		#decide the file mode
		if(os.path.isfile(self.log_filepath)):
			mode = 'a'
		else:
			mode = 'w'
		#log and close
		with open(self.log_filepath, mode) as log_file:
			log_file.write(message)

	def log_error(self):
		"""Log the three pieces of an exception"""
		error = sys.exc_info()
		for i in error:
			self.log(i)

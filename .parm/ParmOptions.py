import ParmLogger
import os.path
import json

class ParmOptions:
	"""Class wrapper for reading user.parm-settings and default.parm-settings, as well as verbosity"""
	def __init__(self, verbose):
		"""Read options files"""''
		logger = ParmLogger.ParmLogger()
		#Set up the paths for the two options files
		options_path = os.path.dirname(__file__)
		user_options_path = os.path.join(options_path, 'user.parm-settings')
		default_options_path = os.path.join(options_path, 'default.parm-settings')
		#Read options files
		logger.log("Reading default.parm-settings.")
		default = json.load(default_options_path)
		logger.log("Reading user.parm-settings.")
		user = json.load(user_options_path)
		#Store as class variable
		self.options = default
		self.options["verbose"] = verbose
		for setting in user.keys():
			self.options[setting] = user[setting]

	def __getattr__(self, name):
		"""Make it easier to access options"""
		if(name in self.options.keys()):
			return self.options[name]
		else:
			raise AttributeError('Class ParmOptions has no attribute named '+name)
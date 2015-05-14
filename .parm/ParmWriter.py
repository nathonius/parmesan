from ParmOptions import ParmOptions
from ParmLogger import ParmLogger
import os.path

class ParmWriter:
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

	def write(self, content):
		for path in content.keys():
			with open(path, 'w') as fp:
				fp.write(content[path])
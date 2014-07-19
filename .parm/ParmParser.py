import os.path
import ParmLogger

class ParmParser:
	"""Parses the all content listed in the manifest, executes the correct commands on the content"""
	def __init__(self, verbose):
		"""Set up the root path, the manifest path, and the logger"""
		self.manifest_path = os.path.abspath(__file__)
		self.manifest_path = os.path.dirname(self.parm_root)
		self.manifest_path = os.path.join(self.manifest_path, 'manifest.parm-settings')
		self.logger = ParmLogger.ParmLogger(verbose)
		self.options = self.read_options()

	def read_options(self):
		

	def content_removed(self, path):
		"""Removes the generated files associated with removed content"""


	def parse_manifest(self):
		"""Read the manifest, call the appropriate functions"""
		self.logger.log("Reading manifest.")
		with open(self.manifest_path, 'r') as manifest:
			for line in manifest:
				processed_line = line.split('|')
				path = processed_line[0]
				#Set the action to removed, added, or changed
				if('REMOVED' in processed_line[1]):
					action = 'REMOVED'
				elif(len(processed_line) == 2):
					continue
				else:
					action = processed_line[2].strip()
				#Do the thing we need to do
				if(action == 'REMOVED'):
					try:
						self.content_removed(path)
					except:
						self.logger.log_error()
						return False
				elif(action == 'ADDED'):
					try:
						self.content_added(path)
					except:
						self.logger.log_error()
						return False
				else:
					try:
						self.content_modified(path)
					except:
						self.logger.log_error()
						return False

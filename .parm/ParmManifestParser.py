import os.path
import os
from ParmLogger import ParmLogger
from ParmOptions import ParmOptions

class ParmManifestParser:
	"""Parses the all content listed in the manifest, executes the correct commands on the content"""
	def __init__(self, verbose):
		"""Set up the root path, the manifest path, and the logger"""
		self.manifest_path = os.path.dirname(__file__)
		self.default_options_path = os.path.join(self.manifest_path, 'default.parm-settings')
		self.user_options_path = os.path.join(self.manifest_path, 'user.parm-settings')
		self.manifest_path = os.path.join(self.manifest_path, 'manifest.parm-settings')
		self.logger = ParmLogger(verbose)
		self.options = ParmOptions(verbose)

	def parse_manifest(self):
		"""Read the manifest, call the appropriate functions"""
		self.logger.log("Parsing new manifest.")
		content_files = []
		with open(self.manifest_path, 'r') as manifest:
			for line in manifest:
				path = line.split("|")[0]
				#Find the changed files
				if line.endswith("|CHANGED") or line.endswith("|ADDED"):
					content_files.append(path)
		self.logger.log("Done.")
		return content_files
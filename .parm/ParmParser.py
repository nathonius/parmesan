import os.path
import os
from ParmLogger import ParmLogger
from ParmOptions import ParmOptions
from ParmContentGenerator import ParmContentGenerator

class ParmParser:
	"""Parses the all content listed in the manifest, executes the correct commands on the content"""
	def __init__(self, verbose):
		"""Set up the root path, the manifest path, and the logger"""
		self.manifest_path = os.path.dirname(__file__)
		self.default_options_path = os.path.join(self.manifest_path, 'default.parm-settings')
		self.user_options_path = os.path.join(self.manifest_path, 'user.parm-settings')
		self.manifest_path = os.path.join(self.manifest_path, 'manifest.parm-settings')
		self.logger = ParmLogger(verbose)
		self.options = ParmOptions(verbose)
		self.generator = ParmContentGenerator(verbose)

	def content_removed(self, path):
		"""Removes the generated files associated with removed content"""
		if not self.options.autoremove_generated_files:
			return
		possible_types = [".html", ".htm", ".php"]
		if self.options.generate_txt_version:
			possible_types.append(".txt")
		filedir = os.path.dirname(path)
		filename = os.path.basename(path)
		type_pos = filename.rfind(".")
		filename = filename[:type_pos]
		for ftype in possible_types:
			name = filename+ftype
			fpath = os.path.join(filedir, name)
			if os.path.isfile(fpath):
				os.remove(fpath)

	def touch_file(self, path):
		"""Reads and re-writes the file to update its 'date modified' value"""
		if not os.path.isfile(path):
			return False
		file_str = ""
		with open(path, 'r') as f:
			file_str = f.read()
		with open(path, 'w') as f:
			f.write(file_str)
		return True

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
				else:
					try:
						self.generator.update_content(path)
					except:
						self.touch_file(path)
						self.logger.log_error()
						return False
		self.logger.log("\tDone.")
		return True
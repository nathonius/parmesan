from os import walk
import os.path
import ParmLogger

class ParmAnalyzer:
	"""Walks through the directory tree, finding all the files to process"""
	def __init__(self):
		"""Set up the base path, ignore list, and logger"""
		self.parm_root = os.path.abspath(__file__)
		self.parm_root = os.path.dirname(self.parm_root)
		self.parm_root = os.path.dirname(self.parm_root)
		self.logger = ParmLogger.ParmLogger()
		self.ignore = ('.py', '.pyc', '.parm-settings', '.html', '.htm', '.php', '.css', '.js')
		self.manifest_path = os.path.join(self.parm_root, '.parm')
		self.manifest_path = os.path.join(self.manifest_path, 'manifest.parm-settings')
		self.existing_manifest = []

	def is_content(self, path):
		"""Returns true if given file path is a content file"""
		filename = str(os.path.basename(path)).lower()
		if(not os.path.isfile(path)):
			return False
		elif(str(filename).endswith(self.ignore)):
			return False
		else:
			return True

	def find_modified_content(self, tracked_content):
		"""Returns 2 dicts of content files that have been added or changed (not deleted)"""
		self.logger.log("Finding new and changed content files.")
		added_content = {}
		modified_content = {}
		for root, dirs, files in walk(self.parm_root):
			#IGNORE HIDDEN FILES/FOLDERS
			files = [f for f in files if not f[0] == '.']
			dirs[:] = [d for d in dirs if not d[0] == '.']
			for f in files:
				path = os.path.join(root, f)
				last_modified = float(os.path.getmtime(path))
				#If we already know about the file, and it has been modified
				if(path in tracked_content.keys()):
					if(last_modified != tracked_content[path]):
						modified_content[path] = last_modified
				#If it's a new file
				else:
					#Is it actually content?
					if(self.is_content(path)):
						added_content[path] = last_modified
		return (added_content, modified_content)

	def find_removed_content(self, tracked_content):
		"""Returns list of content files that have been removed"""
		self.logger.log("Finding deleted content files.")
		removed_content = []
		for path in tracked_content.keys():
			if(not os.path.isfile(path)):
				removed_content.append(path)
		return removed_content

	def read_manifest(self):
		"""Returns dict of files tracked in manifest with their last modified dates"""
		self.logger.log("Reading manifest.")
		tracked_content = {}
		with open(self.manifest_path, 'r') as manifest:
			for line in manifest:
				processed_line = line.split("|")
				if(processed_line[1].strip() != 'REMOVED'):
					tracked_content[processed_line[0]] = float(processed_line[1].strip())
					self.existing_manifest.append(line)
		return tracked_content

	def update_manifest(self):
		"""Updates the manifest, adding new files, sets timestamp on changed files, sets deleted files timestamps to removed"""
		try:
			tracked_content = self.read_manifest()
			(added_content, modified_content) = self.find_removed_content(tracked_content)
			removed_content = self.find_removed_content(tracked_content)
		except:
			self.logger.log_error()
		self.logger.log("Updating manifest.")
		new_manifest = ""
		added_files = added_content.keys()
		modified_files = modified_content.keys()
		for line in self.existing_manifest:
			path = line.split('|')[0]
			#Check to see if we are removing a file
			if(path in removed_content):
				new_manifest = new_manifest + path + '|REMOVED\n'
			#Check to see if we are modifying a file
			elif(path in modified_files):
				new_manifest = new_manifest + path + '|' + modified_content[path] + '\n'
			#Check to see if we are adding a file
			elif(path in added_files):
				new_manifest = new_manifest + path + '|' + added_content[path] + '\n'
			#Otherwise, this file hasn't changed
			else:
				new_manifest = new_manifest + line
		#Write the new manifest
		with open(self.manifest_path, 'w') as manifest:
			manifest.write(new_manifest)
		self.logger.log("Wrote new manifest.")
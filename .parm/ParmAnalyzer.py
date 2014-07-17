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
		self.ignore = ['py', 'parm-settings', 'html', 'htm', 'php']
	"""def go(self):
		for root, dirs, files in walk(self.parm_root):
			#IGNORE HIDDEN FILES
			files = [f for f in files if not f[0] == '.']
			dirs[:] = [d for d in dirs if (not d[0] == '.' or d == '.parm')]
			print('Root:',root)
			print('Dirs:',dirs)
			print('Files:',files)
			print('\n')"""

	def read_manifest(self):
		"""Returns list of files tracked in manifest with their last modified dates"""
		manifest_path = os.path.join(self.parm_root, '.parm')
		manifest_path = os.path.join(manifest_path, 'manifest.parm-settings')
		tracked_content = []
		with open(manifest_path, 'r') as manifest:
			for line in manifest:
				processed_line = line.split("|")
				content = {"path":processed_line[0], "timestamp":processed_line[1]}
				tracked_content.append(content)
		return tracked_content
				

	def update_manifest(self):
		"""Figure out what's new and what's changed, reflect those changes in the manifest"""
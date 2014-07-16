from os import walk
import os.path

class ParmAnalyzer:
	"""Walks through the directory tree, finding all the files to process"""
	def __init__(self):
		"""Set up the base path"""
		self.parm_root = os.path.abspath(__file__)
		self.parm_root = os.path.dirname(self.parm_root)
		self.parm_root = os.path.dirname(self.parm_root)
		print(str(self.parm_root))
	def go(self):
		for root, dirs, files in walk(self.parm_root):
			#IGNORE HIDDEN FILES
			files = [f for f in files if not f[0] == '.']
			dirs[:] = [d for d in dirs if not d[0] == '.']
			print('Root:',root)
			print('Dirs:',dirs)
			print('Files:',files)
			print('\n')

a = ParmAnalyzer()
a.go()
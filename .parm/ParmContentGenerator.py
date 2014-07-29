from ParmOptions import ParmOptions
from ParmLogger import ParmLogger

class ParmContentGenerator:
	""""""
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

def update_content(path):
	"""Add or re-process modified content"""
	
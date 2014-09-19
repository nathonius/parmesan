from ParmLogger import ParmLogger
from ParmOptions import ParmOptions
import os.path

class ParmWebBuilder:
	"""Given the generated html, places the html into the appropriate template in the right place"""
	def __init__(self, template, content, verbose):
		
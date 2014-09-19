from ParmOptions import ParmOptions
from ParmLogger import ParmLogger
import re
import os.path

class ParmTemplateParser:
	"""Returns the generated html content spliced into the correct template"""
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

	def parse(self, template_path, html):
		"""given a template path and some generated html, splices the html in"""
		template_filename = os.path.basename(template_path)
		self.logger.log("\tParsing template "+template_filename)
		content = ""
		with open(template_path, 'r') as template:
			for line in template:
				if not re.search(r'{!content-here!}'):
					content += line
				else:
					content += html
		return content
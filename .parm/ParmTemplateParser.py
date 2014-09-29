from ParmOptions import ParmOptions
from ParmLogger import ParmLogger

class ParmTemplateParser:
	"""Returns the generated html content spliced into the correct template"""
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

	def find_template(self, html):
		for line in html:
			if "<!--{!template:" in line and "!}-->" in line:
				template_line = line.split(':')[1]
				template_line = template_line[:template_line.find("!}")]
				template_line = template_line.strip()
				return template_line
		return False

	def parse(self, html):
		"""given some generated html, finds the correct template and splices the two"""
		template = self.find_template(html)
		if not template:
			return False
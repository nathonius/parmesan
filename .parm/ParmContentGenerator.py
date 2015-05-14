from ParmOptions import ParmOptions
from ParmLogger import ParmLogger
import os
import os.path
import subprocess

class ParmContentGenerator:
	"""Process content and templates to generate the website"""
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

	def markdown(self, path, output_filename):
		"""Given an input and output path, run markdown on it"""		
		self.logger.log("\t\tGenerating "+output_filename)
		html_content = subprocess.check_output(["multimarkdown", path]).decode('utf-8')
		return html_content

	def generate(self, paths):
		"""Given a list of paths to input files, run markdown on each and return a dictionary of html content"""
		self.logger.log("\tGenerating web content.")
		content = {}
		for path in paths:
			input_filename = os.path.basename(path)
			output_filename = input_filename[:input_filename.rfind(".")]+".html"
			output_path = os.path.dirname(path)
			output_path = os.path.join(output_path, output_filename)
			content[output_path] = self.markdown(path, output_filename)
		return content

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

	def generate(self, paths):
		"""Given list of file paths, runs markdown on each"""
		self.logger.log("\tGenerating web content.")
		generated_html = {}
		for path in paths:
			input_filename = os.path.basename(path)
			output_filename = input_filename[:input_filename.rfind(".")]+".html"
			output_path = os.path.dirname(path)
			output_path = os.path.join(output_path, output_filename)
			self.logger.log("\t\tGenerating "+output_filename)
			html_content = subprocess.check_output(["multimarkdown", path]).decode('utf-8')
			generated_html[path] = html_content
		return generated_html
from ParmOptions import ParmOptions
from ParmLogger import ParmLogger
from ParmContentRipper import ParmContentRipper
import os
import os.path
import subprocess
import re

class ParmContentGenerator:
	"""Process content and templates to generate the website"""
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

	def get_content_info(self, content):
		"""Parses the content file for the parm settings blocks"""
		self.logger.log("\t\tSearching for parm settings blocks.")
		previous_line = ""
		parm_data = {}
		found_parm_data = False
		for line in content:
			if re.search(r'{!.*: .*!}', line) and not "<!--parmesan-ignore-->" in previous_line:
				data = line.replace('{!', '')
				data = data.replace('!}', '')
				data = data.strip()
				data = data.split(':')
				option = data[0].strip()
				value = data[1].strip()
				parm_data[option] = value
				found_parm_data = True
			else:
				previous_line = line
		if not found_parm_data:
			self.logger.log("\t\tCould not find parm settings block inside content file!")
			return False
		else:
			return parm_data

	def find_template(self, parm_data):
		self.logger.log("\t\tSearching for template.")
		template_path = os.path.dirname(__file__)
		template_path = os.path.join(template_path, 'templates')
		if not 'template' in parm_data.keys() and self.options.default_template == None:
			self.logger.log("\t\tNo template or default template specified!")
			return False
		else:
			if not 'template' in parm_data.keys():
				parm_data["template"] = self.options.default_template
		template_path = os.path.join(template_path, parm_data['template'])
		if not os.path.isfile(template_path):
			self.logger.log("\t\tTemplate file "+template_path+" does not exist!")
			return False
		else:
			return template_path

	def get_template(self, template):
		self.logger.log("\t\tReading template.")
		"""Given a template file pointer, returns it in pieces before and after content block(s)"""
		before = ""
		after = ""
		found_content_tag = False
		for line in template:
			if '{!content-here!}' in line:
				found_content_tag = True
			elif found_content_tag == False:
				before = before + line + "\n"
			else:
				after = after + line + "\n"
		return (before, after)

	def get_txt_version(self, content_path, before_content, after_content):
		"""Return the content as a txt file"""
		self.logger.log("\t\tWriting txt version.")
		txt_path = os.path.dirname(content_path)
		filename = os.path.basename(content_path)
		txt_file = ""
		if(self.options.include_html_in_txt):
			txt_file = before_content
		with open(content_path, 'r') as content:
			for line in content:
				txt_file = txt_file + line + "\n"
		if(self.options.include_html_in_txt):
			txt_file = txt_file + after_content
		txt_path = os.path.dirname(path)
		type_pos = filename.rfind(".")
		txt_path = os.path.join(txt_path, filename[:type_pos] + ".txt")
		with open(txt_path, 'w') as txt:
			txt.write(txt_file)

	def generate_web(self, parm_data):
		"""Given dictionary of each section of content, runs markdown on each"""
		self.logger.log("\t\tRunning parser.")
		parser = self.options.parser
		parsed_ouput = {}
		#use subprocess.check_output
		for piece in parm_data.keys():
			if piece == 'template':
				pass
			else:
				syntax = [parser, parm_data[piece]]
				html_content = subprocess.check_output(syntax).decode('utf-8')
				parsed_ouput[piece] = html_content
		return parsed_ouput

	def update_content(self, path):
		"""Add or re-process modified content"""
		filename = os.path.basename(path)
		self.logger.log("\tGenerating content from " + str(filename) + "...")
		ripper = ParmContentRipper(self.options.verbose)
		parm_data = ripper.rip(path)
		template = ""
		if self.options.default_template:
			template = self.options.default_template
		if 'template' in parm_data.keys():
			template = parm_data['template']
		parsed_data = generate_web(parm_data)
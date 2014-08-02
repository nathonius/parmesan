from ParmOptions import ParmOptions
from ParmLogger import ParmLogger
import os.path
import subprocess
import os

class ParmContentGenerator:
	"""Process content and templates to generate the website"""
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

	def get_content_info(self, content):
		"""Parses the content file for the parm settings block"""
		previous_line = ""
		parm_data = {}
		found_parm_data = False
		for line in content:
			if found_parm_data and line.startswith("}}"):
				break
			elif found_parm_data:
				data = line.split(':')
				data[0] = data[0].replace('"', '')
				data[1] = data[1].replace('"', '')
				option = data[0].strip()
				value = data[1].strip()
				parm_data[option] = value
			elif line.startswith("{{") and not "<!--parmesan-ignore-->" in previous_line:
				found_parm_data = True
			else:
				pass
		if(found_parm_data == False):
			self.logger.log("\t\tCould not find parm settings block inside content file!")
			return False
		else:
			return parm_data

	def get_template(self, template):
		"""Finds the correct template. Returns it in pieces before and after content block(s)"""
		before = ""
		after = ""
		found_content_tag = False
		for line in template:
			if '{{content-here}}' in line:
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

	def generate_web(self, content_path, before_content, after_content, template_type):
		"""Run the markdown parser"""
		self.logger.log("\tRunning parser.")
		parser = self.options.parser
		parse_syntax = self.options.parse_syntax.split()
		content_filename = os.path.basename(content_path)
		content_filename = content_filename[:content_filename.rfind('.')]
		output_path = os.path.dirname(content_path)
		output_path = os.path.join(output_path, content_filename + template_type)
		for i in range(len(parse_syntax)):
			if parse_syntax[i] == '$file':
				parse_syntax[i] = content_path
			elif parse_syntax[i] == '$out':
				parse_syntax[i] = output_path
		parse_syntax = [parser] + parse_syntax
		parse_syntax = [parser, content_path]
		self.logger.log("Parse syntax:")
		self.logger.log(str(parse_syntax))
		try:
			html_content = subprocess.check_output(parse_syntax)
		except:
			self.logger.log_error()
			raise
		full_content = before_content + html_content + after_content
		with open(output_path, 'w') as output_file:
			output_file.write(str(full_content))
		return True

	def update_content(self, path):
		"""Add or re-process modified content"""
		template_path = os.path.dirname(__file__)
		template_path = os.path.join(template_path, 'templates')
		filename = os.path.basename(path)
		self.logger.log("\tGenerating content from " + str(filename) + "...")
		parm_data = {}
		#Retrieve parm options block
		with open(path, 'r') as content:
			parm_data = self.get_content_info(content)
			if not parm_data:
				return False
		#Figure out if we have a template
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
		#We have a template
		else:
			template_filename = os.path.basename(template_path)
			type_pos = template_filename.rfind(".")
			template_type = template_filename[type_pos:]
			before_content = ""
			after_content = ""
			with open(template_path, 'r') as template:
				(before_content, after_content) = self.get_template(template)
			if self.options.generate_text_version:
				self.get_txt_version(path, before_content, after_content)
			self.generate_web(path, before_content, after_content, template_type)
			self.logger.log("\t\tDone.")
			return True
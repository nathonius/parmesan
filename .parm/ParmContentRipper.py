from ParmOptions import ParmOptions
from ParmLogger import ParmLogger
import os.path
import re

class ParmContentRipper:
	"""Finds all pieces of content in the given file, returns a dictionary of content sections and options"""
	def __init__(self, verbose):
		self.options = ParmOptions(verbose)
		self.logger = ParmLogger(verbose)

	def rip(self, path):
		"""Rip out the content and options"""
		self.logger.log("\tRipping content and parm options.")
		if not os.path.isfile(path):
			filename = str(os.path.basename(path))
			self.logger.log("\t\tContent file "+filename+" could not be found.")
			return False
		ripped_content = {"all":""}
		previous_line = ""
		last_content_id = "all"
		with open(path, 'r') as content:
			for line in content:
				#Is the line a settings block?
				if re.search(r'{!.*: .*!}', line) and not "<!--parmesan-ignore-->" in previous_line:
					option = line.split(':')[1].strip()
					option = option.replace('!}', '')
					option = option.strip()
					if re.search(r'{!template: .*!}', line):
						ripped_content['template'] = option
					elif re.search(r'{!content-id: .*!}', line):
						ripped_content[option] = ""
						last_content_id = option
					else:
						self.logger.log('\t\tUnrecognized parm data "'+line.strip()+'". Ignoring.')
				elif "<!--parmesan-ignore-->" in line:
					pass
				else:
					ripped_content[last_content_id] += line
				previous_line = line
		return ripped_content
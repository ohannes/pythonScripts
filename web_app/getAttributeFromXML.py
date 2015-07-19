import sys
sys.path.append(os.environ["ohannes"])
from ohannes import *

empty_string = ""

class keyObject:
	def __init__(self, key_str, key_seperator, key_EOL, end_of_attribute, input_file_name, output_file_name):
		self.key_str = key_str
		self.key_seperator = key_seperator
		self.key_EOL = key_EOL
		self.end_of_attribute = end_of_attribute
		self.input_file_name = input_file_name
		self.output_file_name = output_file_name

key_objects = 	[
					keyObject('class="', ".", "{}", '"', "wiki_home.xml", "wiki.css"),
					keyObject('id="', "#", "{}", '"', "wiki_home.xml", "wiki.css")
				]

for key_object in key_objects:
	try:
		ftr = open(key_object.input_file_name, read_mode)
	except:
		sys.exit("ERROR: could not open input file " + key_object.input_file_name)
	content = ftr.read()
	ftr.close()

	key_names = []
	while True:
		try:
			index = content.index(key_object.key_str)
		except:
			break
		key_name = empty_string
		while content[index+len(key_object.key_str)] != key_object.end_of_attribute:
			key_name += content[index+len(key_object.key_str)]
			index += 1
		if not key_name in key_names:
			key_names.append(key_name)
		try:
			content = content[(index+len(key_object.key_str)):]
		except:
			break
	try:
		ftw = open(key_object.output_file_name, append_mode)
	except:
		sys.exit("ERROR: could not open output file " + key_object.output_file_name)

	for key_name in key_names:
		ftw.write(key_object.key_seperator + key_name + key_object.key_EOL + EOL)
	ftw.close()

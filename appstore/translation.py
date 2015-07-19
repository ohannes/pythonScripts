import os

language_yml_path = "/home/arcelik/projects/appstore2.0/server/config/locales"

EOL = "\n"
CR = "\r"
TAB = "\t"
SPACE = " "
skip_characters = [SPACE, TAB, CR, EOL]
file_extension_splitter = "."
yml_extension = "yml"
extension = "translation"
language_code_length = 2
reference_language_code = "en"
reference_language_code2 = "tr"
comment_start_indicator = "#"
label_splitter = ":"
read_mode = "r"
write_mode = "w"
END = "END"

def isNotEmpty(line):
	for char in line:
		if not char in skip_characters:
			return True
	return False

def commentStartIndex(line):
	try:
		index = line.index(comment_start_indicator)
		return index
	except:
		return len(line)

def extractComment(line):
	return line[0:commentStartIndex(line)]

def getLabel(line):
	label = ""
	for char in line:
		if char == label_splitter:
			break
		if not char in skip_characters:
			label += char
	return label

def extractLabel(line):
	return line[line.index(label_splitter)+1:len(line)]

def hasValue(line):
	return isNotEmpty(extractLabel(line))

def getDepth(line):
	depth = 0
	for char in line:
		if char != SPACE:
			break
		depth += 1
	return depth/2

def isRealValue(value):
	previous_char = "a"
	for char in value:
		if (char.islower() or char.isupper()) and (previous_char.islower() or previous_char.isupper()):
			return True
		previous_char = char
	return False

def getValue(line):
	value = extractLabel(line)
	start_index = 0
	end_index = len(value) - 1
	while value[start_index] in skip_characters:
		start_index += 1
	while value[end_index] in skip_characters:
		end_index -= 1
	return value[start_index:end_index+1]

def searchFile(file_name):
	ftr = open(file_name, read_mode)

	previous_depth = -1
	previous_label = ""
	ftw = open(file_name + file_extension_splitter + extension, write_mode)
	while True:
		line = ftr.readline()
		if not line:
			break
		if isNotEmpty(line):
			line = extractComment(line)
			if isNotEmpty(line):
				depth = getDepth(line)
				label = getLabel(line)
				if hasValue(line):
					value = getValue(line)
					if isRealValue(value):
						#print depth, label, value
						ftw.write(str(depth) + TAB + label + TAB + value + EOL)
	
	ftr.close()
	ftw.close()

os.chdir(language_yml_path)

yml_files = os.listdir(os.getcwd())
language_codes = []

for yml_file in yml_files:
	language_code = yml_file.split(file_extension_splitter)[0]
	if len(language_code) == language_code_length:
		language_codes.append(language_code)

for language_code in language_codes:
	searchFile(language_code + file_extension_splitter + yml_extension)

import os, sys, time, datetime

line_counter = 0
file_counter = 0
folder_counter = 0

KEYS    = ["\t:", " :", " ,", ", ", "," , " \n", "( ", " )", "    ", "  ", " \t", "\t ", "  "]
VALUES  = [":"  , ":" , "," , "," , ", ", "\n" , "(" , ")" , "\t"  , " " , " "  , " "  , " " ]
REPEATS = [-1   , -1  , -1  , -1  , 1   , -1   , -1  , -1  , -1    , -1  , -1   , -1   , -1  ]

EQUALS_SYMBOLS       = ["="    , "!"        , "+"   , "-"    , "*"       , "/"]
EQUALS_SYMBOLS_NAMES = ["EQUAL", "NOT", "PLUS", "MINUS", "MULTIPLY", "DIVIDE"]

def getEqualSymbols(base_symbol, symbol, name):
	EQUALS         = ["\t" + symbol + base_symbol, " " + symbol + base_symbol, symbol + base_symbol + "\t", symbol + base_symbol + " ", symbol + base_symbol              ]
	EQUALS_VALUES  = [symbol + base_symbol       , symbol + base_symbol      , symbol + base_symbol       , symbol + base_symbol      , "_SYMBOL_EQUAL_WITH_" + name + "_"]
	EQUALS_REPEATS = [-1                         , -1                        , -1                         , -1                        , 1                                 ]
	return EQUALS, EQUALS_VALUES, EQUALS_REPEATS

def getRealEqualSymbols(base_symbol, symbol, name):
	EQUALS         = ["_SYMBOL_EQUAL_WITH_" + name + "_"]
	EQUALS_VALUES  = [" " + symbol + base_symbol + " "  ]
	EQUALS_REPEATS = [1                                 ]
	return EQUALS, EQUALS_VALUES, EQUALS_REPEATS

def getPath():
	if len(sys.argv) < 2:
		sys.exit("Usage: python beautifier.py <dir_path>")

	path = sys.argv[1]
	if path[0] != "/":
		path = os.getcwd() + "/" + path

	if not os.path.exists(path):
		sys.exit(path + " does not exist")
	if not os.path.isdir(path):
		sys.exit(path + " is not a directory")

	return path

def beautify(file_list):
	global line_counter
	global file_counter
	global folder_counter

	for file_name in file_list:
		if os.path.isfile(file_name):
			file_name_split = file_name.split(".")
			if len(file_name_split) < 2:
				continue
			file_ext = file_name_split[1]
			if not file_ext == "py":
				continue

			print "revising file:", file_name

			timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
			temp_file_name = timestamp + "_" + file_name

			temp_file = open(temp_file_name, "w")
			source_file = open(file_name)

			while True:
				line = source_file.readline()
				if not line:
					break

				line_counter += 1

				line_has_char = False
				for char in line:
					if char != " " and char != "\t" and char != "\n":
						line_has_char = True
						break

				if not line_has_char:
					line = "\n"

				next_line = "\n"
				if line == next_line:
					while next_line == "\n":
						next_line = source_file.readline()
						if not next_line:
							next_line = "\n"
							break
						line_counter += 1

					temp_file.write(line)
					line = next_line

				for i in range(len(KEYS)):
					key = KEYS[i]
					value = VALUES[i]
					repeat = REPEATS[i]
					if repeat > 0:
						line = line.replace(key, value)
					elif repeat < 0:
						while key in line:
							line = line.replace(key, value)
					else:
						pass

				for j in range(len(EQUALS_SYMBOLS)):
					symbol = EQUALS_SYMBOLS[j]
					name = EQUALS_SYMBOLS_NAMES[j]
					keys, values, repeats = getEqualSymbols("=", symbol, name)
					for i in range(len(keys)):
						key = keys[i]
						value = values[i]
						repeat = repeats[i]
						if repeat > 0:
							line = line.replace(key, value)
						elif repeat < 0:
							while key in line:
								line = line.replace(key, value)
						else:
							pass

				symbol = "="
				name = "BASE_EQ"
				keys, values, repeats = getEqualSymbols("", symbol, name)
				for i in range(len(keys)):
					key = keys[i]
					value = values[i]
					repeat = repeats[i]
					if repeat > 0:
						line = line.replace(key, value)
					elif repeat < 0:
						while key in line:
							line = line.replace(key, value)
					else:
						pass

				keys, values, repeats = getRealEqualSymbols("", symbol, name)
				for i in range(len(keys)):
					key = keys[i]
					value = values[i]
					repeat = repeats[i]
					if repeat > 0:
						line = line.replace(key, value)
					elif repeat < 0:
						while key in line:
							line = line.replace(key, value)
					else:
						pass

				for j in range(len(EQUALS_SYMBOLS)):
					symbol = EQUALS_SYMBOLS[j]
					name = EQUALS_SYMBOLS_NAMES[j]
					keys, values, repeats = getRealEqualSymbols("=", symbol, name)
					for i in range(len(keys)):
						key = keys[i]
						value = values[i]
						repeat = repeats[i]
						if repeat > 0:
							line = line.replace(key, value)
						elif repeat < 0:
							while key in line:
								line = line.replace(key, value)
						else:
							pass

				if "if(" in line:
					line = line.replace("if(", "if ").replace("):", ":")

				if "while(" in line:
					line = line.replace("while(", "while ").replace("):", ":")

				if "if (" in line:
					line = line.replace("if (", "if ").replace("):", ":")

				if "while (" in line:
					line = line.replace("while (", "while ").replace("):", ":")

				temp_file.write(line)

			source_file.close()
			temp_file.close()

			os.remove(file_name)
			os.rename(temp_file_name, file_name)

			file_counter += 1

		if os.path.isdir(file_name):
			os.chdir(file_name)
			print "In folder:", file_name
			beautify(os.listdir(os.getcwd()))
			os.chdir('..')
			folder_counter += 1

def cleanComments(file_list):
	for file_name in file_list:
		if os.path.isfile(file_name):
			file_name_split = file_name.split(".")
			if len(file_name_split) < 2:
				continue
			file_ext = file_name_split[1]
			if not file_ext == "py":
				continue

			print "cleaning comments from file:", file_name

			timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
			temp_file_name = timestamp + "_" + file_name

			temp_file = open(temp_file_name, "w")
			source_file = open(file_name)

			is_single_quote_started = False
			is_double_quote_started = False
			while True:
				line = source_file.readline()
				if not line:
					break

				if "'''" in line:
					if is_double_quote_started:
						continue
					line_split = line.split("'''")
					if is_single_quote_started:
						line = line_split[1]
						is_single_quote_started = False
					else:
						line = line_split[0]
						is_single_quote_started = True

					if len(line) == 0:
						line = "\n"
					else:
						if line[-1] != "\n":
							line += "\n"

				if '"""' in line:
					if is_single_quote_started:
						continue
					line_split = line.split('"""')
					if is_double_quote_started:
						line = line_split[1]
						is_double_quote_started = False
					else:
						line = line_split[0]
						is_double_quote_started = True

					if len(line) == 0:
						line = "\n"
					else:
						if line[-1] != "\n":
							line += "\n"

				if is_single_quote_started or is_double_quote_started:
					continue

				if "#" in line:
					line_split = line.split("#")
					line = line_split[0]
					line_has_char = False
					for char in line:
						if char != " " and char != "\t":
							line_has_char = True
							break

					if line_has_char:
						line += "\n"
					else:
						continue

				temp_file.write(line)

			source_file.close()
			temp_file.close()

			os.remove(file_name)
			os.rename(temp_file_name, file_name)

		if os.path.isdir(file_name):
			os.chdir(file_name)
			print "In folder:", file_name
			cleanComments(os.listdir(os.getcwd()))
			os.chdir('..')

def beautifyPath(path):
	os.chdir(path)
	beautify(os.listdir(os.getcwd()))
	beautify(os.listdir(os.getcwd()))
	cleanComments(os.listdir(os.getcwd()))
	print line_counter / 2, "lines has been revised in", file_counter / 2, "files in", folder_counter / 2, "folders"

beautifyPath(getPath())

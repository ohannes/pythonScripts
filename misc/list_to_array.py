ftr = open("list", "r")
lines = ftr.readlines()
ftr.close()

array_str = ""
array_str += "["

index = -1

for line in lines:
	
	index += 1
	
	#if line == "" or line == " " or line == "\t" or line == "\n":
	#	continue
		
	#print "line: ", line[:-2]
	#print "line: ", len(line[:-2])
	array_str += '"' + line[:-2] + '"'
	
	if index != len(lines) - 1:
		array_str += ", "

array_str += "]"

print array_str

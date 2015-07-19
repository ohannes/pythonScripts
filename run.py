import os, sys
from ohannes import *

src = "/home/arcelik/pythonScripts"
list_dir = os.listdir(src)

script_file = sys.argv[1]
run_command = "python " + src + "/"

for file_name in list_dir:
	if os.path.isdir(src + "/" + file_name):
		if os.path.exists(src + "/" + file_name + "/" + script_file + ".py"):
			run_command += file_name + "/" + script_file + ".py"
			i = 2
			while i < len(sys.argv):
				run_command += " " + sys.argv[i]
				i += 1
			print START
			os.system(run_command)
			sys.exit(END)

printMessage(ERROR, "script " + script_file + " does not exist", "run")

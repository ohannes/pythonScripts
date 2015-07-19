import os, sys

no_arg_error = "no argument provided"
min_num_of_arg = 2
min_num_of_split = 2
grep_str = "grep"
py_scripts_str = "pythonScripts"

SPACE = " "
OUT_DIR = " > "
ps_cmd_core = "ps aux | grep"
output_file_name = "kill_all_mine.txt"

kill_cmd_core = "kill"
kill_cmd_param = "-9"

if len(sys.argv) < min_num_of_arg:
	sys.exit(no_arg_error)


keyword = sys.argv[1]
cmd =  ps_cmd_core + SPACE + sys.argv[1] + OUT_DIR + output_file_name

os.system(cmd)

ftr = open(output_file_name)
lines = ftr.readlines()
ftr.close()

for i in range(len(lines)):
	if i == len(lines) - 1:
		break
	line = lines[i]
	if grep_str in line or py_scripts_str in line:
		continue
	s = line.split()
	if len(s) < 2:
		continue
	pid = s[1]
	if int(pid, 10) == os.getpid():
		continue
	cmd = kill_cmd_core + SPACE + kill_cmd_param + SPACE + pid
	os.system(cmd)

os.remove(output_file_name)

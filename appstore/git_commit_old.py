import sys, os
sys.path.append(os.environ["ohannes"])
from ohannes import *

run_cmd_flag = False
if len(sys.argv) > 1:
	run_cmd_flag = getBoolArg(1, 1)

temp_file = "temp"
modified_str = "modified:"
git_add_cmd = "git add"
git_status_cmd = "git status"
redirect_output = " > "


os.system(git_status_cmd + redirect_output + temp_file)
temp_lines = getFileLines(temp_file)
os.remove(temp_file)

output_str = git_add_cmd + SPACE
for line in temp_lines:
	if modified_str in line:
		split = line.split()
		file_to_commit = split[LAST_INDEX]
		file_to_commit.replace(SPACE, EMPTY_STR)
		file_to_commit.replace(TAB, EMPTY_STR)
		file_to_commit.replace(EOL, EMPTY_STR)
		output_str += file_to_commit + SPACE

if output_str != git_add_cmd + SPACE:
	if run_cmd_flag:
		os.system(output_str)
	else:
		print output_str
import sys, os
sys.path.append(os.environ["ohannes"])
from ohannes import *

untracked_files_starting = False
untracked_files_started = False
untracked_files_finished = True
run_cmd_flag = False
if len(sys.argv) > 1:
	run_cmd_flag = getBoolArg(1, 1)

temp_file = "temp"

modified_str = "modified:"
deleted_str = "deleted:"
untracked_str = "Untracked files:"
git_add_include_commit_str = '(use "git add <file>..." to include in what will be committed)'
git_add_cmd = "git add"
git_rm_cmd = "git rm"
git_status_cmd = "git status"
redirect_output = " > "

os.system(git_status_cmd + redirect_output + temp_file)
temp_lines = getFileLines(temp_file)
os.remove(temp_file)

add_str = git_add_cmd + SPACE
delete_str = git_rm_cmd + SPACE
for line in temp_lines:
	if untracked_files_started and not SHARP in line:
		untracked_files_finished = True
	if (untracked_files_started and not untracked_files_finished) or (modified_str in line):
		split = line.split()
		file_to_commit = split[LAST_INDEX]
		file_to_commit.replace(SPACE, EMPTY_STR)
		file_to_commit.replace(TAB, EMPTY_STR)
		file_to_commit.replace(EOL, EMPTY_STR)
		if file_to_commit != temp_file and not SHARP in file_to_commit:
			add_str += file_to_commit + SPACE
	elif deleted_str in line:
		split = line.split()
		file_to_delete = split[LAST_INDEX]
		file_to_delete.replace(SPACE, EMPTY_STR)
		file_to_delete.replace(TAB, EMPTY_STR)
		file_to_delete.replace(EOL, EMPTY_STR)
		delete_str += file_to_delete + SPACE
	elif untracked_str in line:
		untracked_files_starting = True
	elif untracked_files_starting and git_add_include_commit_str in line:
		untracked_files_started = True
		untracked_files_finished = False

if add_str != git_add_cmd + SPACE:
	if run_cmd_flag:
		os.system(add_str)
	else:
		print add_str

if delete_str != git_rm_cmd + SPACE:
	if run_cmd_flag:
		os.system(delete_str)
	else:
		print delete_str
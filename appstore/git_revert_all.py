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
git_checkout_cmd = "git checkout"
rm_cmd = "rm"
git_status_cmd = "git status"
redirect_output = " > "

os.system(git_status_cmd + redirect_output + temp_file)
temp_lines = getFileLines(temp_file)
os.remove(temp_file)

checkout_str = git_checkout_cmd + SPACE
remove_str = rm_cmd + SPACE
for line in temp_lines:
	if untracked_files_started and not SHARP in line:
		untracked_files_finished = True
	if untracked_files_started and not untracked_files_finished:
		split = line.split()
		file_to_commit = split[LAST_INDEX]
		file_to_commit.replace(SPACE, EMPTY_STR)
		file_to_commit.replace(TAB, EMPTY_STR)
		file_to_commit.replace(EOL, EMPTY_STR)
		if file_to_commit != temp_file and not SHARP in file_to_commit:
			remove_str += file_to_commit + SPACE
	elif modified_str in line or deleted_str in line:
		split = line.split()
		file_to_commit = split[LAST_INDEX]
		file_to_commit.replace(SPACE, EMPTY_STR)
		file_to_commit.replace(TAB, EMPTY_STR)
		file_to_commit.replace(EOL, EMPTY_STR)
		if file_to_commit != temp_file and not SHARP in file_to_commit:
			checkout_str += file_to_commit + SPACE
	elif untracked_str in line:
		untracked_files_starting = True
	elif untracked_files_starting and git_add_include_commit_str in line:
		untracked_files_started = True
		untracked_files_finished = False

if checkout_str != git_checkout_cmd + SPACE:
	if run_cmd_flag:
		os.system(checkout_str)
	else:
		print checkout_str

if remove_str != rm_cmd + SPACE:
	if run_cmd_flag:
		os.system(remove_str)
	else:
		print remove_str
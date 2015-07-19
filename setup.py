import os, sys

cwd = os.getcwd()

home_path = os.path.expanduser('~')

config = open(home_path + "/.bashrc", "a")
export_cmd = "\nexport ohannes=" + cwd + "\n"
config.write(export_cmd)
config.close()

ftw = open("ohannes", "w")
ftw.write("#ohannes\n")
ftw.write("python " + cwd + "/run.py $1 $2 $3 $4 $5 $6 $7 $8 $9\n")
ftw.close()

os.system("sudo mv ohannes /usr/bin/ohannes")
os.system("sudo chmod +x /usr/bin/ohannes")
print "usage:"
print "\t ohannes <script_name> [params]"
print "\t !!! DO NOT FORGET TO RESTART THE CONSOLE !!!"
print "END"
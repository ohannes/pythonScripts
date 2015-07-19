import os
import sys

cwd = os.getcwd()

sh_file = open("compileUI", "w")
sh_file.write("cd " + cwd)
sh_file.write("\n")
sh_file.write("python compileUI.py $1")
sh_file.close()

os.system("sudo mv compileUI /usr/bin")
os.system("sudo chmod +x /usr/bin/compileUI")

print "Now you can compile the webui for ky with the following command any where in your file system:"
print "\tcompileUI <DEBUG_MODE>"
print "DEBUG_MODE is an optional parameter whose value is false as default"
print "You can compile with debug true as the following:"
print "\tcompileUI t"

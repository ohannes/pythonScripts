import os

scriptPath = "/home/arcelik/pythonScripts"
usrBinPath = "/usr/bin"
SCRIPT_NAME = "compileApp"
CONF_FILE = "pythonScripts"

if not os.path.exists(scriptPath):
	os.system("mkdir " + scriptPath)

if not os.path.exists(scriptPath + "/" + SCRIPT_NAME + ".py"):
	os.system("mv " + SCRIPT_NAME + ".py" + " " + scriptPath + "/" + SCRIPT_NAME + ".py")

if not os.path.exists(scriptPath + "/" + CONF_FILE + ".conf"):
	os.system("mv " + CONF_FILE + ".conf" + " " + scriptPath + "/" + CONF_FILE + ".conf")

if not os.path.exists(usrBinPath + "/" + SCRIPT_NAME):
	os.system("sudo " + "mv " + SCRIPT_NAME + " " + usrBinPath + "/" + SCRIPT_NAME)
	os.system("sudo " + "chmod +x" + " " + usrBinPath + "/" + SCRIPT_NAME)

print SCRIPT_NAME, "has been installed successfully."
print "please run the following command with the required parameter:"
print " compileApp configure YOUR_SRC_PATH"
print "example usage:"
print " compileApp myApp"
print " compileApp myApp f"
print " compileApp myApp t"
print " compileApp myApp true"

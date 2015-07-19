'''
	This script downloads the source code Kaffeine Player.
	Then, it compiles and removes the source code.
	At the end, Kaffeine will be installed on the PC.
'''

import os

def Xchdir(path):
	cwd = str(os.getcwd()).split("/")
	for dirSign in cwd:
		os.chdir('..')
	os.chdir(path)

KAFFEINE_VER = "kaffeine-1.2.2"

#download dependencies
depencyCmd = "sudo apt-get --assume-yes install cmake subversion kdelibs5-dev libxss-dev libx11-dev wget build-essential libxine-dev"
os.system(depencyCmd)

#cd to a path in which Kaffeine will be installed
path = ""
Xchdir(path)

#download tar.gz
downloadCmd = "wget http://sourceforge.net/projects/kaffeine/files/current/kaffeine-1.2.2.tar.gz"
os.system(downloadCmd)

#open tar.gz
openTarCmd = "tar xvzf " + KAFFEINE_VER + ".tar.gz"
os.system(openTarCmd)

#cd to the path where Kaffeine downloaded
Xchdir(KAFFEINE_VER)

#cmake
cmakeCmd = "make ."
os.system(cmakeCmd)

#make
makeCmd = "make"
os.system(makeCmd)

#make install
makeInstallCmd = "sudo make install"
os.system(makeInstallCmd)

#cd to parent path
parentPath = ".."
os.chdir(parentPath)

#remove tar.gz
removeTarCmd = "rm " + KAFFEINE_VER + ".tar.gz"
os.system(removeTarCmd)

#remove source
removeSource = "rm -R " + KAFFEINE_VER
os.system(removeSource)

#restart
restartCmd = "sudo reboot"
os.system(restartCmd)

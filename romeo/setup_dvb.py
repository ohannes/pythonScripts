import os

#enter to home dir
enterHomeCmd = "cd"
print "entering home directory..."
os.system(enterHomeCmd)
print "entered home directory."

#create a clone of media_tree
mediaTreeCmd = "git clone git://linuxtv.org/media_build.git"
print "a git clone of media tree is being created..."
os.system(mediaTreeCmd)
print "clone has been created."

#get required patches
patchCmd = "sudo apt-get install patchutils libproc-processtable-perl"
print "patchutils are being installed..."
os.system(patchCmd)
print "patchutils has been created."

#enter media_build dir
enterMediaCmd = "cd media_build"
print "entering media_build directory..."
os.system(enterMediaCmd)
print "entered media build directory."

#build media_tree
buildCmd = "sudo ./build"
print "media tree is being built..."
os.system(buildCmd)
print "media tree has been built."

#make install
makeInstallCmd = "sudo make install"
print "media tree is being installed..."
os.system(makeInstallCmd)
print "media tree has been installed."

#get dvb-apps
dvbAppsCmd = "sudo apt-get install dvb-apps"
print "dvb apps are being installed..."
os.system(dvbAppsCmd)
print "dvb apps has been installed."

#get required plugins
pluginCmd = "sudo apt-get install libxine1-all-plugins"
print "plugins are being installed..."
os.system(pluginCmd)
print "plugins has been installed."

#get kaffeine
kaffeineCmd = "sudo apt-get install kaffeine"
print "kaffeine app is being installed..."
os.system(kaffeineCmd)
print "kaffeine app has been installed."

#get updates
updateCmd = "sudo apt-get update"
print "getting updates..."
os.system(updateCmd)
print "all updates OK"

#get upgrades
upgradeCmd = "sudo apt-get upgrade"
print "WARNING: Do not forgot to upgrade... Use the following command:"
print "\t" + upgradeCmd

#after plug USB in
print "WARNING: after plugging the DVB USB stick, please check the existence of adapter by the following command:"
print "\tcd /dev/dvb/adapter0"
print "\tls"
print "then, see the following devices:"
print "\tdemux0  dvr0  frontend0  frontend1  net0"

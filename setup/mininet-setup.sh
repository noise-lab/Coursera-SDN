#!/usr/bin/env bash

# We have to downgrade Mininet's version to 2.1.0p2 for the SDX Assignment
# This sucks but we have to ensure compatibility between 
# Mininet & MiniNExT for this assignment. We should be able 
# to get this issue resolved down the line. 

# Make sure that Mininet is uninstalled before this re-installation
cd ~
sudo rm -rf mininet
sudo rm -rf openflow
/usr/bin/yes | sudo pip uninstall mininet
sudo rm `which mn`
sudo rm `which mnexec`
sudo rm /usr/share/man/man1/mn.1*
sudo rm /usr/share/man/man1/mnexec.1*

# Now re-install Mininet
git clone git://github.com/mininet/mininet
pushd mininet
git checkout -b 2.1.0p2 2.1.0p2
./util/install.sh -fn03
popd

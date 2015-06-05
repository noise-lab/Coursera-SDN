#!/usr/bin/env bash

# install packages
sudo apt-get update

sudo apt-get install -y build-essential fakeroot debhelper autoconf \
automake libssl-dev graphviz python-all python-qt4 \
python-twisted-conch libtool git tmux vim python-pip python-paramiko \
python-sphinx

sudo pip install alabaster
sudo apt-get install -y ssh git emacs sshfs

# set up some shortcuts
mkdir ~/bin/
echo "sudo mn -c; sudo mn --topo single,3 --mac --switch ovsk --controller remote" > ~/bin/mininet.sh
chmod 755 ~/bin/mininet.sh

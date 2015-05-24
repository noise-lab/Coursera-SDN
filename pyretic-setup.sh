#!/usr/bin/env bash

# Dependencies install
cd ~
sudo apt-get install -y python-dev screen hping3
sudo pip install networkx bitarray netaddr ipaddr pytest ipdb yappi

# Asynchat installation
wget https://raw.github.com/frenetic-lang/pyretic/master/pyretic/backend/patch/asynchat.py
sudo mv asynchat.py /usr/lib/python2.7/
sudo chown root:root /usr/lib/python2.7/asynchat.py

git clone https://github.com/git/git.git
pushd git/contrib/subtree/
make
sudo install -m 755 git-subtree /usr/lib/git-core
popd
rm -rf git

# Pyretic installation
cd ~  
git clone git://github.com/frenetic-lang/pyretic.git

export PATH=$PATH:$HOME/pyretic:$HOME/pox  
export PYTHONPATH=$HOME/pyretic:$HOME/mininet:$HOME/pox

echo "export PATH=$PATH:$HOME/pyretic:$HOME/pox" >> ~/.bash_profile
echo "export PYTHONPATH=$HOME/pyretic:$HOME/mininet:$HOME/pox" >> ~/.bash_profile
source ~/.bash_profile

#sudo cat /dev/zero > zero.fill; sudo sync; sleep 1; sudo sync; sudo rm -f zero.fill; sudo shutdown -h now

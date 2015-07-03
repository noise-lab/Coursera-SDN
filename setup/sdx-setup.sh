#!/usr/bin/env bash

cd ~

# Install Quagga 
sudo apt-get install -y quagga

# Install MiniNExT
sudo apt-get install -y help2man python-setuptools

git clone https://github.com/USC-NSL/miniNExT.git miniNExT/  
cd miniNExT  
git checkout 1.4.0  
sudo make install

sudo pip install requests

# Install SDX
# Will be provided later
cd ~
git clone https://github.com/sdn-ixp/sdx-ryu.git
cd sdx-ryu
sudo chmod 755 xrs/client.py xrs/route_server.py examples/simple/mininet/sdx_mininext.py
mkdir xrs/ribs
cd ~

# Install ExaBGP
sudo pip install -U exabgp

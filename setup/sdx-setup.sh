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
mkdir asdx
git clone https://github.com/nsg-ethz/supercharged_sdx.git asdx/
sudo chmod 755 ~/asdx/xrs/client.py ~/asdx/xrs/route_server.py ~/asdx/examples/simple/mininet/sdx_mininext.py

mkdir ~/asdx/xrs/ribs

# Install ExaBGP
sudo pip install -U exabgp

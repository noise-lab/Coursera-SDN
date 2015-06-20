#!/usr/bin/env bash

# Install dependencies
sudo apt-get install -y libpcap-dev

sudo pip install psutil bitstring

# Apply patch for POX
cd ~/pox
sudo git remote add netasm-patch https://github.com/PrincetonUniversity/pox
sudo git pull netasm-patch carp

# Install pxpcap
cd ~/pox/pox/lib/pxpcap/pxpcap_c/ 
sudo ./build_linux

# Clone NetASM
cd ~/
git clone https://github.com/NetASM/NetASM-python.git netasm

# Add NetASM to PATH and PYTHONPATH environment variables
echo 'export PATH=$PATH:$HOME/netasm' >> ~/.bash_profile
echo 'export PYTHONPATH=$PYTHONPATH:$HOME/netasm' >> ~/.bash_profile

echo 'alias sudopy="sudo PYTHONPATH=$PYTHONPATH"' >> ~/.bash_profile
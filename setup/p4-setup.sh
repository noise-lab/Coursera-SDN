#!/usr/bin/env bash

cd ~
git clone git://github.com/p4lang/p4factory.git

cd ~/p4factory/
./install.sh

sudo ~/p4factory/tools/veth_setup.sh

cd ~/p4factory/targets/basic_routing/  
make bm  
sudo ./behavioral_model  

cd ~/p4factory/targets/simple_router/  
make bm

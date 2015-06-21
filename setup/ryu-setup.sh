#!/usr/bin/env bash

#  Dependencies for ryu
sudo apt-get install -y python-routes
sudo pip install oslo.config --upgrade
sudo pip install msgpack-python
sudo pip install eventlet

#  Ryu install
pushd ~
git clone git://github.com/osrg/ryu.git
sudo cp /vagrant/setup/ryu-flags.py ~/ryu/ryu/flags.py
pushd ryu
sudo python ./setup.py install

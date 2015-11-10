#!/usr/bin/env bash

wget http://openvswitch.org/releases/openvswitch-2.3.0.tar.gz
tar xf openvswitch-2.3.0.tar.gz
pushd openvswitch-2.3.0
DEB_BUILD_OPTIONS='parallel=8 nocheck' fakeroot debian/rules binary
        popd
sudo dpkg -i openvswitch-common*.deb openvswitch-datapath-dkms*.deb python-openvswitch*.deb openvswitch-pki*.deb openvswitch-switch*.deb
rm -rf *openvswitch*
sudo ln -s /usr/local/bin/controller /usr/bin/ovs-controller

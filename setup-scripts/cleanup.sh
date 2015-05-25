#!/usr/bin/env bash
sudo apt-get clean

# Compact disk space
sudo dd if=/dev/zero of=/EMPTY bs=1M
sudo rm -f /EMPTY

# Clear bash history & exit
cat /dev/null > ~/.bash_history && history -c && exit

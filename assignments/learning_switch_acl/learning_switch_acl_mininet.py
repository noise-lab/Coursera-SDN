#!/usr/bin/python

# ################################################################################
# ##
# ##  https://github.com/NetASM/NetASM-python
# ##
# ##  File:
# ##        single_switch.py
# ##
# ##  Project:
# ##        NetASM: A Network Assembly Language for Programmable Dataplanes
# ##
# ##  Author:
# ##        Muhammad Shahbaz
# ##
# ##  Copyright notice:
# ##        Copyright (C) 2014 Princeton University
# ##      Network Operations and Internet Security Lab
# ##
# ##  Licence:
# ##        This file is a part of the NetASM development base package.
# ##
# ##        This file is free code: you can redistribute it and/or modify it under
# ##        the terms of the GNU Lesser General Public License version 2.1 as
# ##        published by the Free Software Foundation.
# ##
# ##        This package is distributed in the hope that it will be useful, but
# ##        WITHOUT ANY WARRANTY; without even the implied warranty of
# ##        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# ##        Lesser General Public License for more details.
# ##
# ##        You should have received a copy of the GNU Lesser General Public
# ##        License along with the NetASM source package.  If not, see
# ##        http://www.gnu.org/licenses/.

__author__ = 'shahbaz'

# Coursera:
# - Software Defined Networking (SDN) course
# -- Programming Assignment: Simple Router with ACL
# Professor: Nick Feamster
# Author: Muhammad Shahbaz

from optparse import OptionParser

from mininet.node import RemoteController
from mininet.net import Mininet, CLI
from mininet.topo import SingleSwitchTopo
from mininet.log import setLogLevel
from netasm.back_ends.soft_switch.mininet.node import NetASMSwitch


def test():
    op = OptionParser()
    op.add_option('--cli', action="store_true", dest="cli")
    op.add_option('--ports', action="store", dest="ports")

    op.set_defaults(cli=False, ports=2)
    options, args = op.parse_args()

    topo = SingleSwitchTopo(int(options.ports))

    NetASMSwitch.CTL_ADDRESS = "127.0.0.1"
    NetASMSwitch.CTL_PORT = 7791

    net = Mininet(topo, switch=NetASMSwitch, autoSetMacs=True, controller=lambda name: RemoteController(name))

    NetASMSwitch.start_datapath(net.switches, address="127.0.0.1", port=6633)
    net.start()

    if options.cli:
        CLI(net)
    else:
        net.pingAll()

    net.stop()
    NetASMSwitch.stop_datapath()


if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    test()
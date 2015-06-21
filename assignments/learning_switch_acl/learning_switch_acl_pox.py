# ################################################################################
# ##
# ##  https://github.com/NetASM/NetASM-python
# ##
# ##  File:
# ##        table_based_pass_through.py
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

# Coursera:
# - Software Defined Networking (SDN) course
# -- Programming Assignment: Simple Router with ACL
# Professor: Nick Feamster
# Author: Muhammad Shahbaz

from pox.core import core
from pox.lib.util import dpidToStr

from netasm.netasm.core.common import ports_to_bitmap
from netasm.back_ends.soft_switch.api import OutMessage, InMessage, QueryMessage


log = core.getLogger()


def _handle_ConnectionUp(event):
    msg = OutMessage()

    msg.set_policy("netasm.examples.learning_switch_acl.learning_switch_acl_netasm")
    event.connection.send(msg)

    msg.add_table_entry('acl_match_table', 0,
                        {'ipv4_src': (0x0A000001, 0xFFFFFFFF),
                         'ipv4_dst': (0x0A000002, 0xFFFFFFFF)})
    event.connection.send(msg)

    msg.add_table_entry('acl_match_table', 1,
                        {'ipv4_src': (0x0A000002, 0xFFFFFFFF),
                         'ipv4_dst': (0x0A000001, 0xFFFFFFFF)})
    event.connection.send(msg)

    log.info("netasm.examples.learning_switch_acl.learning_switch_acl_netasm for %s",
             dpidToStr(event.dpid))


def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)

    log.info("netasm.examples.learning_switch_acl.learning_switch_acl_netasm running.")
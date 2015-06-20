# Copyright 2013-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Coursera:
# - Software Defined Networking (SDN) course
# -- Programming Assignment: Simple Router with ACL
# Professor: Nick Feamster
# Author: Muhammad Shahbaz

import oftest.dataplane as dataplane
import oftest.pd_base_tests as pd_base_tests

from oftest.testutils import *

from utils import *

from p4_pd_rpc.ttypes import *
from res_pd_rpc.ttypes import *


def setup_default_table_configurations(client, sess_hdl, dev_tgt):
    # Clean all state in the target.
    client.clean_all(sess_hdl, dev_tgt)

    # Set a default action for the ipv4_lpm table.
    result = client.ipv4_lpm_set_default_action__drop(sess_hdl, dev_tgt)
    assert result == 0

    # Set a default action for the forward table.
    result = client.forward_set_default_action__drop(sess_hdl, dev_tgt)
    assert result == 0

    # Set a default action for the acl table.
    result = client.acl_set_default_action__drop(sess_hdl, dev_tgt)
    assert result == 0

    # Set a default action for the send_frame table.
    result = client.send_frame_set_default_action__drop(sess_hdl, dev_tgt)
    assert result == 0


def setup_ipv4_lpm_table_configurations(client, sess_hdl, dev_tgt):
    ip1, ip1_length = "10.0.0.10", 32
    nhop1, port1 = "10.0.0.10", 1
    client.ipv4_lpm_table_add_with_set_nhop(sess_hdl, dev_tgt,
                                            simple_router_acl_ipv4_lpm_match_spec_t(
                                                ipv4_dstAddr=ipv4Addr_to_i32(ip1),
                                                ipv4_dstAddr_prefix_length=ip1_length),
                                            simple_router_acl_set_nhop_action_spec_t(
                                                action_nhop_ipv4=ipv4Addr_to_i32(nhop1),
                                                action_port=port1))

    ip2, ip2_length = "10.0.1.10", 32
    nhop2, port2 = "10.0.1.10", 2
    client.ipv4_lpm_table_add_with_set_nhop(sess_hdl, dev_tgt,
                                            simple_router_acl_ipv4_lpm_match_spec_t(
                                                ipv4_dstAddr=ipv4Addr_to_i32(ip2),
                                                ipv4_dstAddr_prefix_length=ip2_length),
                                            simple_router_acl_set_nhop_action_spec_t(
                                                action_nhop_ipv4=ipv4Addr_to_i32(nhop2),
                                                action_port=port2))


def setup_forward_table_configurations(client, sess_hdl, dev_tgt):
    nhop1, mac1 = "10.0.0.10", "00:04:00:00:00:00"
    client.forward_table_add_with_set_dmac(sess_hdl, dev_tgt,
                                           simple_router_acl_forward_match_spec_t(
                                               routing_metadata_nhop_ipv4=ipv4Addr_to_i32(nhop1)),
                                           simple_router_acl_set_dmac_action_spec_t(
                                               action_dmac=macAddr_to_string(mac1)))

    nhop2, mac2 = "10.0.1.10", "00:04:00:00:00:01"
    client.forward_table_add_with_set_dmac(sess_hdl, dev_tgt,
                                           simple_router_acl_forward_match_spec_t(
                                               routing_metadata_nhop_ipv4=ipv4Addr_to_i32(nhop2)),
                                           simple_router_acl_set_dmac_action_spec_t(
                                               action_dmac=macAddr_to_string(mac2)))


def setup_acl_table_configurations(client, sess_hdl, dev_tgt):
    sport1, dport1 = 4444, 5555
    client.acl_table_add_with__nop(sess_hdl, dev_tgt,
                                   simple_router_acl_acl_match_spec_t(
                                       tcp_srcPort=sport1,
                                       tcp_dstPort=dport1))

    sport2, dport2 = 5555, 4444
    client.acl_table_add_with__nop(sess_hdl, dev_tgt,
                                   simple_router_acl_acl_match_spec_t(
                                       tcp_srcPort=sport2,
                                       tcp_dstPort=dport2))


def setup_send_frame_table_configurations(client, sess_hdl, dev_tgt):
    port1, mac1 = 1, "00:aa:bb:00:00:00"
    client.send_frame_table_add_with_rewrite_mac(sess_hdl, dev_tgt,
                                                 simple_router_acl_send_frame_match_spec_t(
                                                     standard_metadata_egress_port=port1),
                                                 simple_router_acl_rewrite_mac_action_spec_t(
                                                     action_smac=macAddr_to_string(mac1)))

    port2, mac2 = 2, "00:aa:bb:00:00:01"
    client.send_frame_table_add_with_rewrite_mac(sess_hdl, dev_tgt,
                                                 simple_router_acl_send_frame_match_spec_t(
                                                     standard_metadata_egress_port=port2),
                                                 simple_router_acl_rewrite_mac_action_spec_t(
                                                     action_smac=macAddr_to_string(mac2)))


class AclTest(pd_base_tests.ThriftInterfaceDataPlane):
    def __init__(self):
        pd_base_tests.ThriftInterfaceDataPlane.__init__(self, "simple_router_acl")

    def runTest(self):
        # Get connection handle for communicating with the target.
        sess_hdl = self.conn_mgr.client_init(16)
        # Get device handle for the target itself.
        dev_tgt = DevTarget_t(0, hex_to_i16(0xFFFF))

        # Setup table configurations
        setup_default_table_configurations(self.client, sess_hdl, dev_tgt)
        setup_ipv4_lpm_table_configurations(self.client, sess_hdl, dev_tgt)
        setup_forward_table_configurations(self.client, sess_hdl, dev_tgt)
        setup_acl_table_configurations(self.client, sess_hdl, dev_tgt)
        setup_send_frame_table_configurations(self.client, sess_hdl, dev_tgt)

        # Generate sample packets to send through the target

        # Test packet #1
        pkt = simple_tcp_packet(pktlen=100,
                                eth_dst='FF:FF:FF:FF:FF:FF',
                                eth_src='00:04:00:00:00:01',
                                ip_src='10.0.1.10',
                                ip_dst='10.0.0.10',
                                tcp_sport=4444,
                                tcp_dport=5555)

        exp_pkt = simple_tcp_packet(pktlen=100,
                                    eth_dst='00:04:00:00:00:00',
                                    eth_src='00:aa:bb:00:00:00',
                                    ip_src='10.0.1.10',
                                    ip_dst='10.0.0.10',
                                    ip_ttl=63,
                                    tcp_sport=4444,
                                    tcp_dport=5555)

        # Send the packet through the dataplane via its port 2.
        self.dataplane.send(2, str(pkt))
        # Verify if the packet is received from the dataplane on port 1.
        verify_packets(self, exp_pkt, [1])

        # Test packet #2
        pkt = simple_tcp_packet(pktlen=100,
                                eth_dst='FF:FF:FF:FF:FF:FF',
                                eth_src='00:04:00:00:00:00',
                                ip_src='10.0.0.10',
                                ip_dst='10.0.1.10',
                                tcp_sport=5555,
                                tcp_dport=4444)

        exp_pkt = simple_tcp_packet(pktlen=100,
                                    eth_dst='00:04:00:00:00:01',
                                    eth_src='00:aa:bb:00:00:01',
                                    ip_src='10.0.0.10',
                                    ip_dst='10.0.1.10',
                                    ip_ttl=63,
                                    tcp_sport=5555,
                                    tcp_dport=4444)

        # Send the packet through the dataplane via its port 2.
        self.dataplane.send(1, str(pkt))
        # Verify if the packet is received from the dataplane on port 1.
        verify_packets(self, exp_pkt, [2])

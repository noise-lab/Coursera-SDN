'''
Coursera:
- Software Defined Networking (SDN) course
-- Module 8 Programming Assignment

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta
'''

##################################################################
# Author: Hyojoon Kim
# * Run
#   - pox.py pox.misc.pox_gardenwall pox.forwarding.l2_learning
#
# * Mininet
#   - sudo mn --controller=remote,ip=127.0.0.1 --mac --arp --switch ovsk --link=tc --topo=single,5
#
# * Events
#   - python json_sender.py -n infected -l True --flow="{srcmac=00:00:00:00:00:01}" -a 127.0.0.1 -p 5000}
#   - python json_sender.py -n exempt -l True --flow="{srcmac=00:00:00:00:00:01}" -a 127.0.0.1 -p 5000}
#   - python json_sender.py -n exempt -l False --flow="{srcmac=00:00:00:00:00:01}" -a 127.0.0.1 -p 5000}
#   - python json_sender.py -n infected -l False --flow="{srcmac=00:00:00:00:00:01}" -a 127.0.0.1 -p 5000}
##################################################################



from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
from pox.lib.util import dpidToStr
from pox.lib.addresses import EthAddr
from pox.lib.addresses import IPAddr
from collections import namedtuple
import os
from pyretic.kinetic.drivers.json_event import JSONEvent
from pox.misc.rewrite import build_clear_rule
from pox.misc.rewrite import build_rewrite_rule
import pox.lib.packet as pkt
''' Add your imports here ... '''
from csv import DictReader

log = core.getLogger()
policyFile = "%s/pox/pox/misc/firewall-policies.csv" % os.environ[ 'HOME' ]  

''' Add your global variables here ... '''
Policy = namedtuple('Policy', ('dl_src', 'dl_dst'))

class Firewall (EventMixin):

    def __init__ (self):
        self.listenTo(core.openflow)

        # JSON event listener
        json_event = JSONEvent()
        json_event.register_callback(self.event_handler)

        # The Switch
        self.eventSwitch = None

        # flow--state map
        self.flow_state_map = {}

        log.debug("Enabling Firewall Module")
 
    def rule_update(self, flow):
        infected_state = self.get_flowstate_map(flow, 'infected')
        exempt_state = self.get_flowstate_map(flow, 'exempt')
        
        ### --- Add your logic here ---- ###
        
        # Forward to gardenwall if both True.


        # Else if infected is True, drop.


        # Else allow by default (check clear_block(flow))
 

    def event_handler(self, event):
        print 'Event arrived.'
        print '   Flow: ', event.flow
        print '   Event name: ', event.name
        print '   Value: ', event.value

        # Save to flow-state map
        self.save_flowstate_map(event.flow, event.name, event.value.title())
        print self.flow_state_map

        self.rule_update(event.flow)

    def clear_block(self, flow):
        msg = of.ofp_flow_mod()
        msg.command = of.ofp_flow_mod_command_rev_map['OFPFC_DELETE']
        msg.priority = 42
        srcmac_field = flow.get('srcmac')

        if srcmac_field is not None:
            msg.match.dl_src = EthAddr(str(flow['srcmac']))
            msg.match.dl_type =  pkt.ethernet.IP_TYPE

            if self.eventSwitch is not None:
                print 'Send clear message.'
                self.eventSwitch.connection.send(msg)
 
    def install_block(self, flow):
        msg = of.ofp_flow_mod()
        msg.command = of.ofp_flow_mod_command_rev_map['OFPFC_MODIFY']
        msg.priority = 42
        srcmac_field = flow.get('srcmac')

        if srcmac_field is not None:
            msg.match.dl_src = EthAddr(str(flow['srcmac']))
            msg.match.dl_type =  pkt.ethernet.IP_TYPE

            if self.eventSwitch is not None:
                print 'Send block message.'
                self.eventSwitch.connection.send(msg)
                msg.command = of.ofp_flow_mod_command_rev_map['OFPFC_ADD']
                self.eventSwitch.connection.send(msg)

    def save_flowstate_map(self, flow, state, value):
        if flow is not None:
            if self.flow_state_map.has_key(flow):
                state_map = self.flow_state_map[flow]
                state_map[state] = value
            else:
                state_map = {}
                state_map[state] = value
                self.flow_state_map[flow] = state_map
        
    def get_flowstate_map(self, flow, state):
        value = None
        if flow is not None and self.flow_state_map.has_key(flow):
            state_map = self.flow_state_map[flow]
            value = state_map.get(state)
        return value

    def read_policies (self, file):
        if os.path.isfile(file) is False:
            policies = {}
        else: 
            with open(file, 'r') as f:
                reader = DictReader(f, delimiter = ",")
                policies = {}
                for row in reader:
                    policies[row['id']] = Policy(row['mac_0'], row['mac_1'])
        return policies

    def _handle_ConnectionUp (self, event):    
        ''' Add your logic here ... '''
        policies = self.read_policies(policyFile)

        # Save dpid
        self.eventSwitch = event
    
        for policy in policies.itervalues():
            msg = of.ofp_flow_mod()
            msg.priority = 42
            msg.match.dl_src = EthAddr(policy.dl_src)
            msg.match.dl_dst = EthAddr(policy.dl_dst)
            event.connection.send(msg)
    
        log.debug("Firewall rules installed on %s", dpidToStr(event.dpid))

def launch ():
    '''
    Starting the Firewall module
    '''
    core.registerNew(Firewall)

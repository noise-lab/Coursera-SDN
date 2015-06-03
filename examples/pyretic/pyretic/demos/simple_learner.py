################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *

class simplelearn(DynamicPolicy):
    """Standard MAC-learning logic"""
    def update_policy(self):
        """Update the policy based on current forward and query policies"""
        self.policy = self.forward + self.query

    def learn_new_MAC(self,pkt):
        """Update forward policy based on newly seen (mac,port)"""
        self.forward = if_(match(dstmac=pkt['srcmac'],
                                switch=pkt['switch']),
                          fwd(pkt['inport']),
                          self.forward) 
        self.update_policy()

    def __init__(self):
        super(simplelearn,self).__init__()
    	self.flood = flood()           # REUSE A SINGLE FLOOD INSTANCE
	self.query = packets(1,['srcmac','switch'])
        self.query.register_callback(self.learn_new_MAC)
        self.forward = self.flood  # REUSE A SINGLE FLOOD INSTANCE
        self.update_policy()


def mac_learner():
    """Create a dynamic policy object from learn()"""
    return simplelearn()

def main():
    return mac_learner()

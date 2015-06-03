################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Joshua Reich (jreich@cs.princeton.edu)                               #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import mac_learner

class firewall(DynamicPolicy):

  def AddRule (self,switch, srcmac, value=True):
    self.firewall[(switch,srcmac)]=value
    print "Adding firewall rule in %s: %s" % (switch, srcmac) 
    self.policy = parallel([ (match(switch=switch) & 
                              match(srcmac=srcmac)) 
                             for (switch,srcmac) 
                             in self.firewall.keys()])
  def __init__(self):
    # Initialize the firewall
    print "initializing firewall"      
    self.firewall = {}
    super(firewall,self).__init__(true)

    # Add a Couple of Rules
    self.AddRule(1,MAC('00:00:00:00:00:01'))
    self.AddRule(1,MAC('00:00:00:00:00:02'))

    

def main():
    return firewall() >> mac_learner()

################################################################################
# The Pyretic Project                                                          #
# frenetic-lang.org/pyretic                                                    #
# author: Nick Feamster (feamster@cc.gatech.edu)                               #
################################################################################

from pox.lib.addresses import EthAddr

from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.modules.mac_learner import learn

def firewall(self):

  def AddRule (dpidstr, src=0, value=True):
    self.firewall[(dpidstr,src)]=value
    print "Adding firewall rule in %s: %s" % (dpidstr, src) 
  self.AddRule = AddRule

  def DeleteRule (dpidstr, src=0):
     try:
       del self.firewall[(dpidstr,src)]
       print "Deleting firewall rule in %s: %s" % (dpidstr, src)
     except KeyError:
       print "Cannot find in %s: %s" % (dpidstr, src)
  self.DeleteRule = DeleteRule

 # check if packet is compliant to rules before proceeding
  def CheckRule (dpidstr, src=0):
    try:
      entry = self.firewall[(dpidstr, str(src))]
      if (entry == True):
        print "Rule (%s) found in %s: FORWARD" % (src, dpidstr)
      else:
        print "Rule (%s) found in %s: DROP" % (src, dpidstr)
      return entry
    except KeyError:
      print "Rule (%s) NOT found in %s: DROP" % (src, dpidstr)
      return False
  self.CheckRule = CheckRule

  #
  # Pyretic Policies start here
  #

  def update_policy():
    self.policy = self.fwpolicy + self.query
  self.update_policy = update_policy

  def initialize():

    # Initialize the firewall
    print "initializing firewall"      
    self.firewall = {}

    # Add a Couple of Rules
    self.AddRule(1,'00:00:00:00:00:01')
    self.AddRule(1,'00:00:00:00:00:02')
    
    # Register a callback to process upon packet arrivals
    self.query = packets(None, ['srcmac'])
    self.query.register_callback(check_rules)

    # Set default firewall policy
    self.fwpolicy = drop
    self.update_policy()

  def check_rules(pkt):
    filter_on_mac(pkt)

  def filter_on_mac(pkt):
    # get the host IP from the packet
    host = str(pkt['srcmac'])
   
    if self.CheckRule(pkt['switch'], pkt['srcmac']) == True:
        self.fwpolicy = passthrough
    else:
        self.fwpolicy = drop
    self.update_policy()

  initialize()

def main():
    return dynamic(firewall)() >> dynamic(learn)()

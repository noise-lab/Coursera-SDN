#!/usr/bin/python
'''
Coursera:
- Software Defined Networking (SDN) course
-- Programming Assignment 2

Professor: Nick Feamster
Teaching Assistant: Arpit Gupta, Muhammad Shahbaz
'''

from mininet.topo import Topo
from mininet.util import irange
from mininet.link import TCLink
from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.cli import CLI

class CustomTopo(Topo):
    "Simple Data Center Topology"

    "linkopts - (1:core, 2:aggregation, 3: edge) parameters"
    "fanout - number of child switch per parent switch"
    
    # NOTE: logic has to support setting at least bw and delay parameters for
    # each link.
    
    def __init__(self, linkopts1={}, linkopts2={}, linkopts3={}, fanout=2, **opts):
        # Initialize topology and default options
        Topo.__init__(self, **opts)
        
        # Add your logic here ...
        
        # Add CORE
        core = self.addSwitch('c1')
        
        # Aux variables to count switches and hosts used to assign names
        acount = 1
        ecount = 1
        hcount = 1
        
        # Add Agreggation
        for i in irange(1, fanout):
            #name = str(acount + int(i))
            AggSwitch = self.addSwitch('a%s' % acount)
            self.addLink( core, AggSwitch, **linkopts1)
            acount += 1
            # Add Edge
            for j in irange(1,fanout):
                #name = str(ecount + int(j))
                EdgeSwitch = self.addSwitch('e%s' % ecount)
                self.addLink( AggSwitch, EdgeSwitch, **linkopts2)
                ecount += 1
                # Add hosts
                for k in irange(1, fanout):
                    #name = str(hcount + int(k))
                    host = self.addHost('h%s' % hcount)
                    self.addLink( EdgeSwitch, host, **linkopts3)
                    hcount += 1

def simpleTest():
    
    linkopts1 = {'bw':50, 'delay':'5ms'}
    linkopts2 = {'bw':30, 'delay':'10ms'}
    linkopts3 = {'bw':10, 'delay':'15ms'}

    topo = CustomTopo(linkopts1, linkopts2, linkopts3, fanout=3)
    #topo = CustomTopo(fanout=3)
    print "c. Firing up Mininet"
    net = Mininet(topo=topo, link=TCLink)
    net.start()
    h1 = net.get('h1')
    h27 = net.get('h27')
    
    print "d. Starting Test"
    # Start pings
    outputString = h1.cmd('ping', '-c6', h27.IP())
    
    print outputString
    
    print "d.bis Cli"
    CLI(net)
 
    print "e. Stopping Mininet"
    net.stop()
    
if __name__ == '__main__':
    # Tell mininet to print useful information
    setLogLevel('info')
    simpleTest()    

#topos = { 'custom': ( lambda: CustomTopo() ) }


# <a name="h.4k3vsjjdfqv6"></a><span class="c16">Using Mininet and Mininet Python API</span>

<span>In this exercise, you will be learning how to build custom topologies using Mininet Python API and how certain parameters like bandwidth, delay, loss and queue size can be set individually for different links in the topology. You’ll also learn how to do performance testing of these custom topologies using ping and iperf.</span>

<span></span>

<span>After the overview, you will be asked to create and submit your own custom topology based on the most common 3-tier Datacenter architecture i.e., core, aggregation and edge. More details on creating and submitting the code will be provided later on in the instructions. So, make sure that you follow each step carefully.</span>

<span></span>

# <a name="h.4k3vsjjdfqv6"></a><span class="c16">Overview</span>

<span></span>

<span>The network you'll use in this exercise includes hosts and switches connected in a linear topology, as shown in the figure below.</span>

<span></span>

![](https://docs.google.com/drawings/d/sAYbXRCYLjeMAgYFtyNCK8Q/image?w=552&h=483&rev=7&ac=1 "https://docs.google.com/drawings/d/sAYbXRCYLjeMAgYFtyNCK8Q/image?w=552&h=483&rev=7&ac=1")

<span class="c4">Figure 1: hosts and switches connected in a linear topology</span>

## <a name="h.le3k34tab4o5"></a><span class="c16">Creating Topology</span>

<span></span>

<span class="c10">Mininet supports</span> <span class="c10 c28">parametrized topologies</span><span class="c10">. With a few lines of Python code, you can create a flexible topology which can be configured based on the parameters you pass into it, and reused for multiple experiments.</span>

<span></span>

<span class="c10">For example, here is a simple network topology (based on Figure 1) which consists of a specified number of hosts (</span><span class="c10 c0">h1</span><span class="c10"> through</span> <span class="c10 c0">hN</span><span class="c10">) connected to their individual switches (</span><span class="c10 c0">s1</span><span class="c10"> through</span> <span class="c10 c0">sN</span><span class="c10">):</span>

<span></span>

### <a name="h.inagbam49gdf"></a><span>Linear Topology (without Performance Settings)</span>

```bash
#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class LinearTopo(Topo):
   "Linear topology of k switches, with one host per switch."

   def __init__(self, k=2, **opts):
       """Init.
           k: number of switches (and hosts)
           hconf: host configuration options
           lconf: link configuration options"""

       super(LinearTopo, self).__init__(**opts)

       self.k = k

       lastSwitch = None
       for i in irange(1, k):
           host = self.addHost('h%s' % i)
           switch = self.addSwitch('s%s' % i)
           self.addLink( host, switch)
           if lastSwitch:
               self.addLink( switch, lastSwitch)
           lastSwitch = switch

def simpleTest():
   "Create and test a simple network"
   topo = LinearTopo(k=4)
   net = Mininet(topo)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   net.stop()

if __name__ == '__main__':
   # Tell mininet to print useful information
   setLogLevel('info')
   simpleTest()
```

<span></span>

<span>The important</span> <span>classes, methods, functions and variables in the above code include:</span>

<span></span>

1.  <span class="c0">Topo</span><span>: the base class for Mininet topologies</span>
2.  <span class="c0">addSwitch()</span><span>: adds a switch to a topology and returns the switch name</span>
3.  <span class="c0">addHost()</span><span>: adds a host to a topology and returns the host name</span>
4.  <span class="c0">addLink()</span><span>: adds a bidirectional link to a topology (and returns a link key, but this is not important). Links in Mininet are bidirectional unless noted otherwise.</span>
5.  <span class="c0">Mininet</span><span>: main class to create and manage a network</span>
6.  <span class="c0">start()</span><span>: starts your network</span>
7.  <span class="c0">pingAll()</span><span>: tests connectivity by trying to have all nodes ping each other</span>
8.  <span class="c0">stop()</span><span>: stops your network</span>
9.  <span class="c0">net.hosts</span><span>: all the hosts in a network</span>
10.  <span class="c0">dumpNodeConnections()</span><span>: dumps connections to/from a set of nodes.</span>
11.  <span class="c0">setLogLevel( 'info' | 'debug' | 'output' )</span><span>: set Mininet's default output level; 'info' is recommended as it provides useful information.</span>

<span></span>

<span>Additional example code may be found in</span> <span class="c18 c16">[mininet/examples](https://github.com/mininet/mininet/tree/master/examples)</span><span>.</span>

<span></span>

## <a name="h.knrcysl170ty"></a><span class="c16">Setting Performance Parameters</span>

<span></span>

<span>In addition to basic behavioral networking, Mininet provides performance limiting and isolation features, through the</span> <span class="c0">CPULimitedHost</span><span> and</span> <span class="c0">TCLink</span><span> classes.</span>

<span></span>

<span>There are multiple ways that these classes may be used, but one simple way is to specify them as the default host and link classes/constructors to</span> <span class="c0">Mininet()</span><span>, and then to specify the appropriate parameters in the topology.</span>

<span></span>

### <a name="h.iqpo3gxynvgw"></a><span>Linear Topology (with Performance Settings)</span>

[](#)[](#)

```bash
#!/usr/bin/python

from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import CPULimitedHost
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel

class LinearTopo(Topo):
   "Linear topology of k switches, with one host per switch."

   def __init__(self, k=2, **opts):
       """Init.
           k: number of switches (and hosts)
           hconf: host configuration options
           lconf: link configuration options"""

       super(LinearTopo, self).__init__(**opts)

       self.k = k

       lastSwitch = None
       for i in irange(1, k):
           host = self.addHost('h%s' % i, cpu=.5/k)
           switch = self.addSwitch('s%s' % i)
           # 10 Mbps, 5ms delay, 1% loss, 1000 packet queue
           self.addLink( host, switch, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
           if lastSwitch:
               self.addLink(switch, lastSwitch, bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
           lastSwitch = switch

def perfTest():
   "Create network and run simple performance test"
   topo = LinearTopo(k=4)
   net = Mininet(topo=topo, 
                 host=CPULimitedHost, link=TCLink)
   net.start()
   print "Dumping host connections"
   dumpNodeConnections(net.hosts)
   print "Testing network connectivity"
   net.pingAll()
   print "Testing bandwidth between h1 and h4"
   h1, h4 = net.get('h1', 'h4')
   net.iperf((h1, h4))
   net.stop()

if __name__ == '__main__':
   setLogLevel('info')
   perfTest()
```
<span class="c4"></span>

<span>Some important methods and parameters:</span>

<span></span>

<span class="c0">self.addHost(name, cpu=f):</span> <span>This allows you to specify a fraction of overall system CPU resources which will be allocated to the virtual host.</span>

<span class="c0"></span>

<span class="c0">self.addLink( node1, node2, bw=10, delay='5ms', max_queue_size=1000, loss=1, use_htb=True)</span><span>: adds a bidirectional link with bandwidth, delay and loss characteristics, with a maximum queue size of 1000 packets using the Hierarchical Token Bucket rate limiter and netem delay/loss emulator. The parameter bw is expressed as a number in Mb/s; delay is expressed as a string with units in place (e.g. '5ms', '100us', '1s'); loss is expressed as a percentage (between 0 and 100); and max_queue_size is expressed in packets.</span>

<span></span>

<span>You may find it useful to create a Python dictionary to make it easy to pass the same parameters into multiple method calls, for example:</span>

<span></span>

<span></span>

[](#)[](#)

```bash
linkopts = dict(bw=10, delay='5ms', loss=1, max_queue_size=1000, use_htb=True)
’’’
alternately: linkopts = {'bw':10, 'delay':'5ms', 'loss':1, 'max_queue_size':1000, 'use_htb':True}
’’’
self.addLink(node1, node2, **linkopts)
```

<span></span>

## <a name="h.hwnyfoxx5fhy"></a><span class="c16">Running in Mininet</span>

<span></span>

<span>To run the custom topology you have created above, follow the instructions below:</span>

<span></span>

1.  <span>Create a LinearTopo.py script on your Mininet VM and copy the contents of Linear Topology (without Performance Settings), listed above in it.</span>
2.  <span>Make the script executable</span>

<span>$</span><span class="c0"> chmod u+x LinearTopo.py</span>

1.  <span>Execute the script</span>

<span class="c0">        </span><span>$</span><span class="c0">  sudo ./LinearTopo.py</span>

<span class="c0"></span>

### <a name="h.pk3whmaxyfu9"></a><span>Output</span>

<span></span>

[](#)[](#)

```bash
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 h3 h4
*** Adding switches:
s1 s2 s3 s4
*** Adding links:
(h1, s1) (h2, s2) (h3, s3) (h4, s4) (s1, s2) (s2, s3) (s3, s4)
*** Configuring hosts
h1 h2 h3 h4
*** Starting controller
*** Starting 4 switches
s1 s2 s3 s4
Dumping host connections
h1 h1-eth0:s1-eth1
h2 h2-eth0:s2-eth1
h3 h3-eth0:s3-eth1
h4 h4-eth0:s4-eth1
Testing network connectivity
*** Ping: testing ping reachability
h1 -> h2 h3 h4
h2 -> h1 h3 h4
h3 -> h1 h2 h4
h4 -> h1 h2 h3
*** Results: 0% dropped (0/12 lost)
*** Stopping 4 hosts
h1 h2 h3 h4
*** Stopping 4 switches
s1 ...s2 ....s3 ....s4 ...
*** Stopping 1 controllers
c0
*** Done
```

<span class="c0"></span>

<span class="c4"></span>

# <a name="h.hjfz7ws9w6a5"></a><span class="c16">Assignment</span>

## <a name="h.be1fg8g7c7fl"></a><span class="c16">Background</span>

<span>Data center networks typically have a tree-like topology. End-hosts connect to top-of-rack switches, which form the leaves (edges) of the tree; one or more core switches form the root; and one or more layers of aggregation switches form the middle of the tree.  In a basic tree topology, each switch (except the core switch) has a single parent switch.  Additional switches and links may be added to construct more complex tree topologies (e.g., fat tree) in an effort to improve fault tolerance or increase inter-rack bandwidth.</span>

<span></span>

<span>In this assignment, your task is to create a simple tree topology. You will assume each level i.e., core, aggregation, edge and host to be composed of a single layer of switches/hosts with a configurable fanout value (k). For example, a simple tree network having a single layer per each level and a fanout of 2 looks like:</span>

<span></span>

![](https://docs.google.com/drawings/d/sYxg20Rqg7HGDIWATY8AXhA/image?w=610&h=271&rev=1&ac=1 "Image: https://docs.google.com/drawings/d/sYxg20Rqg7HGDIWATY8AXhA/image?w=610&h=271&rev=1&ac=1")

<span>Figure 2: Simple Tree Topology with Fanout 2</span>

<span></span>

<span>To start this assignment update the course's Github repo (by default, ```Coursera-SDN```) on your host machine using ```git pull```. Turn on your guest VM (if it is turned off) using ```vagrant up```. Now ssh into the guest VM using ```vagrant ssh```. Go to the directory with the updated code base in your guest VM. 
```bash
cd /vagrant/assignments/mininet-topology
```
</span>

<span> It consists of two files: </span>

1.  ```CustomTopo.py```: a sekleton class which you will update with the logic for creating the datacenter topology described above.</span>
2.  ```submit.py```: used to submit your code and output to the coursera servers for grading. You don’t have to do any modifications in here.</span>

<span></span>

## <a name="h.1fw61dr7jo8p"></a><span class="c16">CustomTopo.py</span>

<span></span>

<span>The skeleton class takes following arguments as input:</span>

<span></span>

1.  <span class="c0">linkopts1</span><span>: for specifying performance parameters for the links between core and aggregation switches.</span>
2.  <span class="c0">linkopts2</span><span>: for specifying performance parameters for the links between aggregation and edge switches.</span>
3.  <span class="c0">linkopts3</span><span>: for specifying performance parameters for the links between edge switches and host</span>
4.  <span class="c0">Fanout</span><span>: to specify fanout value i.e., number of childs per node.</span>

<span></span>

<span class="c11">Your logic should support setting at least</span> <span class="c0 c11">bw</span><span class="c11"> and</span> <span class="c0 c11">delay</span><span class="c11"> parameters for each link.</span>

<span></span>

## <a name="h.j87ks6oefd6"></a><span class="c16">Submitting your Code</span>

<span></span>

<span>To submit your code, run the ```submit.py``` script:</span>

<span></span>

```bash
$ sudo python submit.py
```

<span></span>

<span>Make sure that</span> <span class="c0">CustomTopo.py</span> <span>is in the same directory as</span> <span class="c0">submit.py</span><span>. Your mininet VM should have internet access by default, but still verify that it has internet connectivity (i.e., eth0 set up as NAT). Otherwise submit.py will not be able to post your code and output to our coursera servers.</span>

<span></span>

<span>The submission script will ask for your login and password. This password is not the general account password, but an assignment-specific password that is uniquely generated for each student. You can get this from the assignments listing page.</span>

```bash
vagrant@coursera-sdn:/vagrant/assignments/mininet-topology$ sudo python submit.py 
==
== [sandbox] Submitting Solutions 
==
Login (Email address): <Your email id>
One-time Password (from the assignment page. This is NOT your own accounts password): <Your assignment-specific password>

== Connecting to Coursera ... 
Hello! These are the assignment parts that you can submit:
1) Create Custom Topology
Please enter which part you want to submit (1-1): <Part of the assignment you want to submit, 1 in this case>
```

<span></span>

<span>Once finished, it will prompt the results on the terminal (either passed or failed).</span>

<span></span>

<span>Note, if during the execution</span> <span class="c0">submit.py</span> <span>script crashes for some reason or you terminate it using CTRL+C, make sure to clean mininet environment using:</span>

<span></span>

```bash
$ sudo mn -c
```


<span class="c0"></span>

<span>Also, if it still complains about the controller running. Execute the following command to kill it:</span>

<span></span>
```bash
$ sudo fuser -k 6633/tcp
```
* * *

# <a name="h.febi5qeveedy"></a>

<span></span>

<span>* These instructions are adapted from</span> <span class="c18 c16">[mininet.org](http://mininet.org)</span><span> and</span> <span class="c16 c18">[wisc-cs838](http://pages.cs.wisc.edu/~akella/CS838)</span>

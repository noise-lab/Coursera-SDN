# <a name="h.uvxhnin3m725"></a><span class="c48 c2 c26 c11">Introduction</span>

<span class="c2">In this exercise, you will learn how to configure and program a Software Defined Internet Exchange Point (SDX). An Internet Exchange Point (IXP) is a location on the network where different independently operated networks (sometimes also called autonomous systems, or domains) exchange traffic with each other.</span>

<span class="c2">There is growing interest in applying Software Deﬁned Networking (SDN) could make some aspects of wide-area network management easier by giving operators direct control over packet-processing rules that match on multiple header ﬁelds and perform a variety of actions. Internet exchange points (IXPs) are a compelling place to start, given their central role in interconnecting many networks and their growing importance in bringing popular content closer to end users.  The recent paper “</span><span class="c42">[SDX: A Software Defined Internet Exchange](http://www.google.com/url?q=http%3A%2F%2Fgtnoise.net%2Fpapers%2F2014%2Fgupta-sigcomm2014.pdf&sa=D&sntz=1&usg=AFQjCNFN92u6bx1uHl6aCNZ_Qk3FaGK9ag)</span><span class="c2">” describes some of this promise in greater detail, as well as the implementation of an SDX that you will be using to complete this assignment.</span>

<span class="c2">In this exercise, we’ll explore one implementation of a software defined Internet exchange point (SDX).  This implementation provides new programming abstractions allowing participants to create and run new wide area traffic delivery applications. SDX platform provides a scalable runtime that both, behaves correctly when interacting with BGP, and ensures that the applications do not interfere with each other.</span>

### <span class="c2 c26 c11 c48">Installation</span>
To start this assignment update the course's Github repo (by default, Coursera-SDN) on your host machine using git pull. We updated the ```Vagrantfile``` to install all the required software to run the SDX assignment. Turn on your guest VM (if it is turned off) using vagrant up with provisioning. 
```bash
vagrant reload --provision
```

The SDX setup script installs:
* [Quagga](http://www.nongnu.org/quagga/)
* [MiniNExT](https://github.com/USC-NSL/miniNExT.git)
* [Exabgp](https://github.com/Exa-Networks/exabgp)

SDX's setup script looks like this:
```bash
#!/usr/bin/env bash

cd ~

# Install Quagga 
sudo apt-get install -y quagga

# Install MiniNExT
# MiniNExT dependencies
sudo apt-get install -y help2man python-setuptools

git clone https://github.com/USC-NSL/miniNExT.git miniNExT/  
cd miniNExT  
git checkout 1.4.0  
sudo make install

# Install Requests
sudo pip install requests

# Install SDX
cd ~
git clone https://github.com/sdn-ixp/sdx-ryu.git
cd sdx-ryu
sudo chmod 755 xrs/client.py xrs/route_server.py examples/simple/mininet/sdx_mininext.py
mkdir xrs/ribs
cd ~

# Install ExaBGP
sudo pip install -U exabgp
```

`Note`: We also had to re-provision the Mininet setup to make it work with ```MiniNExT```. Check the `Vagrantfile` to make sure that it has sdx and mininet setup uncommented.

### <a name="h.hefnxat1hpve"></a><span class="c48 c2 c26 c11">Walkthrough</span>

#### <a name="h.35ws6bwun9r5"></a><span class="c2 c6">Overview</span>

<span class="c2">This part of the exercise allows you to get comfortable using the SDX software. You are not required to submit anything. All of the examples in SDX are organized in the directory called</span> <span class="c0">```~/sdx-ryu/examples/```<span class="c2">. We'll focus on the example</span> <span class="c0">```simple```</span><span class="c2">  for the walkthrough.</span>


<span></span>

![](https://d396qusza40orc.cloudfront.net/sdn/images/sigcomm14_mininext.jpg "https://d396qusza40orc.cloudfront.net/sdn/images/sigcomm14_mininext.jpg")

<span class="c4">Figure 1: Example SDX topology.</span>


```172.*``` addresses refer to the IP addresses of the connected router interfaces. ```/24``` IP prefixes are the routes that each router advertises.  ASes A and C each have Pyretic policies, as shown.</span>

<span class="c2">The setup consists of three participants, each representing a participating AS: A, B, and C. Participants A and B each have a single router.  Participant C has two routers connected to the IXP.  These routers are running the</span> <span class="c0">zebra</span><span class="c2"> and</span> <span class="c0">bgpd</span><span class="c2"> daemons, part of the</span> <span class="c32 c2 c10">Quagga</span><span class="c2"> routing engine. We are also using the</span> <span class="c0">MiniNext</span><span class="c2"> emulation tool to create this topology.  MiniNext is a variant of Mininet that gives each node in the topology its own filesystem, thus allowing each node to run its own version of the routing software. The following sites have more information about</span> <span class="c44">[MiniNext](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2FUSC-NSL%2FminiNeXT&sa=D&sntz=1&usg=AFQjCNFtMs5QPPHGlq8urv0_AWCrfMoFeA) </span><span>and</span><span class="c44">[ ](https://www.google.com/url?q=https%3A%2F%2Fgithub.com%2FUSC-NSL%2FminiNeXT&sa=D&sntz=1&usg=AFQjCNFtMs5QPPHGlq8urv0_AWCrfMoFeA)</span><span class="c44">[Quagga](http://www.google.com/url?q=http%3A%2F%2Fwww.nongnu.org%2Fquagga%2F&sa=D&sntz=1&usg=AFQjCNEygXPyuNAp9vmEtGDa65a11fEzyA)</span><span class="c2">[.](http://www.google.com/url?q=http%3A%2F%2Fwww.nongnu.org%2Fquagga%2F&sa=D&sntz=1&usg=AFQjCNEygXPyuNAp9vmEtGDa65a11fEzyA)</span>

#### <a name="h.onujae3nkrvb"></a><span class="c2 c50">Understanding the SDX Setup</span>

<span class="c2">The example setup has two directories:</span> <span class="c0">controller</span><span class="c2"> and</span> <span class="c0">mininet</span><span class="c2">. The</span> <span class="c0">controller</span><span class="c2"> directory has configuration files pertaining to SDX controller; the</span> <span class="c0">mininet</span><span class="c2"> directory has information pertaining to topology configuration, as well as information for configuring communication with the route server.</span>

##### <a name="h.7477fhkt7fm8"></a><span class="c2 c6">Configuring Topology and Routing Information in Mininext</span>

<span class="c2">We</span><span class="c2"> need to set up routers that run a routing engine to exchange BGP routes at the exchange point. Running a routing engine requires a particular filesystem that is not supported for the</span> <span class="c0">Mininet</span><span class="c32 c2 c10"> </span><span class="c2">nodes.  </span><span class="c0">MiniNext</span><span class="c2"> enables a filesystem for its nodes enabling emulation of legacy switches, routers, etc.</span>

<span class="c2">The</span> <span class="c0">mininet</span><span class="c2"> directory has a</span> <span class="c2">Mininext</span><span class="c32 c2 c10"> </span><span class="c2">script (</span><span class="c0">sdx_mininext.py</span><span class="c2">) and a directory containing the configuration of the Quagga router.</span>

<span class="c2">The following excerpt from</span><span class="c2"> </span><span class="c0">```sdx_mininext.py```</span><span class="c2">  shows how each host is set up</span><span class="c2">:</span>

```python

'''Set Quagga service configuration for this node'''
quaggaSvcConfig = { 'quaggaConfigPath' : scriptdir + '/quaggacfgs/' + host.name }

'''Add services to the list for handling by service helper'''
services = {} 
services[quaggaSvc] = quaggaSvcConfig 

'''Create an instance of a host, called a quaggaContainer''' 
quaggaContainer = self.addHost( name=host.name, ip=host.ip, mac=host.mac, 
                               privateLogDir=True, 
                               privateRunDir=True,
                                inMountNamespace=True,    
                                inPIDNamespace=True)
self.addNodeService(node=host.name, service=quaggaSvc,
                                nodeConfig=quaggaSvcConfig)
 

'''Attach the quaggaContainer to the IXP Fabric Switch''' 
self.addLink( quaggaContainer, ixpfabric , port2=host.port)
```

<span class="c2 c11 c16">Figure 2\. Configuring a Quagga router from Mininet.</span> <span class="c2 c11 c16">(sdx_mininext.py)</span>

<span class="c2">The first part of the configuration simply tells Mininet where the configuration for Quagga is and adds a service to the service helper.  The second part of the configuration creates an instance of the host and then adds the quagga service to the host.  Finally, we use the</span> <span class="c0">addLink</span> <span class="c2">function to add a link from the host running Quagga to the part of the topology running the SDX.</span>

<span class="c2">Next, in a different part of</span> <span class="c0">sdx_mininext.py</span><span class="c2">, we configure the SDX interfaces with</span> <span class="c0">ifconfig</span><span class="c2">. Because we now need to do IP routing, we need to explicitly set the host and subnet information for each of those hosts.</span>

```python
print "Configuring participating ASs\n\n"
for host in hosts:
   if host.name=='a1':
   host.cmdPrint('sudo ifconfig lo:1 100.0.0.1 netmask 255.255.255.0 up')
       ...
   if host.name=='b1':
       host.cmdPrint('sudo ifconfig lo:140 140.0.0.1 netmask 255.255.255.0 up')
       ... 
   ...
```

<span class="c2 c11 c16">Figure 3\. Configuring the host interfaces for the SDX setup from witin mininet. (```sdx_mininext.py```)</span>

<span class="c2">The SDX route server is based on ExaBGP and runs in the root namespace. We need to create an interface in the root namespace itself and connect it with the SDX switch.</span>

```python
" Add root node for ExaBGP. ExaBGP acts as route server for SDX. "
root = self.addHost('exabgp', ip = '172.0.255.254/16', inNamespace = False)
self.addLink(root, ixpfabric, port2 = 5)
```

<span class="c11 c16 c40">Figure 4\. Adding the route server host, which we have named “exabgp”, after the software on which the route server is based.</span> <span class="c2 c11 c16">(```sdx_mininext.py```)</span>

<span class="c2">The</span> <span class="c0">mininet</span><span class="c2"> directory also has a</span> <span class="c32 c2 c10">Quagga</span><span class="c2"> config directory. We define BGP configuration for each of the participating</span> <span class="c32 c2 c10">Quagga</span><span class="c2"> router here. BGP configuration for participant A's router (</span><span class="c0">```~/vagrant/sdx-ryu/examples/simple/mininet/configs/a1/bgpd.conf```</span><span class="c2">) looks like this:</span>
```bash
router bgp 100  
bgp router-id 172.0.0.1  
neighbor 172.0.255.254 remote-as 65000  
network 100.0.0.0/24  
network 110.0.0.0/24  
redistribute static
```
<span class="c2 c11 c16">Figure 5\. BGP routing configuration for participant A. (bgpd.conf)</span>

<span class="c2">This configuration indicates that this router has router-id</span> <span class="c0">172.0.0.1</span><span class="c2">, A's AS number is</span> <span class="c0">100</span><span class="c2">  The</span> <span class="c0">neighbor</span><span class="c2"> configuration command tells the node to look for a remote BGP session (SDX’s routeserver ) whose IP address is</span> <span class="c0">172.0.255.254</span><span class="c2"> and whose remote AS is</span> <span class="c0">65000</span><span class="c2">.  The network lines advertise the respective prefixes.</span>

##### <a name="h.mt88cjvu9mdw"></a><span class="c2 c6">Participants' SDX Policies</span>

<span class="c2">The control plane configuration involves defining participant's policies, which entails (1) configuring</span> <span class="c0">```bgp.conf```</span><span class="c2"> for SDX's route server and (2) configuring ```sdx_global.cfg``` to provide each participant's information to the SDX controller.</span>

<span class="c2">The SDX presents a virtual SDX switch abstraction to each participant. Each participant writes policies for its virtual switch without bothering about other participant's policies. This limited view of the network provides desired isolation by ensuring that the participants are not allowed to write rules for other network's traffic. For more details about this abstraction, you can refer to the</span> <span class="c26 c42">[SIGCOMM paper](http://www.google.com/url?q=http%3A%2F%2Fgtnoise.net%2Fpapers%2F2014%2Fgupta-sigcomm2014.pdf&sa=D&sntz=1&usg=AFQjCNFN92u6bx1uHl6aCNZ_Qk3FaGK9ag)</span><span class="c2"> about SDX</span><span class="c2">.</span>

<span class="c2">In this example, participant A has outbound policies defined in</span> <span class="c0">```~/sdx-ryu/examples/simple/controller/participant_policies/participant_1.py```</span><span class="c32 c2 c10">,</span><span class="c2"> which are written as:</span>

```json
{
    "outbound": [
        {
            "match": 
            {
                "tcp_dst": 80
            },
            "action": 
            {
                "fwd": 2
            }
        },
        {
            "match": 
            {
                "tcp_dst": 4321
            },
            "action": 
            {
                "fwd": 3
            }
        },
        {
            "match": 
            {
                "tcp_dst": 4322
            },
            "action": 
            {
                "fwd": 3
            }
        }
    ]
}
```

<span class="c2 c11 c16">Figure 6\. Participant A’s outbound policies. (participant_1.py)</span>

<span class="c2">Each p</span><span class="c2">articipant's policies written in Pyretic. The policy shown above reflects AS A’s policy for perform application-specific peering—it forwards web (i.e., port 80) traffic to peer B, and port 4321–4322 traffic to peer C.  Participant C has inbound policies as defined in</span><span class="c2 c10 c32"> </span><span class="c0">```~/sdx-ryu/examples/simple/controller/participant_policies/participant_3.py```</span><span class="c2">:</span>

```json
{
    "inbound": [
        {
            "match": 
            {
                "tcp_dst": 4321
            },
            "action": 
            {
                "fwd": 0
            }
        },
        {
            "match": 
            {
                "tcp_dst": 4322
            },
            "action": 
            {
                "fwd": 1
            }
        }
    ]
}
```

<span class="c2 c11 c16">Figure 7\. Participant C’s inbound policies. (participant_3.py)</span>

<span class="c2">Participant C has two input ports at the SDX. It writes policies for inbound traffic engineering-- forwarding its port 4321 traffic to its</span> <span class="c2">port[0]</span><span class="c2">, and port 4322 traffic to peer port[1].</span>

<span class="c2">Participant B does not specify any specific policy, so its forwarding proceeds according to default BGP forwarding.</span>

#### <a name="h.ue8z58v6dg2p"></a><span class="c2 c6">Running the SDX Setup</span>


* Step 1\.Launch the topology using MiniNExT (Mininet) [shell#1]:
```bash
    $ cd ~/sdx-ryu/examples/simple/mininet  
    $ sudo ./sdx_mininext.py
 ```
 
 * Step 2\. In a new shell, make the OVS use OpenFlow 1.3 [shell#2]: 
```bash
    $ sudo ovs-vsctl set bridge s1 protocols=OpenFlow13
```

* Step 3\. Now start the Ryu Controller [shell#2]: 

```bash
$ ryu-manager ~/sdx-ryu/ctrl/asdx.py --asdx-dir simple
```

* Step 4\. In a new shell, the Route Server [shell#3]: 
```bash
$ cd ~/sdx-ryu/xrs
$ sudo ./route_server.py simple
```

* Step 5\. Finally, in another new shell start the ExaBGP [shell#4]:
```bash
 $ exabgp ~/sdx-ryu/examples/simple/controller/sdx_config/bgp.conf
```

#### <a name="h.7ckch6gls77e"></a><span class="c2 c6">Sanity Checks</span>

<span class="c2">You can now check to determine whether the participants received the routes from route server.  For example, to see the routes on host a1, type the following:</span>

```bash
mininext> a1 route -n  
Kernel IP routing table  
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface  
140.0.0.0       172.0.1.3       255.255.255.0   UG    0      0        0 a1-eth0  
150.0.0.0       172.0.1.4       255.255.255.0   UG    0      0        0 a1-eth0  
172.0.0.0       0.0.0.0         255.255.0.0     U     0      0        0 a1-eth0
```

<span class="c2">Specifically, you should see two entries in A’s routing table for 140.0.0.0/8 and 150.0.0.0/8 whose next-hop IP addresses are 172.0.1.3 & 172.0.01.4. These are the virtual next-hops for the two prefixes. You can find more details about the virtual next-hops from the section 4.2 of SDX's [SIGCOMM paper](http://www.cs.princeton.edu/~arpitg/pdfs/sigc056.pdf)</span>

#### <a name="h.uxkh081ccb6a"></a><span class="c2 c6">Testing SDX Policies</span>

As a quick recap, A’s app-specific policy can be represented as:

```python
match(dstport = 80) >>  fwd(B) + match(dstport=4321/4322) >> fwd(C)
```

<span class="c2">and C’s inbound traffic engineering policy can be represented as:</span>

```python 
match(dstport = 4321) >>  fwd(C1) + match(dstport=4322) >> fwd(C2)
```

<span class="c2">Both B and C are advertising IP prefixes ```140.0.0.0/24, 150.0.0.0/24``` to A. SDX’s route server decides best BGP path for these prefixes and advertises to A. In this example, routes advertised by B are preferred over C, as B’s router-id is smaller than C’s. We should expect that traffic from participant A for dstport 80 should go to b1, port 4321 to c1 and 4322 to c2\. We can test this setup using iperf.</span>

<span class="c2 c26">Starting the  </span><span class="c0 c26">iperf</span> <span class="c2 c26">servers:</span>
```bash
mininext> b1 iperf -s -B 140.0.0.1 -p 80 &  
mininext> c1 iperf -s -B 140.0.0.1 -p 4321 &  
mininext> c2 iperf -s -B 140.0.0.1 -p 4322 &  
```
<span class="c2 c26">Starting the  </span><span class="c0 c26">iperf</span> <span class="c2 c26">clients:</span>

```bash
mininext> a1 iperf -c 140.0.0.1 -B 100.0.0.1 -p 80 -t 2  
mininext> a1 iperf -c 140.0.0.1 -B 100.0.0.1 -p 4321 -t 2  
mininext> a1 iperf -c 140.0.0.1 -B 100.0.0.1 -p 4322 -t 2  
```

<span class="c2">Successful</span> <span class="c0">iperf</span><span class="c2"> connections should look like this:</span>


    mininext> c2 iperf -s -B 140.0.0.1 -p 4322 &  
    mininext> a1 iperf -c 140.0.0.1 -B 100.0.0.1 -p 4322 -t 2  
    ------------------------------------------------------------  
    Client connecting to 140.0.0.1, TCP port 4322  
    Binding to local address 100.0.0.1  
    TCP window size: 85.3 KByte (default)  
    ------------------------------------------------------------  
    [  3] local 100.0.0.1 port 4322 connected with 140.0.0.1 port 4322  
    [ ID] Interval       Transfer     Bandwidth  
    [  3]  0.0- 2.0 sec  1.53 GBytes  6.59 Gbits/sec  

In case the `iperf` connection is not successful, you should see the message, `connect failed: Connection refused.`

#### Cleaning Up
Make sure that you clean up the ribs and clean the Mininet topology. For convenience, we have provided the ```clean.sh``` script. Run ```sudo sh clean.sh``` script to clean the ribs and the Mininet topology.

## <a name="h.dpp4i4pvtw7k"></a><span class="c48 c2 c26 c11">Assignment</span>

<span class="c2">The setup for the assignment is similar to the previous example.  </span>

<span></span>

![](https://d396qusza40orc.cloudfront.net/sdn/images/Coursera%20SDX.jpg "https://d396qusza40orc.cloudfront.net/sdn/images/Coursera%20SDX.jpg")

<span class="c4">Figure 8\. Topology that you will set up for the assignment. 

 
172.* addresses refer to the IP addresses of the connected router interfaces. /24 IP prefixes are the routes that each router advertises.  </span>

<span class="c2">In the figure, the IP addresses on each interface (</span><span class="c0">172.0.*.*</span><span class="c2">) refer to the interfaces on the local LAN that the routers (and the SDX controller/route server) use to communicate with one another.  The /24 IP prefixes shown by each router in the figure indicate the IP prefixes that each router should be announcing to the neighboring ASes using BGP (i.e., using a BGP</span> <span class="c0">network</span><span class="c2"> statement, as we showed above in the example</span> <span class="c0">bgpd.conf</span><span class="c2">).</span>

<span class="c2">You will need to modify files in the example</span> <span class="c0">```simple```</span><span class="c2"> so that the behavior of the topology and forwarding is as we have have shown in the figure.  </span>


#### <span class="c3 c2 c11">Part 1: Topology and route server configuration</span><span class="c3 c2">  
</span><span class="c2">First, you will configure the topology as shown in the figure. You will need two files:</span>

*   <span class="c0">```sdx_mininext.py```</span><span class="c2">: You will use this file to configure the SDX topology, as we have shown above. Similar to the walkthrough example, make sure that each router has a loopback address for each advertised route. For example, if the node</span> <span class="c0">c1</span><span class="c2"> advertises</span> <span class="c0">140.0.0.0/24</span> <span class="c2">then add the loopback interface</span> <span class="c0">140.0.0.1</span><span class="c2"> for</span> <span class="c0">c1</span><span class="c2">.  </span>
*   <span class="c0">```bgpd.conf```</span><span class="c2">: You will use this file to set up the BGP sessions for `each` participant and change the IP prefixes that they advertise. For example if node</span> <span class="c0">c1</span><span class="c2"> advertises</span> <span class="c0">140.0.0.0/24,</span> <span class="c2">then make sure that</span> <span class="c2">network</span><span class="c9 c2"> </span><span class="c0">140.0.0.0/24</span><span class="c9 c2"> </span><span class="c2">is added in</span><span class="c9 c2"> c1’s bgpd.conf</span> <span class="c2">file.</span><span class="c9 c2"> </span>

##### <span class="c3 c2 c11">Testing the topology and route server configuration</span>

<span class="c2">Follow the steps specified in the walkthrough example to run the setup and test your new topology and route setup.</span>

<span class="c2">The routing table for participant A (node a1) should look like this:</span>
```bash
mininext> a1 route -n
Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
140.0.0.0       172.0.1.3       255.255.255.0   UG    0      0        0 a1-eth0
150.0.0.0       172.0.1.6       255.255.255.0   UG    0      0        0 a1-eth0
160.0.0.0       172.0.1.7       255.255.255.0   UG    0      0        0 a1-eth0
170.0.0.0       172.0.1.8       255.255.255.0   UG    0      0        0 a1-eth0
172.0.0.0       0.0.0.0         255.255.0.0     U     0      0        0 a1-eth0
180.0.0.0       172.0.1.5       255.255.255.0   UG    0      0        0 a1-eth0
190.0.0.0       172.0.1.4       255.255.255.0   UG    0      0        0 a1-eth0
```

#### <span class="c3 c2 c11">Part 2: Policy configuration</span><span class="c2 c3">  
</span><span class="c2">In the second part, you will define policies for each participant. These policies should satisfy the following goals:</span>

*   <span class="c2">Participant A should forward HTTP traffic to peer B, HTTPS traffic to C.</span>
*   <span class="c2">Participant C should forward HTTPS traffic to c1, HTTP traffic to c2. 

<span class="c2">You will need to modify</span> <span class="c0">participant_1.py</span><span class="c2"> and</span> <span class="c0">participant_3.py</span><span class="c2"> from the walkthrough to implement these policies.</span>

##### <span class="c3 c2 c11">Testing policy configuration</span>

<span class="c2">SDX’s route server will select B’s routes for the prefixes</span> <span class="c0">140.0.0.0/24</span><span class="c0">,</span> <span class="c0">150.0.0.0/24</span><span class="c0">,</span> <span class="c0">160.0.0.0/24</span><span class="c0"> &</span> <span class="c0">170.0.0.0/24</span><span class="c0">;</span> <span class="c2">C’s routes for the prefixes</span><span class="c0"> </span><span class="c0">180.0.0.0/24</span><span class="c0"> &</span> <span class="c0">190.0.0.0/24</span><span class="c0">; and</span> <span class="c2">A’s routes for the prefixes</span><span class="c0"> </span><span class="c0">100.0.0.0/24</span><span class="c0"> &</span> <span class="c0">110.0.0.0/24</span><span class="c0">.

</span> <span class="c2">Even though A’s policy is to forward port 80 traffic to B, the SDX controller will forward port 80 traffic with dstip = 180.0.0.1 to C (because participant B didn't advertise the route for the prefix 180.0.0.0/24). Since C’s inbound TE policy forwards the HTTP traffic to c2, thus this traffic should be received at c2\. Similarly HTTPS traffic from A should be received at c1\. 

<span class="c2">Similar to the walkthrough example, you can use iperf to test the policy configuration. You can verify that port 80 traffic for routes advertised by B will be received by node b1.</span>
```bash
mininext> b1 iperf -s -B 140.0.0.1 -p 80 &
mininext> a1 iperf -c 140.0.0.1 -B 100.0.0.1 -p 80 -t 2
------------------------------------------------------------
Client connecting to 140.0.0.1, TCP port 80
Binding to local address 100.0.0.1
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  3] local 100.0.0.1 port 80 connected with 140.0.0.1 port 80
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 3.0 sec   384 KBytes  1.06 Mbits/sec
```

<span class="c2">You can also verify that port 80 traffic from A for routes advertised only by C will be forwarded to node c1\.</span>
```bash
mininext> c2 iperf -s -B 180.0.0.1 -p 80 &
mininext> a1 iperf -c 180.0.0.1 -B 100.0.0.2 -p 80 -t 2
------------------------------------------------------------
Client connecting to 180.0.0.1, TCP port 80
Binding to local address 100.0.0.2
TCP window size: 85.3 KByte (default)
------------------------------------------------------------
[  3] local 100.0.0.2 port 80 connected with 180.0.0.1 port 80
[ ID] Interval       Transfer     Bandwidth
[  3]  0.0- 3.0 sec   384 KBytes  1.04 Mbits/sec
```

### <a name="h.43cd3gtc620p"></a><span class="c48 c2 c26">Submitting the Assignment</span>

**NOTE** The submit.py script will start all applications required by the sdx assignment (MiniNExT, set OF 1.3, start Ryu, start route server and ExaBGP). To make sure the enviroment is clean, close all other windows but one and clean the enviroment with the provided script and only then submit.

<span class="c2">Copy the</span> <span class="c0">submit.py</span><span class="c2"> file that we have provided to the</span> <span class="c0">~/sdx-ryu/</span><span class="c0">examples/simple/mininet/</span><span class="c2"> directory.</span> Now run the ```submit.py``` script from the ```~/sdx-ryu/examples/simple/mininet/``` directory.

```bash
$ sudo python submit.py  
```

<span class="c2">Your mininet VM should have Internet access by default, but still verify that it has internet connectivity (i.e., eth0 set up as NAT). Otherwise, ```submit.py``` will not be able to post your code and output to our coursera servers.</span>

<span class="c2">The submission script will ask for your login and password. This password is not the general account password, but an assignment-specific password that is uniquely generated for each student. You can get this from the assignments listing page.</span>

<span class="c2">Once finished, it will prompt the results on the terminal (either passed or failed).</span>


<span class="c2">Note, if during the execution ```submit.py``` scripts crash for some reason or you terminate it using CTRL+C, make sure to run the ```clean.sh``` script:</span>

```bash
$ sudo sh clean.sh
```

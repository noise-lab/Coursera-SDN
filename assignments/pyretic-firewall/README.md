<span class="c8">In this exercise, you will be working with</span> <span class="c8 c6">Pyretic</span><span class="c8">, a new programmer-friendly domain-specific language embedded in Python. It provides a runtime system that enables programmers to specify network policies at a high level of abstraction, compose them together in a variety of ways, and execute them on abstract topologies. As in week 4, this week you will be taken through the steps of writing network applications i.e., hub and layer 2 MAC learning on Pyretic and testing them using Mininet. The purpose of this exercise is to show you that there is no single way of writing such applications. New runtime systems are being developed, which provide richer abstractions and tools to express your network applications --- Pyretic is one such example.</span>

<span class="c8"></span>

<span class="c8">After the walkthrough, You will be asked to re-implement and submit the Layer 2 firewall you encoded in POX last week using the higher-level constructs offered by Pyretic. More details on creating and submitting the code will be provided later on in the instructions. So, as always, make sure that you follow each step carefully.</span>

<span class="c8"></span>

## Overview


<span class="c31 c6"></span>

<span class="c8">The network you'll use in this exercise includes 3 hosts and a switch, this time with the Pyretic runtime to express your network applications.</span>

<span class="c8"></span>

<span></span>

![](https://lh6.googleusercontent.com/JgNextBvzib8PTXVvnA-4QF-D5J3GdqxIoVKvuRwo0gPhgqRppQ6DH32SdWbInmQBwWBQHVd4OzyUR-HR75JDXtqMMg6MZtmZIhtgZj1M6-7ij6CSKxRZaEN "Image: https://lh6.googleusercontent.com/JgNextBvzib8PTXVvnA-4QF-D5J3GdqxIoVKvuRwo0gPhgqRppQ6DH32SdWbInmQBwWBQHVd4OzyUR-HR75JDXtqMMg6MZtmZIhtgZj1M6-7ij6CSKxRZaEN")

<span>Figure 1: Topology for the Network under Test</span>

<span class="c8">As mentioned above, Pyretic is a new language and system  that enables modular programming by:</span>

*   <span class="c8">Defining composition operators and a library of policies for forwarding and querying traffic. Pyretic's parallel composition operator allows multiple policies to operate on the same set of packets, while it's sequential composition operator allows one policy to process packets after another.</span>

<span></span>

*   <span class="c8">Pyretic enables each policy to operate on an abstract topology that implicitly constrains what the module can see and do.</span>

<span></span>

*   <span class="c8">Pyretic provides a rich abstract packet model that allows programmers to extend packets with virtual fields that may be used to associate packets with high-level meta-data.</span>

<span class="c8"></span>

<span class="c8">For more details on Pyretic, see</span> <span class="c39">[http://www.frenetic-lang.org/pyretic/](http://www.google.com/url?q=http%3A%2F%2Fwww.frenetic-lang.org%2Fpyretic%2F&sa=D&sntz=1&usg=AFQjCNHvJToVEFlXfqRNabKYj4uxNRFpXw)</span><span class="c8">.                         </span>

<span class="c8">                                </span>

<span class="c8">We will be using the Pyretic runtime system, so make sure that the default or POX controller is not running in the background. Also, confirm that the port ```6633``` used to communicate with OpenFlow switches by the runtime is not bounded:</span>

<span class="c8"></span>

```bash 
$ sudo fuser -k 6633/tcp
```

<span class="c9"></span>

<span class="c8">This will kill any existing TCP connection, using this port.</span>

<span class="c8"></span>

<span class="c8">You should also run</span> <span class="c9">sudo mn -c</span><span class="c8"> and restart Mininet to make sure that everything is clean and using the faster kernel switch: From you Mininet console:</span>

<span class="c8"></span>

```bash
mininet> exit
$ sudo mn -c
$ sudo mn --topo single,3 --mac --switch ovsk --controller remote
```
<span class="c9"></span>

<span class="c8">The Pyretic runtime comes pre-installed with the provided Vagrant setup.</span>

### Verify Hub behavior with tcpdump</span>


<span class="c8">Now, run the basic hub example:</span>

<span class="c8"></span>

```bash 
$ pyretic.py -v high pyretic.modules.hub
```

<span class="c9"></span>

<span class="c8">This tells Pyretic to enable verbose logging and to start the hub component. You</span><span>’ll find the file</span> <span class="c8"> </span><span class="c30">```pyretic.py```</span> <span>in</span> <span class="c30">~/pyretic</span> <span>directory.</span>

<span class="c28"></span>

<span class="c47 c28 c49">TIP: start pyretic first for quicker hookup w/ mininet</span>

<span class="c8">The switches may take a little bit of time to connect. When an OpenFlow switch loses its connection to a controller, it will generally increase the period between which it attempts to contact the controller, up to a maximum of 15 seconds. Since the OpenFlow switch has not connected yet, this delay may be anything between 0 and 15 seconds. If this is too long to wait, the switch can be configured to wait no more than N seconds using the --max-backoff parameter. Alternately, you exit Mininet to remove the switch(es), start the controller, and then start Mininet to immediately connect.</span>

<span class="c8"></span>

<span class="c8">Wait until the application indicates that the OpenFlow switch has connected. When the switch connects, Pyretic will print something like this:</span>
```
OpenFlow switch 1 connected
2013-07-21 13:19:11.276764  | clear_all
2013-07-21 13:19:11.278561  | clear_all
2013-07-21 13:19:11.280613  | clear_all
2013-07-21 13:19:11.281942  | clear_all
```

<a name="h.30j0zll"></a><span class="c44">Now verify that hosts can ping each other, and that all hosts see the exact same traffic - the behavior of a hub. To do this, we'll create xterms for each host and view the traffic in each. In the Mininet console, start up three xterms:</span>

```
mininet> xterm h1 h2 h3
```

<span class="c8">Arrange each xterm so that they're all on the screen at once. This may require reducing the height to fit a cramped laptop screen.</span>

<span class="c8"></span>

<span class="c8">In the xterms for h2 and h3, run</span> <span class="c9">tcpdump</span><span class="c8">, a utility to print the packets seen by a host:</span>

```bash
# tcpdump -XX -n -i h2-eth0
```


<span class="c8">and respectively:</span>

```bash
# tcpdump -XX -n -i h3-eth0
```

<span class="c8">In the xterm for h1, send a ping:</span>

```bash
# ping -c1 10.0.0.2
```

<span class="c8">The ping packets are now going up to the controller, which then floods them out all interfaces except the sending one. You should see identical ARP and ICMP packets corresponding to the ping in both xterms running tcpdump. This is how a hub works; it sends all packets to every port on the network.</span>

<span class="c8"></span>

<span class="c8">Now, see what happens when a non-existent host doesn't reply. From h1 xterm:</span>

```bash
# ping -c1 10.0.0.5
```

<span class="c8">You should see three unanswered ARP requests in the tcpdump xterms. If your code is off later, three unanswered ARP requests is a signal that you might be accidentally dropping packets.</span>

<span class="c8"></span>

<span class="c8">You can close the xterms now.</span>

<span class="c8"></span>

<span class="c8">Now, lets look at the hub code (You can see the reduction in the amount of code needed to implement hub in Pyretic as compared to POX):</span>
```python
from pyretic.lib.corelib import *
from pyretic.lib.std import *
   """Implement hub-like behavior --- send all packets to all ports on a network
    minimum spanning tree, except for the input port"""
hub = flood()
def main():
    return hub
```

Table 1. Hub Application

<span></span>

<span>Interestingly, Pyretic’s “flood” operator computes a minimum spanning tree under the hood, so you don’t have to worry about loops in your topology when you call Pyretic’s flood operator.</span>

<span></span>

### <a name="h.3znysh7"></a><span class="c17 c6">Verify Switch behavior with tcpdump</span>

<span class="c17 c6"></span>

<span class="c8">This time, let’s verify that hosts can ping each other when the controller is behaving like a layer 2 learning switch. Kill the Pyretic runtime by pressing Ctrl-C in the window running the program.</span>

<span class="c8"></span>

<span class="c8">Now, run the switch example:</span>

```bash
$ pyretic.py -v high pyretic.modules.mac_learner
```

<a name="h.2et92p0"></a><span class="c44">Like before, we'll create xterms for each host and view the traffic in each. In the Mininet console, start up three xterms:</span>

```bash
mininet> xterm h1 h2 h3
```

<span class="c9"></span>

<span class="c8">Arrange each xterm so that they're all on the screen at once. This may require reducing the height of to fit a cramped laptop screen.</span>

<span class="c8"></span>

<span class="c8">In the xterms for h2 and h3, run</span> <span class="c9">tcpdump</span><span class="c8">, a utility to print the packets seen by a host:</span>

<span class="c8"></span>

```bash
# tcpdump -XX -n -i h2-eth0
```

<span class="c9"></span>

<span class="c8">and respectively:</span>

```bash
# tcpdump -XX -n -i h3-eth0
```

<span class="c9"></span>

<span class="c8">In the xterm for h1, send a ping:</span>

```bash
# ping -c1 10.0.0.2
```

<span class="c9"></span>

<span class="c8">Here, the switch examines each packet and learn the source-port mapping. Thereafter, the source MAC address will be associated with the port. If the destination of the packet is already associated with some port, the packet will be sent to the given port, else it will be flooded on all ports of the switch.</span>

<span class="c8"></span>

<span class="c8">You can close the xterms now.</span>

<span class="c8"></span>

<span class="c8">Let’s have a look at the</span> <span>mac_learner</span><span class="c8"> code (it’s pretty self explanatory, and we went throug</span><span>h it in lecture, as well</span><span class="c8">):</span>

```python
from pyretic.lib.corelib import *
from pyretic.lib.std import *
from pyretic.lib.query import *
class mac_learner(DynamicPolicy):
    """Standard MAC-learning logic"""
    def __init__(self):
        super(mac_learner,self).__init__()
        self.flood = flood()           # REUSE A SINGLE FLOOD INSTANCE
        self.set_initial_state()
    def set_initial_state(self):
        self.query = packets(1,['srcmac','switch'])
        self.query.register_callback(self.learn_new_MAC)
        self.forward = self.flood  # REUSE A SINGLE FLOOD INSTANCE
        self.update_policy()
    def set_network(self,network):
        self.set_initial_state()
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
       
def main():
    return mac_learner()
```

<span class="c8">Table 2\. Switch Application</span>

<span class="c8"></span>

### <a name="h.3dy6vkm"></a><span>Useful Pyretic policies</span>

<span></span>

<span class="c9">```match(f=v)```</span><span class="c8">: filters only those packets whose header field f's value matches v</span>

<span class="c9">```~A```</span><span class="c8">: negates a match</span>

<span class="c9">```A & B```</span><span class="c8">:  logical intersection of matches A and B</span>

<span class="c9">```A | B```</span><span class="c8">:   logical union of matches A and B</span>

<span class="c9">```fwd(a)```</span><span class="c8">: forward packet out port a</span>

<span class="c9">```flood()```</span><span class="c8">: send all packets to all ports on a network minimum spanning tree, except for the input port</span>

<span class="c9">```A >> B```</span><span class="c8">:  A's output becomes B's input</span>

<span class="c9">```A + B```</span><span class="c8">:   A's output and B's output are combined  </span>

<span class="c9">```if_(M,A,B)```</span><span class="c8">: if packet filtered by M, then use A, otherwise use B  </span>

<span class="c8"></span>

<span class="c8">These policies are explained in greater detail in</span> <span class="c39">[Module 6.4](https://class.coursera.org/sdn1-001/lecture/59)</span><span class="c8">.</span>

<span class="c8"></span>

## <a name="h.1t3h5sf"></a><span class="c31 c6">Assignment</span>

### <a name="h.4d34og8"></a><span class="c17 c6">Background</span>

<span class="c6 c17"></span>

<span class="c8">A Firewall is a network security system that is used to control the flow of ingress and egress traffic usually between a more secure local-area network (LAN) and a less secure wide-area network (WAN). The system analyses data packets for parameters like L2/L3 headers (i.e., MAC and IP address) or performs deep packet inspection (DPI) for higher layer parameters (like application type and services etc) to filter network traffic. A firewall acts as a barricade between a trusted, secure internal network and another network (e.g. the Internet) which is supposed to be not very secure or trusted.</span>

<span class="c8"></span>

<span class="c8">In this assignment, your task is to implement a layer 2 firewall that runs alongside the MAC learning module on the Pyretic runtime. The firewall application is provided with a list of MAC address pairs i.e., access control list (ACLs). When a connection establishes between the controller and the switch, the application installs static flow rule entries in the OpenFlow table to disable all communication between each MAC pair.</span>

<span class="c8"></span>

### <a name="h.2s8eyo1"></a><span class="c17 c6">Network Topology</span>

<span class="c17 c6"></span>

<span class="c8">Your firewall should be agnostic of the underlying topology. It should take MAC pair list as input and install it on the switches in the network. To make things simple, we will implement a less intelligent approach and will install rules on</span> <span class="c8 c6">all</span><span class="c8"> the switches in the network.  </span>

<span class="c8"></span>

### <a name="h.17dp8vu"></a><span class="c17 c6">Understanding the Code</span>

<span class="c17 c6"></span>

To start this assignment update the course's Github repo (by default, Coursera-SDN) on your host machine using git pull. Turn on your guest VM (if it is turned off) using vagrant up. Now ssh into the guest VM using vagrant ssh. Go to the directory with the updated code base in your guest VM.
```bash
~$ cd /vagrant/assignments/pyretic-firewall
```

The directory consists of three files:


<span class="c9">```pyretic_firewall.py```</span><span class="c8">: a sekleton class which you will update with the logic for installing firewall rules.</span>

<span class="c9">```firewall-policies.csv```</span><span class="c8">:  a list of MAC pairs (i.e., policies) read as input by the firewall application.</span>

<span class="c9">```submit.py```</span><span class="c8">: used to submit your code and output to the</span> <span>C</span><span class="c8">oursera servers for grading.</span>

<span class="c8"></span>

<span class="c8">You don’t have to do any modifications in</span> <span class="c9">firewall-policies.csv</span><span class="c8"> and</span> <span class="c9">submit.py</span><span class="c8">.</span>

<span class="c8"></span>

<span class="c8">The</span><span class="c9"> pyretic_firewall.py</span><span class="c8"> is populated with a skeleton code. It consists of a</span> <span class="c9">main</span><span class="c8"> function and a global variable (</span><span class="c9">policy_file</span><span class="c8">) that holds the path of the</span> <span class="c9">firewall-policies.csv</span><span class="c8"> file. Whenever a connection is established between the Pyretic controller and the OpenFlow switch the</span> <span class="c9">main</span> <span class="c8">functions gets executed.</span>

<span class="c8"></span>

<span class="c8">Your task is to read the policy file and update the</span> <span class="c9">```main```</span> <span class="c8">function. The function should install policies in the OpenFlow switch that drop packets whenever a matching src/dst MAC address (for any of the listed MAC pairs) enters the switch</span>

<span class="c8"></span>

### <a name="h.3rdcrjn"></a><span class="c17 c6">Testing your Code</span>

<span class="c17 c6"></span>

<span class="c8">Once you have your code, copy the</span> <span class="c9">pyretic_firewall.py</span><span class="c8"> in the</span> <span class="c9">~/pyretic/pyretic/examples</span> <span class="c8">directory on your VM. Also in the same directory create the following file:</span>

<span class="c8"></span>

```bash
$ cd ~/pyretic/pyretic/examples
$ touch firewall-policies.csv
```

<span class="c9"></span>

<span class="c8">and copy the following lines in it:</span>

```
id,mac_0,mac_1
1,00:00:00:00:00:01,00:00:00:00:00:02
```

<span class="c8">This will cause the firewall application to install a flow rule entry to disable all communication between host (h1) and host (h2).</span>

<span class="c8"></span>

<span class="c8">Run Pyretic runtime:</span>

<span class="c8"></span>

```bash
$ cd ~
$ pyretic.py pyretic.examples.pyretic_firewall
```

<span class="c9"></span>

<span class="c8">Now run mininet:</span>

<span class="c8"></span>

```bash
$ sudo mn --topo single,3 --controller remote --mac
```

<span class="c9"></span>

<span class="c8">In mininet try to ping host (h2) from host (h1):</span>

<span class="c8"></span>

```bash
mininet> h1 ping -c1 h2
```

<span class="c9"></span>

<span class="c8">What do you see? If everything has be done and setup correctly then host (h1) should not be able to ping host (h2).</span>

<span class="c8"></span>

<span class="c8">Now try pinging host (h3) from host (h1):</span>

<span class="c8"></span>

```bash
mininet> h1 ping -c1 h3
```

<span class="c9"></span>

<span class="c8">What do you see? Host (h1) is able to ping host (h3) as there is no flow rule entry installed in the network to disable the communication between them.</span>

<span class="c8"></span>

### <a name="h.26in1rg"></a><span class="c17 c6">Submitting your Code</span>

<span>T</span><span class="c8">he</span> <span class="c9">pyretic_firewall.py</span><span class="c8"> </span><span class="c29">and the provided</span> <span class="c43 c30 c47">firewall-policy.csv</span><span class="c43"> </span><span>should go</span><span class="c43"> </span><span class="c8">into the</span> <span class="c9">```~/pyretic/pyretic/examples```</span> <span class="c8">directory on your VM.</span>

<span class="c8"></span>

<span class="c8">Also copy the</span> <span class="c9">```submit.py```</span><span class="c8"> script in the HOME (~/) directory.</span>

<span class="c8"></span>

<span class="c8">Run pyretic:</span>

<span class="c8"></span>

```bash
$ pyretic.py pyretic.examples.pyretic_firewall
```



<span></span>

<span class="c8">To submit your code, run the submit.py script:</span>

<span class="c8"></span>

```bash
$ sudo python submit.py
```

<span class="c9"></span>

<span class="c8">Your mininet VM should have internet access by default, but still verify that it has internet connectivity (i.e., eth0 set up as NAT). Otherwise</span> <span class="c9">submit.py</span><span class="c8"> will not be able to post your code and output to our coursera servers.</span>

<span class="c8"></span>

<span class="c8">The submission script will ask for your login and password. This password is not the general account password, but an assignment-specific password that is uniquely generated for each student. You can get this from the assignments listing page.</span>

<span class="c8"></span>

<span class="c8">Once finished, it will prompt the results on the terminal (either passed or failed).</span>

<span class="c8"></span>

<span class="c8">Note, if during the execution</span> <span class="c9">submit.py or m6-output.py</span> <span class="c8">scripts crash for some reason or you terminate it using CTRL+C, make sure to clean mininet environment using:</span>

<span class="c8"></span>

```bash
$ sudo mn -c
```

<span class="c9"></span>

<span class="c8">Also, if it still complains about the controller running. Execute the following command to kill it:</span>

<span class="c8"></span>

```bash
$ sudo fuser -k 6633/tcp
```

<span class="c9"></span>

* * *

<span class="c9"></span>

<span class="c9"></span>

<span class="c8">* Part of these instructions are adapted from</span> <span class="c39">http://www.frenetic-lang.org/pyretic/</span><span class="c8">.</span>

<span class="c8"></span>

<span class="c8"></span>

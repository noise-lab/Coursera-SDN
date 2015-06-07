<span>In this exercise, you will learn about an open-source OpenFlow controller “POX”. You will learn how to write network applications, i.e., Hub and Layer 2 MAC Learning etc., on POX and run them on a virtual network based on Mininet.</span>

<span></span>

<span>After the exercise, you will be asked to create and submit a network application that implements Layer 2 Firewall that disables inbound and outbound traffic between two systems based on their MAC address. More details on creating and submitting the code will be provided later on in the instructions. So, make sure that you follow each step carefully.</span>

<span></span>

<span class="c24">(Note: you can skip this section and start directly with the assignment at the end, if you feel confident and are already familiar with POX and its basic functions)</span>

<span class="c24"></span>

# <a name="h.ll5q1qbqv1b2"></a><span class="c19">Overview</span>

<span></span>

<span>The network you'll use in this exercise includes 3 hosts and a switch with an OpenFlow controller (POX):</span>

<span></span>

![](https://lh6.googleusercontent.com/JgNextBvzib8PTXVvnA-4QF-D5J3GdqxIoVKvuRwo0gPhgqRppQ6DH32SdWbInmQBwWBQHVd4OzyUR-HR75JDXtqMMg6MZtmZIhtgZj1M6-7ij6CSKxRZaEN "Image: https://lh6.googleusercontent.com/JgNextBvzib8PTXVvnA-4QF-D5J3GdqxIoVKvuRwo0gPhgqRppQ6DH32SdWbInmQBwWBQHVd4OzyUR-HR75JDXtqMMg6MZtmZIhtgZj1M6-7ij6CSKxRZaEN")

<span>Figure 1: Topology for the Network under Test</span>

<span class="c19 c33"></span>

<span>POX is a Python based SDN controller platform geared towards research and education. For more details on POX, see</span> <span class="c19 c27">[About POX](http://www.noxrepo.org/pox/about-pox/)</span><span> or</span> <span class="c19 c27">[POX Documentation](https://openflow.stanford.edu/display/ONL/POX+Wiki)</span><span> on</span> <span class="c19 c27">[NOXRepo.org](http://www.noxrepo.org/)</span><span>.</span>

<span></span>

<span>We’re not going to be using the reference controller anymore, which is the default controller that Mininet uses during it simulation. Make sure that it’s not running in the background:</span>

```bash
$ ps -A | grep controller
```

<span>If so, you should kill it either press Ctrl-C in the window running the controller program, or from the other SSH window:</span>

<span></span>
```bash
$ sudo killall controller
```
<span class="c1 c26"></span>

<span>You should also run</span> <span class="c1">sudo mn -c</span><span> and restart Mininet to make sure that everything is clean and using the faster kernel switch: From you Mininet console:</span>

<span></span>

```bash
mininet> exit  
$ sudo mn -c  
$ sudo mn --topo single,3 --mac --switch ovsk --controller remote
```

<span class="c1"></span>

<span>The POX controller comes pre-installed with the provided VM image.</span>

<span></span>

<span>Now, run the basic hub example:</span>

<span class="c1"></span>

```bash
$ pox.py log.level --DEBUG forwarding.hub
```

<span class="c1"></span>

<span>This tells POX to enable verbose logging and to start the hub component.</span>

<span></span>

<span>The switches may take a little bit of time to connect. When an OpenFlow switch loses its connection to a controller, it will generally increase the period between which it attempts to contact the controller, up to a maximum of 15 seconds. Since the OpenFlow switch has not connected yet, this delay may be anything between 0 and 15 seconds. If this is too long to wait, the switch can be configured to wait no more than N seconds using the --max-backoff parameter. Alternately, you exit Mininet to remove the switch(es), start the controller, and then start Mininet to immediately connect.</span>

<span></span>

<span>Wait until the application indicates that the OpenFlow switch has connected. When the switch connects, POX will print something like this:</span>

<span></span>

```
INFO:openflow.of_01:[Con 1/1] Connected to 00-00-00-00-00-01  
DEBUG:samples.of_tutorial:Controlling [Con 1/1]
```

<span></span>

## <a name="h.jk1wcrjvrj9s"></a><span class="c19">Verify Hub behavior with tcpdump</span>

<span>Now verify that hosts can ping each other, and that all hosts see the exact same traffic - the behavior of a hub. To do this, we'll create xterms for each host and view the traffic in each. In the Mininet console, start up three xterms:</span>

<span class="c1"></span>

```bash
mininet> xterm h1 h2 h3
```

<span class="c1"></span>

<span>Arrange each xterm so that they're all on the screen at once. This may require reducing the height to fit a cramped laptop screen.</span>

<span></span>

<span>In the xterms for h2 and h3, run</span> ```tcpdump```, a utility to print the packets seen by a host:</span>

```bash
# tcpdump -XX -n -i h2-eth0
```
<span></span>

<span>and respectively:</span>

<span></span>

```bash
# tcpdump -XX -n -i h3-eth0
```

<span></span>

<span>In the xterm for h1, send a ping:</span>

<span></span>

```bash
# ping -c 1 10.0.0.2
```

<span class="c1"></span>

<span>The ping packets are now going up to the controller, which then floods them out all interfaces except the sending one. You should see identical ARP and ICMP packets corresponding to the ping in both xterms running tcpdump. This is how a hub works; it sends all packets to every port on the network.</span>

<span></span>

<span>Now, see what happens when a non-existent host doesn't reply. From h1 xterm:</span>

<span></span>

```bash
# ping -c 1 10.0.0.5
```

<span class="c1"></span>

<span>You should see three unanswered ARP requests in the tcpdump xterms. If your code is off later, three unanswered ARP requests is a signal that you might be accidentally dropping packets.</span>

<span></span>

<span>You can close the xterms now.</span>

<span></span>

<span>Now, lets look at the hub code:</span>

<span></span>

```bash
#!/usr/bin/python

from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.util import dpidToStr
log = core.getLogger()
def _handle_ConnectionUp (event):
  msg = of.ofp_flow_mod()
  msg.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD))
  event.connection.send(msg)
  log.info("Hubifying %s", dpidToStr(event.dpid))
def launch ():
  core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
  log.info("Hub running.")
```
<span>Table 1\. Hub Controller</span>

<span></span>

### <a name="h.sw3sfi66zwby"></a><span>Useful POX API’s</span>



*  ```connection.send( ... )``` function sends an OpenFlow message to a switch.</span>



<span>When a connection to a switch starts, a ConnectionUp event is fired. The above code invokes a</span><span class="c1"> _handle_ConnectionUp ()</span> <span>function that implements the hub logic.</span>


*  ```ofp_action_output``` class



<span>This is an action for use with</span> <span class="c1">ofp_packet_out</span><span> and</span> <span class="c1">ofp_flow_mod</span><span>. It specifies a switch port that you wish to send the packet out of. It can also take various "special" port numbers. An example of this, as shown in Table 1, would be</span> <span class="c1">OFPP_FLOOD</span><span> which sends the packet out all ports except the one the packet originally arrived on.</span>



<span>Example. Create an output action that would send packets to all ports:</span>



```bash
out_action = of.ofp_action_output(port = of.OFPP_FLOOD)
```


* ```ofp_match``` class (not used in the code above but might be useful in the assignment)</span>



<span>Objects of this class describe packet header fields and an input port to match on. All fields are optional -- items that are not specified are "wildcards" and will match on anything.</span>



<span>Some notable fields of ofp_match objects are:</span>

1.  ```dl_src```- The data link layer (MAC) source address</span>
2.  ```dl_dst```- The data link layer (MAC) destination address</span>
3.  ```in_port```- The packet input switch port</span>



<span>Example. Create a match that matches packets arriving on port 3:</span>

```
match = of.ofp_match()  
match.in_port = 3
```

*  ```ofp_packet_out``` <span>OpenFlow message</span> <span class="c34">(not used in the code above but might be useful in the assignment)</span>

<span></span>

<span>The</span> <span class="c1">```ofp_packet_out```</span><span> message instructs a switch to send a packet. The packet might be one constructed at the controller, or it might be one that the switch received, buffered, and forwarded to the controller (and is now referenced by a</span> <span class="c1">buffer_id</span><span>).</span>

<span></span>

<span>Notable fields are:</span>

1.  <span class="c1">```buffer_id```</span><span> - The buffer_id of a buffer you wish to send. Do not set if you are sending a constructed packet.</span>
2.  <span class="c1">```data```</span><span> - Raw bytes you wish the switch to send. Do not set if you are sending a buffered packet.</span>
3.  <span class="c1">```actions```</span><span> - A list of actions to apply (for this tutorial, this is just a single</span> <span class="c1">```ofp_action_output```</span><span> action).</span>
4.  <span class="c1">```in_port```</span><span> - The port number this packet initially arrived on if you are sending by</span> <span class="c1">buffer_id</span><span>, otherwise</span> <span class="c1">```OFPP_NONE```</span><span>.</span>

<span></span>

<span>Example. ```send_packet()``` method:</span>

```bash
def send_packet (self, buffer_id, raw_data, out_port, in_port):
  """
   Sends a packet out of the specified switch port.
   If buffer_id is a valid buffer on the switch, use that.  Otherwise,
   send the raw data in raw_data.
   The "in_port" is the port number that packet arrived on.  Use
   OFPP_NONE if you're generating this packet.
   """
  msg = of.ofp_packet_out()
  msg.in_port = in_port
  if buffer_id != -1 and buffer_id is not None:
    # We got a buffer ID from the switch; use that
    msg.buffer_id = buffer_id
  else:
    # No buffer ID from switch -- we got the raw data
    if raw_data is None:
      # No raw_data specified -- nothing to send!
      return
    msg.data = raw_data
  
  action = of.ofp_action_output(port = out_port)
  msg.actions.append(action)
  
  # Send message to switch
  self.connection.send(msg)
```



<span>Table 2: Send Packet</span>

<span></span>

1.  <span class="c1 c19">```ofp_flow_mod```</span><span class="c1"> </span><span>OpenFlow message</span>

<span class="c8"></span>

<span>This instructs a switch to install a flow table entry. Flow table entries match some fields of incoming packets, and executes some list of actions on matching packets. The actions are the same as for</span> <span class="c1">```ofp_packet_out```</span><span>, mentioned above (and, again, for the tutorial all you need is the simple</span> <span class="c1">```ofp_action_output```</span><span> action). The match is described by an</span> <span class="c1">```ofp_match```</span><span> object.</span>

<span></span>

<span>Notable fields are:</span>

1.  <span class="c1">idle_timeout</span><span> - Number of idle seconds before the flow entry is removed. Defaults to no idle timeout.</span>
2.  <span class="c1">hard_timeout</span><span> - Number of seconds before the flow entry is removed. Defaults to no timeout.</span>
3.  <span class="c1">actions</span><span> - A list of actions to perform on matching packets (e.g.,</span> <span class="c1">ofp_action_output</span><span>)</span>
4.  <span class="c1">priority</span><span> - When using non-exact (wildcarded) matches, this specifies the priority for overlapping matches. Higher values are higher priority. Not important for exact or non-overlapping entries.</span>
5.  <span class="c1">buffer_id</span><span> - The</span> <span class="c1">buffer_id</span><span> of a buffer to apply the actions to immediately. Leave unspecified for none.</span>
6.  <span class="c1">in_port</span><span> - If using a buffer_id, this is the associated input port.</span>
7.  <span class="c1">match</span><span> - An</span> <span class="c1">ofp_match</span><span> object. By default, this matches everything, so you should probably set some of its fields!</span>

<span></span>

<span>Example. Create a flow_mod that sends packets from port 3 out of port 4.</span>

<span></span>

```
fm = of.ofp_flow_mod()  
fm.match.in_port = 3  
fm.actions.append(of.ofp_action_output(port = 4))
```

## <a name="h.j5ane6ow8m7d"></a><span class="c19">Verify Switch behavior with tcpdump</span>

<span></span>

<span>This time, let’s verify that hosts can ping each other when the controller is behaving like a Layer 2 learning switch. Kill the POX controller by pressing Ctrl-C in the window running the controller program and run the l2_learning example:</span>

<span></span>

```bash
$ pox.py log.level --DEBUG forwarding.l2_learning</span>
```

<span>Like before, we'll create xterms for each host and view the traffic in each. In the Mininet console, start up three xterms:</span>

<span class="c1"></span>

```bash
mininet> xterm h1 h2 h3
```

<span class="c1"></span>

<span>Arrange each xterm so that they're all on the screen at once. This may require reducing the height of to fit a cramped laptop screen.</span>

<span></span>

<span>In the xterms for h2 and h3, run</span> <span class="c1">tcpdump</span><span>, a utility to print the packets seen by a host:</span>

```bash
# tcpdump -XX -n -i h2-eth0
```

<span></span>

<span>and respectively:</span>

<span></span>

```bash
# tcpdump -XX -n -i h3-eth0
```

<span></span>

<span>In the xterm for h1, send a ping:</span>

<span></span>

```bash
# ping -c 1 10.0.0.2
```

<span class="c1"></span>

<span>Here, the switch examines each packet and learn the source-port mapping. Thereafter, the source MAC address will be associated with the port. If the destination of the packet is already associated with some port, the packet will be sent to the given port, else it will be flooded on all ports of the switch.</span>

<span></span>

<span>You can close the xterms now.</span>

<span></span>

<span>The code for l2_learning application is provided under ~/pox/pox/forwarding and is explained with greater detail in the</span> <span class="c19 c27">[Module 3.3 lecture on SDN Controller](https://XX)</span><span>.</span>

<span></span>

# <a name="h.rppynhu05rs"></a><span class="c19">Assignment</span>

## <a name="h.6flb20h4s8c2"></a><span class="c19">Background</span>

<span></span>

<span>A Firewall is a network security system that is used to control the flow of ingress and egress traffic usually between a more secure local-area network (LAN) and a less secure wide-area network (WAN). The system analyses data packets for parameters like L2/L3 headers (i.e., MAC and IP address) or performs deep packet inspection (DPI) for higher layer parameters (like application type and services etc) to filter network traffic. A firewall acts as a barricade between a trusted, secure internal network and another network (e.g. the Internet) which is supposed to be not very secure or trusted.</span>

<span></span>

<span>In this assignment, your task is to implement a layer 2 firewall that runs alongside the MAC learning module on the POX OpenFlow controller. The firewall application is provided with a list of MAC address pairs i.e., access control list (ACLs). When a connection establishes between the controller and the switch, the application installs flow rule entries in the OpenFlow table to disable all communication between each MAC pair.</span>

<span></span>

## <a name="h.s04hr7vigj2l"></a><span class="c21 c19">Network Topology</span>

<span></span>

<span>Your firewall should be agnostic of the underlying topology. It should take MAC pair list as input and install it on the switches in the network. To make things simple, we will implement a less intelligent approach and will install rules on</span> <span class="c21">all</span><span> the switches in the network.  </span>

<span></span>

## <a name="h.5kwqaho00huw"></a><span class="c21 c19">Handling Conflicts</span>

<span></span>

<span>POX allows running multiple applications concurrently i.e., MAC learning can be done in conjunction with firewall, but it doesn’t automatically handles rule conflicts. You have to make sure, yourself, that conflicting rules are not being installed by the two applications e.g., both applications trying to install a rule with same src/dst MAC at the same priority level but with different actions.</span> <span class="c24">The most simplistic way to avoid this contention is to assign priority level to each application.</span>

<span></span>

## <a name="h.j57egno8inn0"></a><span class="c19">Understanding the Code</span>

<span></span>

<span>To start this assignment update the course's Github repo (by default, ```Coursera-SDN```) on your host machine using ```git pull```. Turn on your guest VM (if it is turned off) using ```vagrant up```. Now ssh into the guest VM using ```vagrant ssh```. Go to the directory with the updated code base in your guest VM. 
```bash
cd /vagrant/assignments/simple-controller
```
</span> It consists of three files:</span>

<span></span>

1.  <span class="c1">```firewall.py```</span><span>: a sekleton class which you will update with the logic for installing firewall rules.</span>
2.  <span class="c1">```firewall-policies.csv```</span><span>:  a list of MAC pairs (i.e., policies) read as input by the firewall application.</span>
3.  <span class="c1">```submit.py```</span><span>: used to submit your code and output to the coursera servers for grading.</span>

<span></span>

<span>You don’t have to do any modifications in</span> <span class="c1">```firewall-policies.csv```</span><span> and</span> <span class="c1">```submit.py```</span><span>.</span>

<span></span>

<span>The</span><span class="c1"> firewall.py</span><span> is populated with a skeleton code. It consists of a</span> <span class="c1">firewall</span><span> class that has a</span> <span class="c1">_handle_ConnectionUp</span><span> function. It also has a global variable,</span> <span class="c1">policyFile</span><span>, that holds the path of the</span> <span class="c1">firewall-policies.csv</span><span> file. Whenever a connection is established between the POX controller and the OpenFlow switch the</span> <span class="c1">_handle_ConnectionUp</span> <span>functions gets executed.</span>

<span></span>

<span>Your task is to read the policy file and update the</span> <span class="c1">_handle_ConnectionUp</span> <span>function. The function should install rules in the OpenFlow switch that drop packets whenever a matching src/dst MAC address (for any of the listed MAC pairs) enters the switch.</span> <span class="c24">(Note: make sure that you handle the conflicts carefully. Follow the technique described in the section above)</span>

<span></span>

## <a name="h.110hs3ffm302"></a><span class="c19">Testing</span><span class="c19"> your Code</span>

<span class="c20"></span>

<span>Once you have your code, copy the</span> <span class="c1">firewall.py</span><span> in the</span> <span class="c1">~/pox/pox/misc</span> <span>directory on your VM. Also in the same directory create the following file:</span>

<span></span>

```bash
$ cd ~/pox/pox/misc
$ touch firewall-policies.csv
```

<span></span>

<span>and copy the following lines in it:</span>

<span></span>
```
id,mac_0,mac_1
1,00:00:00:00:00:01,00:00:00:00:00:02
```
<span></span>

<span>This will cause the firewall application to install a flow rule entry to disable all communication between host (h1) and host (h2).</span>

<span></span>

<span>Run POX controller:</span>

<span></span>
```bash
$ cd ~
$ pox.py forwarding.l2_learning misc.firewall &
```

<span class="c1"></span>

<span>This will run the controller with both MAC learning and firewall application.</span>

<span></span>

<span>Now run mininet:</span>

<span class="c1"></span>

```bash
$ sudo mn --topo single,3 --controller remote --mac
```
<span class="c1"></span>

<span>In mininet try to ping host (h2) from host (h1):</span>

<span class="c1"></span>

```bash
mininet> h1 ping -c 1 h2
```

<span class="c1"></span>

<span>What do you see? If everything has be done and setup correctly then host (h1) should not be able to ping host (h2).</span>

<span></span>

<span>Now try pinging host (h3) from host (h1):</span>

<span></span>

```bash
mininet> h1 ping -c 1 h3
```

<span></span>

<span>What do you see? Host (h1) is able to ping host (h3) as there is no flow rule entry installed in the network to disable the communication between them.</span>

<span></span>

## <a name="h.i97hjxhipffo"></a><span class="c19">Submitting your Code</span>

<span></span>

<span>This time copy the</span> <span class="c1">firewall.py</span><span> </span><span class="c24">and the provided</span> <span class="c1 c24">firewall-policy.csv</span><span class="c24"> </span><span>in the</span> <span class="c1">~/pox/pox/misc</span> <span>directory on your VM.</span>

<span></span>

<span>Also copy the</span> <span class="c1">submit.py</span><span> script in the HOME (~/) directory.</span>

<span></span>

<span>To submit your code, run the submit.py script:</span>

<span></span>

```bash 
$ sudo python submit.py
```

<span></span>

<span>Your mininet VM should have internet access by default, but still verify that it has internet connectivity (i.e., eth0 set up as NAT). Otherwise</span> <span class="c1">submit.py</span><span> will not be able to post your code and output to our coursera servers.</span>

<span></span>

<span>The submission script will ask for your login and password. This password is not the general account password, but an assignment-specific password that is uniquely generated for each student. You can get this from the assignments listing page.</span>

<span></span>

<span>Once finished, it will prompt the results on the terminal (either passed or failed).</span>

<span></span>

<span>Note, if during the execution</span> <span class="c1">submit.py</span> <span>script crashes for some reason or you terminate it using CTRL+C, make sure to clean mininet environment using:</span>

<span></span>

```bash
$ sudo mn -c
```

<span class="c1"></span>

<span>Also, if it still complains about the controller running. Execute the following command to kill it:</span>

<span></span>

```bash
$ sudo fuser -k 6633/tcp
```

<span></span>

* * *

<span></span>

<span></span>

<span>* Part of these instructions are adapted from</span> <span class="c19 c27">[mininet.org](http://mininet.org)</span><span> and</span> <span class="c19 c27">[noxrepo.org](http://www.google.com/url?q=http%3A%2F%2Fwww.noxrepo.org&sa=D&sntz=1&usg=AFQjCNHaa6HA7IEblHusbdoYDiE2gawAPA)</span><span>.</span>

<span></span>

<span></span>

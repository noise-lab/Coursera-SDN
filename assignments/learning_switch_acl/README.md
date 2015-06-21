## NetASM Assignment

In this exercise, you will learn how to define new data-plane layouts, add custom state elements like tables, and control how each packet is processed in the data plane. To do so, you will be learning and using **NetASM**, a new domain-specific language for configuring programmable data planes on a variety of targets.

NetASM is analogous to an x86 or MIPS-like instructions set.  However, unlike updating main memory and registers, it defines the layout (i.e., control-flow and states) of the data plane. Control-flow defines how the packet is traversed through the data plane, and state refers to the type of memory element (i.e., tables). These state elements have a well-defined data structure and type declaration in NetASM, which makes it easy to identify bugs early in the compilation process.

The syntax of the NetASM language is defined in the [`netasm/core/syntax.py`](https://github.com/NetASM/NetASM-python/blob/master/netasm/netasm/core/syntax.py) file.

### Overview

For more information about the NetASM language read the following material:

* [NetASM-python Wiki](https://github.com/NetASM/NetASM-python/wiki)
* The Case for an Intermediate Representation for Programmable Data Planes: [`paper`](http://www.cs.princeton.edu/~mshahbaz/papers/sosr15-netasm.pdf) [`slides`](http://www.cs.princeton.edu/~mshahbaz/slides/sosr15-netasm.pptx)

### Learning Switch with ACL

In this exercise, you will be extending the learning switch NetASM program -- provided in the base NetASM repository -- with an access control list.

In order to do this, you have to update the following aspects of the learning switch program:
* Add a new match table for access control
* Add support for reading and parsing ip fields
* Write instructions for doing access control using ip's source and destination addresses

#### 1. Copy the assignment

* Copy the `learning_switch_acl` directory to the `netasm/netasm/examples` folder

``` bash
$ cd ~/netasm/netasm/examples
$ cp -rf /vagrant/assignments/learning_switch_acl/ .
```

#### 2. Update the source files to add support for access control

You only need to modify the `learning_switch_acl_netasm.py` file.

#### 3. Test the assignment

Run Mininet script `learning_switch_acl_mininet.py`.

``` bash
$ cd ~
$ sudopy ~/netasm/netasm/examples/learning_switch_acl/learning_switch_acl_mininet.py
```

> Note: make sure that you run this and the remaining scripts using `sudopy`

The script will halt at some point and you should see the following output.

``` bash
*** Creating network
*** Adding controller
Unable to contact the remote controller at 127.0.0.1:6633
*** Adding hosts:
h1 h2
*** Adding switches:
s1
*** Adding links:
(h1, s1) (h2, s1)
*** Configuring hosts
h1 h2
*** Run this command in a separate terminal then press Enter!
sudopy python /home/vagrant/pox/pox.py --no-openflow netasm.back_ends.soft_switch.datapath --address=127.0.0.1 --port=6633 --dpid=0000000000000001 --policy= --ports=s1-eth1,s1-eth2 --ctl_port=7791
```

It's asking you to run a command in a separate terminal and then press Enter.

In a separate terminal run the following command:

``` bash
$ cd ~
$ sudopy python /home/vagrant/pox/pox.py --no-openflow netasm.back_ends.soft_switch.datapath --address=127.0.0.1 --port=6633 --dpid=0000000000000001 --policy= --ports=s1-eth1,s1-eth2 --ctl_port=7791
```

This will launch the NetASM datapath with the required configurations.

Now, open up another terminal and run the POX (controller) script.

``` bash
$ cd ~
$ sudopy ./pox/pox.py netasm.examples.learning_switch_acl.learning_switch_acl_pox
```

You should see that after a short time, both NetASM datapath and POX controller are connected. Upong successful connection, you should see the following ouput on the POX terminal.

``` bash
POX 0.2.0 (carp) / Copyright 2011-2013 James McCauley, et al.
INFO:.home.vagrant.netasm.netasm.examples.learning_switch_acl.learning_switch_acl_pox:netasm.examples.learning_switch_acl.learning_switch_acl_netasm running.
INFO:core:POX 0.2.0 (carp) is up.
INFO:openflow.of_01:[00-00-00-00-00-01 1] connected
INFO:.home.vagrant.netasm.netasm.examples.learning_switch_acl.learning_switch_acl_pox:netasm.examples.learning_switch_acl.learning_switch_acl_netasm for 00-00-00-00-00-01
```

Now go back to the Mininet terminal, where it's waiting for you to press Enter.

```
Press Enter!
```

This will run `net.pingall`. If the `learning_switch_acl_netasm.py` policy is correct. You should see all pings going through.

``` bash
*** Starting controller
c0
*** Starting 1 switches
s1
*** Ping: testing ping reachability
h1 -> h2
h2 -> h1
*** Results: 0% dropped (2/2 received)
*** Stopping 1 controllers
c0
*** Stopping 2 links
..
*** Stopping 1 switches
s1
*** Stopping 2 hosts
h1 h2
*** Done
```

#### 4. Submit your code

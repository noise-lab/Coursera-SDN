##Coursera SDN Virtual Machine Setup

###Setting up the course VM

####Prerequisite

To get started install these softwares on your host machine:

1. Install ***Vagrant***, it is a wrapper around virtualization softwares like VirtualBox, VMWare etc.: http://www.vagrantup.com/downloads

2. Install ***VirtualBox***, this would be your VM provider: https://www.virtualbox.org/wiki/Downloads

3. Install ***Git***, it is a distributed version control system: https://git-scm.com/downloads

4. Install X Server and SSH capable terminal
    * For Windows install [Xming](http://sourceforge.net/project/downloading.php?group_id=156984&filename=Xming-6-9-0-31-setup.exe) and [Putty](http://the.earth.li/~sgtatham/putty/latest/x86/putty.exe).
    * For MAC OS install [XQuartz](http://xquartz.macosforge.org/trac/wiki) and Terminal.app (builtin)
    * Linux comes pre-installed with X server and Gnome terminal + SSH (buitlin)   

####Basics

* Clone the course repository from Github:
```bash 
$ git clone https://github.com/PrincetonUniversity/Coursera-SDN
```

* Change the directory to Coursera-SDN:
```bash
$ cd Coursera-SDN
```

* Now run the vagrant up command. This will read the Vagrantfile from the current directory and provision the VM accordingly:
```bash
$ vagrant up
```

If you want to tear down your vagrant session, you have multiple options to do so, each has its pros and cons. These options are as follows: 
* **vagrant suspend**: With this option you will be able to save the state of the VM and stop it. 
* **vagrant halt**: This will gracefully shutdown the guest operating system and power down the guest machine. 
* **vagrant destroy**: If you want to remove all traces of the guest machine from your system, this is the command you should use. It will power down the machine and remove all guest hard disks

Go [here](http://docs.vagrantup.com/v2/getting-started/teardown.html) for more information about vagrant teardown. 

**Note**: By default it will instantiate a 64 bit VM. In case you want to run a 32 bit VM, you will need to change the ```config.vm.box_url``` parameter in the Vagrantfile as shown below: 
```
## 64 bit Vagrant Box
#config.vm.box_url = "https://d396qusza40orc.cloudfront.net/sdn1/srcs/Vagrant%20Box/coursera-sdn-2015_64bit.box"

## 32 bit Vagrant Box 
config.vm.box_url = "https://d396qusza40orc.cloudfront.net/sdn1/srcs/Vagrant%20Box/coursera-sdn-2015_32bit.box"
```

* Now SSH into the VM:
``` bash
$ vagrant ssh
```



* Programming assignments: You will find the programming assignments in the vm under the directory: /vagrant/assignments.
``` bash
vagrant@coursera-sdn:~$ ls /vagrant/
assignments  README.md  setup  Vagrantfile
```

* To perform a simple test to check if your VM setup is correct, run the command:
```bash
sudo mn
```
This will start a Mininet bash terminal. Type ```xterm h1 h2``` in this terminal. If two external terminals pop out, then your setup worked as expected. 

#### Notes and Tips for running vagrant and the course VM
- Follow the instructions closely
- If you are running a 64bit OS, run a 64 bit VM
- If you are running a 32bit OS, run a 32 bit VM
- Disable Hyper-V on Windows
- Enable Virtualization support on the host (BIOS setup)
- The VM runs 192.168.0.0/24 as default network, if you use that network locally you need to change it (edit Vagrantfile: config.vm.network :private_network, ip: "192.168.0.100”)
- The host machine needs to run an X server (it’s native on Linux; OS X and Windowns require the installation of an X Server)
- Alternative methods to ssh to the VM: run "ssh -X vagrant@192.168.0.100" password is vagrant
- If you see "ssh_exchange_identification: read: Connection reset by peer" when trying to connect using "vagrant ssh" use the alternative method provided above since it has been reported as a valid workaround, this issue is under investigation
- The shared folder: "Coursera-SDN" git cloned folder for the host and /vagrant for the guest

#### Sample setup output for reference
- Following output is from MacOS

```
Coursera-SDN TestUser$ vagrant up
Bringing machine 'default' up with 'virtualbox' provider...
==> default: Clearing any previously set network interfaces...
==> default: Preparing network interfaces based on configuration...
    default: Adapter 1: nat
    default: Adapter 2: hostonly
==> default: Forwarding ports...
    default: 6633 => 6635 (adapter 1)
    default: 22 => 2222 (adapter 1)
==> default: Booting VM...
==> default: Waiting for machine to boot. This may take a few minutes...
    default: SSH address: 127.0.0.1:2222
    default: SSH username: vagrant
    default: SSH auth method: private key
    default: Warning: Connection timeout. Retrying...
    default: Warning: Connection timeout. Retrying...
    default: Warning: Remote connection disconnect. Retrying...
==> default: Machine booted and ready!
==> default: Checking for guest additions in VM...
==> default: Setting hostname...
==> default: Configuring and enabling network interfaces...
==> default: Mounting shared folders...
    default: /vagrant => /Users/TestUser/git/Coursera-SDN



TestUser-MBP:Coursera-SDN TestUser$ vagrant ssh
Welcome to Ubuntu 14.04.2 LTS (GNU/Linux 3.13.0-49-generic x86_64)

 * Documentation:  https://help.ubuntu.com/

 System information disabled due to load higher than 1.0

  Get cloud support with Ubuntu Advantage Cloud Guest:
    http://www.ubuntu.com/business/services/cloud


Last login: Mon May 25 18:00:05 2015 from 10.0.2.2
vagrant@coursera-sdn:~$ ls /vagrant/
assignments  README.md	setup  Vagrantfile
vagrant@coursera-sdn:~$ sudo mn
*** Creating network
*** Adding controller
*** Adding hosts:
h1 h2 
*** Adding switches:
s1 
*** Adding links:
(h1, s1) (h2, s1) 
*** Configuring hosts
h1 h2 
*** Starting controller
c0 
*** Starting 1 switches
s1 ...
*** Starting CLI:
mininet> help

Documented commands (type help <topic>):
========================================
EOF    gterm  iperfudp  nodes        pingpair      py      switch
dpctl  help   link      noecho       pingpairfull  quit    time  
dump   intfs  links     pingall      ports         sh      x     
exit   iperf  net       pingallfull  px            source  xterm 

You may also send a command to a node using:
  <node> command {args}
For example:
  mininet> h1 ifconfig

The interpreter automatically substitutes IP addresses
for node names when a node is the first arg, so commands
like
  mininet> h2 ping h3
should work.

Some character-oriented interactive commands require
noecho:
  mininet> noecho h2 vi foo.py
However, starting up an xterm/gterm is generally better:
  mininet> xterm h2

mininet> h1 ifconfig
h1-eth0   Link encap:Ethernet  HWaddr 12:1e:ad:14:fe:b3  
          inet addr:10.0.0.1  Bcast:10.255.255.255  Mask:255.0.0.0
          inet6 addr: fe80::101e:adff:fe14:feb3/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:1500  Metric:1
          RX packets:14 errors:0 dropped:0 overruns:0 frame:0
          TX packets:8 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000 
          RX bytes:1128 (1.1 KB)  TX bytes:648 (648.0 B)

lo        Link encap:Local Loopback  
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:0 errors:0 dropped:0 overruns:0 frame:0
          TX packets:0 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:0 
          RX bytes:0 (0.0 B)  TX bytes:0 (0.0 B)


mininet> 
mininet> 
mininet> h1 ping h2
PING 10.0.0.2 (10.0.0.2) 56(84) bytes of data.
64 bytes from 10.0.0.2: icmp_seq=1 ttl=64 time=2.15 ms
64 bytes from 10.0.0.2: icmp_seq=2 ttl=64 time=0.331 ms
64 bytes from 10.0.0.2: icmp_seq=3 ttl=64 time=0.165 ms
64 bytes from 10.0.0.2: icmp_seq=4 ttl=64 time=0.073 ms
64 bytes from 10.0.0.2: icmp_seq=5 ttl=64 time=0.085 ms
64 bytes from 10.0.0.2: icmp_seq=6 ttl=64 time=0.035 ms
64 bytes from 10.0.0.2: icmp_seq=7 ttl=64 time=0.099 ms
64 bytes from 10.0.0.2: icmp_seq=8 ttl=64 time=0.088 ms
64 bytes from 10.0.0.2: icmp_seq=9 ttl=64 time=0.139 ms
64 bytes from 10.0.0.2: icmp_seq=10 ttl=64 time=0.089 ms
^C
--- 10.0.0.2 ping statistics ---
10 packets transmitted, 10 received, 0% packet loss, time 9016ms
rtt min/avg/max/mdev = 0.035/0.326/2.156/0.614 ms
mininet> pingall
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 0% dropped (2/2 received)
mininet> pingallfull
*** Ping: testing ping reachability
h1 -> h2 
h2 -> h1 
*** Results: 
 h1->h2: 1/1, rtt min/avg/max/mdev 0.850/0.850/0.850/0.000 ms
 h2->h1: 1/1, rtt min/avg/max/mdev 0.114/0.114/0.114/0.000 ms
mininet> pingpairfull
h1 -> h2 
h2 -> h1 
*** Results: 
 h1->h2: 1/1, rtt min/avg/max/mdev 0.243/0.243/0.243/0.000 ms
 h2->h1: 1/1, rtt min/avg/max/mdev 0.122/0.122/0.122/0.000 ms
mininet> time
*** Elapsed time: 0.000005 secs
mininet> nodes
available nodes are: 
c0 h1 h2 s1

mininet> quit
*** Stopping 1 controllers
c0 
*** Stopping 2 links
..
*** Stopping 1 switches
s1 
*** Stopping 2 hosts
h1 h2 
*** Done
completed in 324.923 seconds

vagrant@coursera-sdn:~$ exit
logout
Connection to 127.0.0.1 closed.
```

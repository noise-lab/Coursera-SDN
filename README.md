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
* **vagrant destroy**: If you want to remove all traces of the guest machine from your system, this is the command you should use. It willpower down the machine and remove all guest hard disks

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
- The VM runs 192.168.0.0/24 as default network, if you use that network locally you need to change it (edit Vagrantfile: config.vm.network :private_network, ip: "192.168.0.100”). It has been reported that on ocations when "vagrant ssh" fails, this alternative method does work. This is under investigation.
- The host machine needs to run an X server (it’s native on Linux; OS X and Windowns require the installation of an X Server)
- Alternative methods to ssh to the VM (ssh -X vagrant@192.168.0.100; password is vagrant)
- The shared folder: "Coursera-SDN" git cloned folder for the host and /vagrant for the guest

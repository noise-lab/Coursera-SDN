##Coursera SDN Virtual Machine Setup

###Setting up the course VM

####Prerequisite

To get started install these softwares on your host machine:

1. Install ***Vagrant***, it is a wrapper around virtualization softwares like VirtualBox, VMWare etc.: http://www.vagrantup.com/downloads

2. Install ***VirtualBox***, this would be your VM provider: https://www.virtualbox.org/wiki/Downloads

3. Install ***Git***, it is a distributed version control system: https://git-scm.com/downloads

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
Note: By default it will instantiate a 64 bit VM. In case you want to run a 32 bit VM, you will need to change the ```config.vm.box_url``` parameter in the Vagrantfile as shown below: 
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

* Programming assignments: You will find the programming assignments in the vm under the directory: /vagrant/Programming-Assignments.
``` bash
vagrant@coursera-sdn:~$ ls /vagrant/
Programming-Assignments  README.md  setup-scripts  Vagrantfile
```

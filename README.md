##Coursera SDN 2015

###Setting up the course VM

####Prerequisite

To get started install these softwares on your host machine:

1. Install ***Vagrant***, it is a wrapper around virtualization softwares like VirtualBox, VMWare etc.: http://www.vagrantup.com/downloads

2. Install ***VirtualBox***, this would be your VM provider: https://www.virtualbox.org/wiki/Downloads

3. Install ***Git***, it is a distributed version control system: https://git-scm.com/downloads

####Basics

* Clone the course repository from Github:
```bash 
$ git clone https://github.com/PrincetonUniversity/Coursera-SDN-2015
```

* Change the directory to Coursera-SDN-2015:
```bash
$ cd Coursera-SDN-2015
```

* Now run the vagrant up command. This will read the Vagrantfile from the current directory and provision the VM accordingly:
```bash
$ vagrant up
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

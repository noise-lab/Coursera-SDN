Coursera SDN 2015

Setting up the course VM

Prerequisite

To get started install these softwares on your host machine:

Install Vagrant, it is a wrapper around virtualization softwares like VirtualBox, VMWare etc.: http://www.vagrantup.com/downloads

Install VirtualBox, this would be your VM provider: https://www.virtualbox.org/wiki/Downloads

Install Git, it is a distributed version control system: https://git-scm.com/downloads

Basics

Clone the course repository from Github:
$ git clone https://github.com/PrincetonUniversity/Coursera-SDN-2015
Change the directory to Coursera-SDN-2015:
$ cd Coursera-SDN-2015
Now run the vagrant up command. This will read the Vagrantfile from the current directory and provision the VM accordingly:
$ vagrant up
Now SSH into the VM:
$ vagrant ssh
Programming assignments: You will find the programming assignments in the vm under the directory: /vagrant/Programming-Assignments.
vagrant@coursera-sdn:~$ ls /vagrant/
Programming-Assignments  README.md  setup-scripts  Vagrantfile

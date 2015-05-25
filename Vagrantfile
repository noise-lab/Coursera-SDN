VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  # All Vagrant configuration is done here. The most common configuration
  # options are documented and commented below. For a complete reference,
  # please see the online documentation at vagrantup.com.

  config.vm.box = "coursera-sdn-2015.box"

  # The url from where the 'config.vm.box' box will be fetched if it
  # doesn't already exist on the user's system.
  # TODO: Upload the box image over Coursera's server and update the url here.
  config.vm.box_url = "http://cs.princeton.edu/~arpitg/coursera_vm/coursera-sdn-2015.box"

 ## Provisioning
 ## We will update the Vagrantfile as the course progresses and students will 
 ## need additional installations to complete the assignments. 
 
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/ryu-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/netasm-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/sdx-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/kinetic-setup.sh"

end

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"

  config.vm.provider "virtualbox" do |v|
      v.customize ["modifyvm", :id, "--cpuexecutioncap", "50"]
      v.customize ["modifyvm", :id, "--memory", "2048"]
  end
  
  ## Guest Config
  config.vm.hostname = "coursera-sdn"
  config.vm.network :private_network, ip: "192.168.0.100"
  config.vm.network :forwarded_port, guest:6633, host:6635 # forwarding of port

  ## Provisioning
  config.vm.provision :shell, privileged: false, :path => "setup-scripts/basic-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "setup-scripts/ovs-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "setup-scripts/mininet-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "setup-scripts/pox-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "setup-scripts/pyretic-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/ryu-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/netasm-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/sdx-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "setup-scripts/kinetic-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "setup-scripts/cleanup.sh"

  ## SSH config
  config.ssh.forward_x11 = true
end

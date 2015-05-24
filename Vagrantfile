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
  config.vm.provision :shell, privileged: false, :path => "basic-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "ovs-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "mininet-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "pox-setup.sh"
  config.vm.provision :shell, privileged: false, :path => "pyretic-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "ryu-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "netasm-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "sdx-setup.sh"
  #config.vm.provision :shell, privileged: false, :path => "kinetic-setup.sh"

  ## SSH config
  config.ssh.forward_x11 = true
end

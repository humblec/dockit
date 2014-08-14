# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "chef/centos-7.0"
  config.vm.define vm_name = "dockit-dev" do |config|
    config.vm.hostname = vm_name
    config.vm.synced_folder ".", "/home/vagrant/dockit", type: "rsync"
    config.vm.provision :shell, :inline => "yum update -y", :privileged => true
    config.vm.provision :shell, :inline => "yum install -y -q gcc python-devel", :privileged => true
    config.vm.provision :shell, :inline => "cd /home/vagrant/dockit && python setup.py install", :privileged => true
  end
end

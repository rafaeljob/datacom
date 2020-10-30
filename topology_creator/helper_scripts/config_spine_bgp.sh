#!/bin/bash

echo "********************************************"
echo "  Running BGP SPINE Post Config - DATACOM   "
echo "********************************************"

sudo su 

export DEBIAN_FRONTEND=noninteractive

# some config still learning :p
cat <<EOT > /etc/network/interfaces
auto lo
iface lo inet loopback
	
auto vagrant
iface vagrant inet dhcp

auto eth0
iface eth0 inet dhcp

EOT

echo ">>>Updating"
apt-get update

#echo ">>>Installing TShark"
#echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
#apt-get install tshark -qy

echo ">>>Changing Permission config.sh"
chmod +x /vagrant/config.sh

echo ">>>Setting IP Forward"
sysctl -w net.ipv4.ip_forward=1 > /dev/null

echo "********************************************"
echo "   Finished SPINE Post Config - DATACOM     "
echo "********************************************"
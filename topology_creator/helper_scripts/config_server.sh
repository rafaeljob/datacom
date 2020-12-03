#!/bin/bash

echo "********************************************"
echo "  Running Server Post Config - DATACOM  "
echo "********************************************"

sudo su 

export DEBIAN_FRONTEND=noninteractive

echo ">>>Updating"
apt-get update

# some config still learning :p
cat <<EOT > /etc/network/interfaces
auto lo
iface lo inet loopback

auto vagrant
iface vagrant inet dhcp

auto eth0
iface eth0 inet dhcp

EOT

#
echo ">>>Changing Permission config.sh"
chmod +x /vagrant/config.sh

#
#echo ">>>Installing TShark"
#echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
#apt-get install tshark -qy

echo ">>>Installing Traceroute"
apt-get install traceroute

echo ">>>Installing Scamper"
apt-get install scamper
  
echo "********************************************"
echo "   Finished Server Post Config - DATACOM    "
echo "********************************************"
#!/bin/bash

echo "********************************************"
echo "  Running Server Post Config - DATACOM  "
echo "********************************************"

sudo su 

#echo "retry 1;" >> /etc/dhcp/dhclient.conf
#echo "timeout 600;" >> /etc/dhcp/dhclient.conf

# some config still learning :p
cat <<EOT > /etc/network/interfaces
auto lo
iface lo inet loopback

auto vagrant
iface vagrant inet dhcp

auto eth0
iface eth0 inet dhcp

EOT

echo ">>>Running Host File"
/vagrant/host.sh
  
echo "********************************************"
echo "   Finished Server Post Config - DATACOM    "
echo "********************************************"
#!/bin/bash

echo "********************************************"
echo "  Running BGP SPINE Post Config - DATACOM   "
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

echo ">>>Updating"
apt-get update

#echo">>>Autoremove"
#apt-get autoremove

#echo">>>Autoclean"
#apt-get autoclean

echo ">>>Installing Quagga"
apt-get install quagga quagga-doc -qy 

echo ">>>Installing TShark"
echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
apt-get install tshark -qy

echo ">>>Copying vtysh.conf"
cp /usr/share/doc/quagga-core/examples/vtysh.conf.sample /etc/quagga/vtysh.conf

echo ">>>Copying zebra.conf"
cp /vagrant/zebra.conf /etc/quagga/zebra.conf

echo ">>>Copying bgpd.conf"
cp /vagrant/bgpd.conf /etc/quagga/bgpd.conf

#echo ">>>Changing Owner"
#chown quagga:quagga /etc/quagga/*.conf
#chown quagga:quaggavty /etc/quagga/vtysh.conf
#chmod 640 /etc/quagga/*.conf

echo ">>>Starting Zebra"
service zebra start

echo ">>>Starting BGPD"
service bgpd start

echo ">>>Setting IP Forward"
sysctl -w net.ipv4.ip_forward=1 > /dev/null

echo "********************************************"
echo "   Finished SPINE Post Config - DATACOM     "
echo "********************************************"
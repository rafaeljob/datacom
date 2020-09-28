#!/bin/bash

echo "********************************************"
echo "  Running BGP LEAF Post Config - DATACOM    "
echo "********************************************"

sudo su 

#echo "retry 1;" >> /etc/dhcp/dhclient.conf
#echo "timeout 600;" >> /etc/dhcp/dhclient.conf

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

#echo ">>>Installing Quagga"
#apt-get install quagga quagga-doc -qy 

#echo ">>>Installing FRRouting"
#curl -s https://deb.frrouting.org/frr/keys.asc | apt-key add -
#FRRVER="frr-stable"
#echo deb https://deb.frrouting.org/frr $(lsb_release -s -c) $FRRVER |  tee -a /etc/apt/sources.list.d/frr.list
#apt install frr frr-pythontools -qy

echo ">>>Installing Bridge-Utils"
apt-get install bridge-utils -qy

echo ">>>Installing TShark"
echo "wireshark-common wireshark-common/install-setuid boolean true" | debconf-set-selections
apt-get install tshark -qy

echo ">>>Changing Permission config.sh"
chmod +x /vagrant/config.sh

#echo ">>>Copying vtysh.conf"
#cp /usr/share/doc/quagga-core/examples/vtysh.conf.sample /etc/quagga/vtysh.conf

#echo ">>>Copying zebra.conf"
#cp /vagrant/zebra.conf /etc/quagga/zebra.conf
#cp /vagrant/zebra.conf /etc/frr/zebra.conf

#echo ">>>Copying bgpd.conf"
#cp /vagrant/bgpd.conf /etc/quagga/bgpd.conf
#cp /vagrant/bgpd.conf /etc/frr/bgpd.conf

#echo ">>>Starting Zebra"
#service zebra start

#echo ">>>Starting BGPD"
#service bgpd start

echo ">>>Setting IP Forward"
sysctl -w net.ipv4.ip_forward=1 > /dev/null

echo "********************************************"
echo "   Finished LEAF Post Config - DATACOM      "
echo "********************************************"
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


#cat <<EOT > /etc/init.d/host
#!/bin/sh
#/vagrant/host.sh
#EOT

#echo ">>>Copying host.sh"
#cp /vagrant/host.sh /etc/init.d/host.sh

echo ">>>Changing Permission"
chmod +x /vagrant/host.sh
#update-rc.d host defaults
#echo ">>>Running Host File"
#/vagrant/host.sh

echo ">>>Installing TShark"
echo "wireshark-common wireshark-common/install-setuid boolean true" | sudo debconf-set-selections
apt-get install tshark -qy
  
echo "********************************************"
echo "   Finished Server Post Config - DATACOM    "
echo "********************************************"
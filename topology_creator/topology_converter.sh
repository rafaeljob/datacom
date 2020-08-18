#!/bin/bash

args=$*
echo "Arguments: " ${args}
echo "Path: " ${PATH}

if [ -z $args ];
then
	return 0
elif [ $args = "-h" ] || [ $args = "--help" ]; 
then
	python3 -B topology_creator.py ${args}
	python3 -B reader.py ${args}
elif [ $args = *"-v"* ] || [ $args = *"--verbose"* ];
	python3 -B topology_creator.py ${args}
	python3 -B reader.py topology.dot -p libvirt -v
	sudo vagrant up
else
	python3 -B topology_creator.py ${args}
	python3 -B reader.py topology.dot -p libvirt
	sudo vagrant up		
fi	

#for host in $allMachines; do
	#echo -e "Running machine" ${host} "configs"
	#sudo vagrant ssh $host -c "sudo chmod +x /vagrant/host.sh"
	#sudo vagrant ssh $host -c "sudo /vagrant/host.sh"
#done
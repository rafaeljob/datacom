#!/bin/bash

args=$*
echo "Arguments: " $args
read -a args_array <<< $args
size_array=${#commandArray[@]}

spine=""; leaf=""; host="";

for (( args_array=0; args_array < $size_array; args_array=args_array+1)); do
  if [[ ${rgs_array[$args]} = "-s" ]];
  then 
	spine=${rgs_array[$args+1]}
  elif [[ ${rgs_array[$args]} = "-l" ]];
  then 
  	leaf=${rgs_array[$args+1]}
  elif [[ ${rgs_array[$args]} = "-l" ]];
  then 
  	host=${rgs_array[$args+1]}
  fi	  
done

echo $spine " -- " $leaf " -- " $host

if [ -z $args ];
then
	echo "Empty Arguments"
elif [ $args = "-h" ] || [ $args = "--help" ]; 
then
	python3 -B topology_creator.py ${args}
	python3 -B reader.py ${args}
elif [ $args = *"-v"* ] || [ $args = *"--verbose"* ];
then	
	python3 -B topology_creator.py ${args}
	python3 -B reader.py topology.dot -p libvirt -v
	#sudo vagrant up
else
	python3 -B topology_creator.py ${args}
	python3 -B reader.py topology.dot -p libvirt
	#sudo vagrant up		
fi	

#for host in $allMachines; do
	#echo -e "Running machine" ${host} "configs"
	#sudo vagrant ssh $host -c "sudo chmod +x /vagrant/host.sh"
	#sudo vagrant ssh $host -c "sudo /vagrant/host.sh"
#done
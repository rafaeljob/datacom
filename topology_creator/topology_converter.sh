#!/bin/bash

args=$*
echo ">>Arguments: " $args
read -a args_array <<< $args
size_array=${#args_array[@]}
#echo ">>Size: " $size_array

spine="1"; leaf="1"; host="1";

for i in $(seq 0 $(($size_array - 1)) ); do
	#echo "arg " $i ": " ${args_array[$i]}
	case "${args_array[$i]}" in
		"-s") spine="${args_array[$(($i + 1))]}" ;;

		"-l") leaf="${args_array[$(($i + 1))]}" ;;

		"-e") host="${args_array[$(($i + 1))]}" ;;
	esac
done


#echo "spine" $spine
#echo "leaf" $leaf
#echo "host" $host
#echo "argsss " $args
if [[ -z $args ]]; then
	echo "Empty Arguments"
	exit 0
elif [[ $args == "-h" ]] || [[ $args == "--help" ]]; then
	#echo "help"
	python3 -B topology_creator.py $args
	python3 -B reader.py $args
	exit 0
elif [[ $args == *"-v"* ]] || [[ $args == *"--verbose"* ]]; then
	#echo "verbose"
	python3 -B topology_creator.py $args
	python3 -B reader.py topology.dot -p libvirt -v
	sudo vagrant up
else
	#echo "else"
	python3 -B topology_creator.py $args
	python3 -B reader.py topology.dot -p libvirt
	sudo vagrant up
fi

wait $!
echo -e "*****************DONE WAITING VAGRANT UP*****************"
#sleep 50

for host in $(seq -f "%02g" 1 $(($leaf * $host))); do
	echo -e "Running machine" "host"${host} "configs"
	sudo vagrant ssh "host"$host -c "sudo chmod +x /vagrant/config.sh && sudo /vagrant/config.sh"
done

for leaf in $(seq -f "%02g" 1 $leaf); do
	echo -e "Running machine" "leaf"${leaf} "configs"
	sudo vagrant ssh "leaf"$leaf -c "sudo chmod +x /vagrant/config.sh && sudo /vagrant/config.sh"
done

for spine in $(seq -f "%02g" 1 $spine); do
	echo -e "Running machine" "spine"${spine} "configs"
	sudo vagrant ssh "spine"$spine -c "sudo chmod +x /vagrant/config.sh && sudo /vagrant/config.sh"
done

#export DEBIAN_FRONTEND=noninteractive
#echo ">>>Installing FRRouting"
#curl -s https://deb.frrouting.org/frr/keys.asc | apt-key add -
#FRRVER="frr-stable"
#echo deb https://deb.frrouting.org/frr $(lsb_release -s -c) "frr-stable" | sudo tee -a /etc/apt/sources.list.d/frr.list
#sudo apt update && sudo apt install frr frr-pythontools -qy
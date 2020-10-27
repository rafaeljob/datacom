#!/bin/bash

RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

args=$*
read -a args_array <<< $args
size_array=${#args_array[@]}

spine="1"; leaf="1"; host="1";

for i in $(seq 0 $(($size_array - 1)) ); do
	case "${args_array[$i]}" in
		"-s") spine="${args_array[$(($i + 1))]}" ;;

		"-l") leaf="${args_array[$(($i + 1))]}" ;;

		"-e") host="${args_array[$(($i + 1))]}" ;;
	esac
done

start=$(date +'%X')

if [[ -z $args ]]; then
	echo -e "\n>>Empty Arguments"
	exit 0
elif [[ $args == "-h" ]] || [[ $args == "--help" ]]; then
	python3 -B topology_creator.py $args
	python3 -B reader.py $args
	exit 0
elif [[ $args == *"-v"* ]] || [[ $args == *"--verbose"* ]]; then
	python3 -B topology_creator.py $args
	python3 -B reader.py topology.dot -p libvirt -v
	echo -e "\n>>>>>>>>>>>>>>>>> VAGRANT UP <<<<<<<<<<<<<<<<<\n"
	sudo vagrant up
else
	python3 -B topology_creator.py $args
	python3 -B reader.py topology.dot -p libvirt
	echo -e "\n>>>>>>>>>>>>>>>>> VAGRANT UP <<<<<<<<<<<<<<<<<\n"
	sudo vagrant up
fi

wait $!
echo -e "\n>>>>>>>>>>>>>>>>> DONE WAITING VAGRANT UP <<<<<<<<<<<<<<<<<\n"

for spine in $(seq -f "%02g" 1 $spine); do
	echo -e "\n>>Running machine" "spine"${spine} "configs"
	sudo vagrant ssh "spine"$spine -c "sudo chmod +x /vagrant/config.sh && sudo /vagrant/config.sh"
done

for leaf in $(seq -f "%02g" 1 $leaf); do
	echo -e "\n>>Running machine" "leaf"${leaf} "configs"
	sudo vagrant ssh "leaf"$leaf -c "sudo chmod +x /vagrant/config.sh && sudo /vagrant/config.sh"
done

for host in $(seq -f "%02g" 1 $(($leaf * $host))); do
	echo -e "\n>>Running machine" "host"${host} "configs"
	sudo vagrant ssh "host"$host -c "sudo chmod +x /vagrant/config.sh && sudo /vagrant/config.sh"
done

finish=$(date +'%X')

echo -e "\n>>ARGUMENTS:  " $args 
echo -e ">>START:  " ${start}
echo -e ">>END:    " ${finish} "\n"

exit 0
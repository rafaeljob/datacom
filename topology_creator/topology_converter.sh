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
echo -e "*****************DONE WATING VAGRANT UP*****************"
#sleep 50

for host in $(seq -f "%02g" 1 $(($leaf * $host))); do
	#echo "host"$host
	echo -e "Running machine" "host"${host} "configs"
	sudo vagrant ssh "host"$host -c "sudo chmod +x /vagrant/host.sh" && "sudo /vagrant/host.sh"
	#sudo vagrant ssh "host"$host -c "sudo /vagrant/host.sh"
done

for leaf in $(seq -f "%02g" 1 $leaf); do
	#echo "host"$host
	echo -e "Running machine" "leaf"${leaf} "configs"
	sudo vagrant ssh "leaf"$leaf -c "sudo chmod +x /vagrant/leaf.sh" && "sudo /vagrant/leaf.sh"
	#sudo vagrant ssh "leaf"$leaf -c "sudo /vagrant/leaf.sh"
done
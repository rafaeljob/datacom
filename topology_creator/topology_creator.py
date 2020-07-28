####
## Dev by Rafael Basso
##
##
####


##
#IMPORTS
##

from topology_creator_header import *
import sys
import argparse
import bcolors
import os
import pydotplus
import shutil
##
#GLOBAL VARS
##

devices = []
SPINE_NUM = 0
LEAF_NUM = 0
EDGE_NUM = 0
OS = ""
MEMORY = 0
VERBOSE = False
VERSION = "0.0.1"
SPINE_START_IP = "192.168."
LEAF_START_IP = "172.16."
TEMP_PATH = "./temp_scripts/"
#PRINTS
##

def print_parse():
	print(bcolors.OK + "#" + bcolors.END + " PARSING ARGUMENTS")

def print_create_machine():
	print(bcolors.OK + "#" + bcolors.END + " CREATING DEVICES")

def print_create_interface():
	print(bcolors.OK + "#" + bcolors.END + " CREATING INTERFACES")	

def print_write_graph():
	print(bcolors.OK + "#" + bcolors.END + " WRITING GRAPH VX")

def print_create_temp():
	print(bcolors.OK + "#" + bcolors.END + " CREATING TEMPORARY CONFIG FILES")

def print_delete_temp():
	print(bcolors.OK + "#" + bcolors.END + " DELETING EXISTING TEMPORARY CONFIG FILES")

def print_fail(exception):
	print(bcolors.FAIL + "#" + bcolors.END + " ERROR: " + "(%s)" % exception)

##
#DEFINES
##
 
def list():
	for device in devices:
		device.print_info()

def add(device, device_name):
	if(device == "spine"):
		devices.append(Spine(device_name=device_name))
	elif(device == "router"):
		devices.append(Router(device_name=device_name))
	elif(device == "switch"):
		devices.append(Switch(device_name=device_name))
	elif(device == "host"):	
		devices.append(Host(device_name=device_name))

def parser():

	global SPINE_NUM
	global LEAF_NUM
	global EDGE_NUM
	global OS
	global MEMORY 
	global VERBOSE 

	print_parse()

	parser = argparse.ArgumentParser(description='Spine-leaf Topology Creator')

	parser.add_argument('-s', '--spine', dest='spine', metavar='spine', type=int, default=1,
							help='Select the amount of spine machines in this topology')

	parser.add_argument('-l', '--leaf', dest='leaf', metavar='leaf', type=int, default=1,
							help='Select the amount of leaf machines in this topology')

	parser.add_argument('-e', '--edge', dest='edge', metavar='edge', type=int, default=1,
							help='Select the amount of servers connected to each leaf')

	parser.add_argument('-o', '--os', dest='os', metavar='os', type=str, default='hashicorp/bionic64',
							help='Select the OS for each machine')

	parser.add_argument('-m', '--memory', dest='memory', metavar='memory', type=int, default=500,
							help='Select the amount of memory for each machine (MB)')

	parser.add_argument('-v', '--verbose', action="store_true",
							help='Show every step made by this program')

	parser.add_argument('--version', action='version', version="Spine-leaf Topology Creator v%s" % VERSION,
							help='Shows the current version of this Spine-leaf Topology Creator')

	args = parser.parse_args()
	ARG_STRING = " ".join(sys.argv)

	SPINE_NUM = args.spine
	LEAF_NUM = args.leaf
	EDGE_NUM = args.edge
	OS = args.os
	MEMORY = args.memory
	if args.verbose: VERBOSE = True
	print("\tinput: %s" % ARG_STRING)

def create_machine():

	print_create_machine()

	for i in range(1, SPINE_NUM+1):
		device_name = "spine%02d" % i
		devices.append(Spine(device_name=device_name, memory=MEMORY, os=OS, vagrant="eth1", function="spine",
								config="./helper_scripts/config_switch_bgp.sh", version="1.0.282"))

	for i in range(1, LEAF_NUM+1):	
		device_name = "leaf%02d" % i
		devices.append(Leaf(device_name=device_name, memory=MEMORY, os=OS, vagrant="eth1", function="leaf",
								config="./helper_scripts/config_switch_bgp.sh", version="1.0.282"))

	for i in range(1, (EDGE_NUM*LEAF_NUM)+1):	
		device_name = "host%02d" % i
		devices.append(Host(device_name=device_name, memory=MEMORY, os=OS, vagrant="eth1", function="host",
								config="./helper_scripts/config_server.sh", version="1.0.282"))

	if VERBOSE:
		list()	

def create_interface():
	print_create_interface()

	spine_leaf = 1
	host_list = []

	spine_local_machine_ip = 1
	leaf_local_network_ip = 1

	for i in range(0, len(devices)):
		if devices[i].get_function() == 'leaf':
			leaf_host = 1
			leaf_spine = 50

			spine_local_network_ip = 1
			leaf_local_machine_ip = 1

			for j in range(0, len(devices)):
				if i != j and devices[j].get_function() != "leaf": 

					if devices[j] not in host_list:

						if devices[j].get_function() == 'spine':
							li_leaf = "swp%d" % leaf_spine
							ri_leaf = "swp%d" % spine_leaf

							local_ip = SPINE_START_IP + str(spine_local_network_ip) + '.' + str(spine_local_machine_ip + 1)
							remote_ip = SPINE_START_IP + str(spine_local_network_ip) + '.' + str(spine_local_machine_ip) 

							devices[i].append_interface(Interface(local_interface=li_leaf, remote_interface=ri_leaf, remote_device=devices[j].get_device_name(),
																	local_ip=local_ip, remote_ip=remote_ip))	#visao da leaf
							devices[j].append_interface(Interface(local_interface=ri_leaf, remote_interface=li_leaf, remote_device=devices[i].get_device_name(),
																	local_ip=remote_ip, remote_ip=local_ip))	#visao da spine

							leaf_spine+= 1
							spine_local_network_ip+= 1

						elif devices[j].get_function() == 'host' and (leaf_host <= EDGE_NUM):	
							li_leaf = "swp%d" % leaf_host
							ri_leaf = "eth1"

							local_ip = LEAF_START_IP + str(leaf_local_network_ip) + '.' + str(leaf_local_machine_ip)
							remote_ip = LEAF_START_IP + str(leaf_local_network_ip) + '.' + str(leaf_local_machine_ip + 1)

							devices[i].append_interface(Interface(local_interface=li_leaf, remote_interface=ri_leaf, remote_device=devices[j].get_device_name(),
																	local_ip=local_ip, remote_ip=remote_ip))	#visao da leaf
							devices[j].append_interface(Interface(local_interface=ri_leaf, remote_interface=li_leaf, remote_device=devices[i].get_device_name(),
																	local_ip=remote_ip, remote_ip=local_ip))	#visao do host

							leaf_host+=	1
							leaf_local_machine_ip+= 2
							host_list.append(devices[j])
							
			spine_leaf+= 1
			spine_local_machine_ip+= 2
			leaf_local_network_ip+= 1

	if VERBOSE:
		list()		

def create_config_files():

	if os.listdir(TEMP_PATH):
		print_delete_temp()
		for directory in os.listdir(TEMP_PATH):
			try:
				if os.listdir(TEMP_PATH + directory):
					for file in os.listdir(TEMP_PATH + directory):
						os.remove(TEMP_PATH + directory + "/" + file)		
				os.rmdir(TEMP_PATH + directory)
			except Exception as e:
				print_fail(e)
				exit(1)

	print_create_temp()
	for device in devices:
		try:
			path = TEMP_PATH + device.get_device_name()
			os.mkdir(path=path)
			write_zebra_file(device=device, path=path)
		except Exception as e:
			print_fail(e)
			exit(1)	

def write_zebra_file(device, path):
	try:
		file = open(path + "/zebra.conf", "w")
		file.write("hostname " + device.get_device_name() + "\n")
		file.write("password zebra\n")
		file.write("!\n")
		for interface in device.get_interfaces():
			file.write("interface " + interface.get_local_interface() + "\n")
			if interface.get_remote_device() == 'host':
				file.write(" ip address " + interface.get_local_ip() + "/24\n")
			else:	#pra spine e leaf	
				file.write(" ip address " + interface.get_local_ip() + "/31\n")
			file.write("!\n")		
		file.write("interface lo\n")
		file.write("!\n")
		file.write("ip forwarding\n")
		file.write("!\n")
		file.write("!\n")
		file.write("line vty\n")
		file.write("!\n")	
	except Exception as e:
			print_fail(e)
			exit(1)		

def add_double_quotes(string):
	return '"' + string + '"' 

#"tor-A" [function="leaf" vagrant="eth1" os="hashicorp/bionic64" version="1.0.282" memory="500" config="./helper_scripts/config_production_switch.sh" ]
def create_node(device):
	node = pydotplus.graphviz.Node(name=add_double_quotes(device.get_device_name()), 
									obj_dict=None)
	node.set('function', add_double_quotes(device.get_function()) )
	node.set('vagrant', add_double_quotes(device.get_vagrant()) )
	node.set('os', device.get_os() )
	node.set('version', device.get_version() )
	node.set('memory', add_double_quotes(str(device.get_memory())) )
	node.set('config', device.get_config() )
	return node

#"tor-A":"swp50" -- "tor-B":"swp49"
def create_edge(src_dev, rmt_dev, src_i, rmt_i):
	src_str = '"' + src_dev + '"' + ':' + '"' + src_i + '"'
	rmt_str = '"' + rmt_dev + '"' + ':' + '"' + rmt_i + '"'
	return pydotplus.graphviz.Edge(src=src_str, dst=rmt_str, obj_dict=None)

def write_graph():
	graph = pydotplus.graphviz.Dot( graph_name='vx', 
									graph_type='graph', 
									strict=False,
									simplify=True)

	for device in devices:
		graph.add_node(create_node(device))

	for device in devices:	
		for interface in device.get_interfaces():
			graph.add_edge(create_edge(src_dev=device.get_device_name(),
										rmt_dev=interface.get_remote_device(),
										src_i=interface.get_local_interface(),
										rmt_i=interface.get_remote_interface()
										))	
	try:
		print_write_graph()	
		graph.write(path="./topology.dot", prog='dot', format='raw')
	except Exception as e:
		print_fail(e)
		#print(bcolors.FAIL + "\t#  " + bcolors.END + "ERROR: " + "(%s)", e)
		exit(1)	

def main():
	'''#dev = Device("dev1")
	rout = Router("tor-B", 800, "hashicorp/bionic64", "127.0.0.1", "eth1", 
		"./helper_scripts/config_production_switch.sh", "leaf", "1.0.282")
	rout2 = Router()

	rout.print_info()
	rout2.print_info()
	rout2.set_host_name("tor-A")
	rout2.print_info()

	int1 = Interface("swp1", "127.0.0.1", 8002, "44:38:39:00:00:08", 
				"serve-A0", "eth1", "127.0.0.1", 9002)
	int2 = Interface("swp2", "127.0.0.1", 8004, "44:38:39:00:00:0C", 
				"serve-A1", "eth1", "127.0.0.1", 9004)
	rout.append_interface(int1)
	rout.append_interface(int2)
	rout.print_info()'''
	os.system('color 7')		
	parser()
	create_machine()
	create_interface()
	create_config_files()
	write_graph()

if __name__ == "__main__":
	main()
exit(0)
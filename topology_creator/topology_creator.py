####
## 
#   Dev by Rafael Basso
##
####


#
##  IMPORTS
###

from topology_creator_header import *
import sys
import argparse
import bcolors
import os
import pydotplus
import jinja2
import math

#
##  GLOBAL VARS
###

DEVICES = []
SPINES = []
LEAFS = []
HOSTS = []
IP_LIST = []

SPINE_NUM = 0
LEAF_NUM = 0
EDGE_NUM = 0
LAN_NUM = 0 
OS = ""
MEMORY = 0
PROTOCOL = ""
VERBOSE = False
CLEAN = False
VERSION = "0.4.1"

SPINE_START_IP = "192.178.0.0"
VLAN_START_IP = "172.16.0.0"
VXLAN_START_IP = "10.10.10.0"
START_ID = "10.0.0."
START_AS = 65000

TEMP_PATH 		= "./temp_scripts/"
ZEBRA_TEMPLATE 	= "./templates/zebra_template.j2"
BGPD_TEMPLATE 	= "./templates/bgpd_template.j2"
CONFIG_TEMPLATE = "./templates/config_template.j2"
LEAF_TEMPLATE 	= "./templates/leaf_template.j2"
RR_TEMPLATE 	= "./templates/route_reflector_template.j2"
INFO_TEMPLATE	= "./templates/info_template.j2"
HOST_CONFIG_TEMPLATE = "./templates/host_configure_template.j2"

#
##	PRINTS
###

def print_parse():
	print(bcolors.OK + "#" + bcolors.END + " PARSING ARGUMENTS")

def print_create_machine():
	print(bcolors.OK + "#" + bcolors.END + " CREATING DEVICES")

def print_create_interface():
	print(bcolors.OK + "#" + bcolors.END + " CREATING INTERFACES")	

def print_write_graph():
	print(bcolors.OK + "#" + bcolors.END + " WRITING GRAPH VX")

def print_write_info():
	print(bcolors.OK + "#" + bcolors.END + " WRITING INFO FILE")

def print_create_temp():
	print(bcolors.OK + "#" + bcolors.END + " CREATING TEMPORARY CONFIG FILES")

def print_delete_temp():
	print(bcolors.OK + "#" + bcolors.END + " DELETING EXISTING TEMPORARY CONFIG FILES")

def print_delete_files():
	print(bcolors.OK + "#" + bcolors.END + " DELETING EXISTING TEMPORARY FILES")

def print_fail(exception):
	print(bcolors.FAIL + "#" + bcolors.END + " ERROR: " + "(%s)" % exception)

#
##	DEFINES
###
 
def list(lst):
	for device in lst:
		device.print_info()

def parser():

	global SPINE_NUM
	global LEAF_NUM
	global EDGE_NUM
	global LAN_NUM
	global OS
	global MEMORY 
	global PROTOCOL
	global TUNNEL
	global CLEAN
	global VERBOSE 

	parser = argparse.ArgumentParser(description='Spine-leaf Topology Creator')

	#group = parser.add_mutually_exclusive_group()

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

	parser.add_argument('-p', '--protocol', dest='protocol', choices=["evpn", "bgp"], default='bgp',
				help='Choose the protocol \{evpn or bgp}')

	parser.add_argument('-ln', '--lan', dest='lan', metavar='lan', type=int, default=1,
							help='Select the amount of VxLAN in each leaf')

	parser.add_argument('-v', '--verbose', action="store_true",
							help='Show every step made by this program')

	parser.add_argument('--clean', action="store_true",
							help='Remove all temp files')

	parser.add_argument('--version', action='version', version="Spine-leaf Topology Creator v%s" % VERSION,
							help='Shows the current version of this Spine-leaf Topology Creator')

	print_parse()
	args = parser.parse_args()
	ARG_STRING = " ".join(sys.argv)

	SPINE_NUM = args.spine
	LEAF_NUM = args.leaf
	EDGE_NUM = args.edge
	OS = args.os
	MEMORY = args.memory
	PROTOCOL = args.protocol
	LAN_NUM = args.lan

	if args.verbose: VERBOSE = True
	if args.clean: CLEAN = True
	#print("\tinput: %s" % ARG_STRING)

def create_machine():
	print_create_machine()

	for i in range(1, SPINE_NUM+1):
		device_name = "spine%02d" % i
		SPINES.append(Spine(device_name=device_name, memory=MEMORY, os=OS, vagrant="eth1", function="spine",
								config="./helper_scripts/config_spine_bgp.sh", version="1.0.282", as_number=START_AS, router_id=START_ID + str(20+i)))
	for i in range(1, LEAF_NUM+1):	
		device_name = "leaf%02d" % i
		LEAFS.append(Leaf(device_name=device_name, memory=MEMORY, os=OS, vagrant="eth1", function="leaf",
								config="./helper_scripts/config_leaf_bgp.sh", version="1.0.282", as_number=(START_AS+10+i), router_id=START_ID + str(10+i)))
	for i in range(1, (EDGE_NUM*LEAF_NUM*LAN_NUM)+1):	
		device_name = "host%02d" % i
		HOSTS.append(Host(device_name=device_name, memory=MEMORY, os=OS, vagrant="eth1", function="host",
								config="./helper_scripts/config_server.sh", version="1.0.282"))	

def spine_leaf_interface():
	nt_list = []
	#all interfaces are created considering the Leafs vision
	for i in range(0, len(LEAFS)):
		rinf = 'swp%d' % (i+1)
		network = nt_fetch(SPINE_START_IP, nt_list, 2, 1)

		for j in range(0, len(SPINES)):
			linf = 'swp%d' % (j+51)
			network = nt_fetch(network, nt_list, 2, 100)
			rip = ip_fetch(network)
			lip = ip_fetch(network)

			LEAFS[i].append_interface(Interface(local_interface=linf, remote_interface=rinf, remote_device=SPINES[j].get_device_name(),
										local_ip=lip, remote_ip=rip, remote_as=SPINES[j].get_as_number(), interface_type="x"))	

			SPINES[j].append_interface(Interface(local_interface=rinf, remote_interface=linf, remote_device=LEAFS[i].get_device_name(),
										local_ip=rip, remote_ip=lip, remote_as=LEAFS[i].get_as_number(), interface_type="x"))
				
def leaf_host_interface():
	nt_list = []
	#all interfaces are created considering the Leafs vision
	for i in range(0, len(LEAFS)):
		for l in range(1, LAN_NUM+1):
			if PROTOCOL == 'bgp':
				network = nt_fetch(VLAN_START_IP, nt_list, 2, 1)
				lip = ip_fetch(network)
				LEAFS[i].append_interface(Interface(local_interface="vlan" + str(10), remote_interface="NOTHING", remote_device="NOTHING",
							local_ip=lip, remote_ip="NOTHING", remote_as="", vni=10, interface_type="bridge"))
	
			elif PROTOCOL == 'evpn':
				network = VXLAN_START_IP
				lip = LEAFS[i].get_router_id()
				#for l in range(1, LAN_NUM+1):
				LEAFS[i].append_interface(Interface(local_interface="vxlan" + str(l*10), remote_interface="NOTHING", remote_device="NOTHING",
									local_ip=lip, remote_ip="NOTHING", remote_as="", vni=(l*10), interface_type="vxlan"))
				LEAFS[i].append_interface(Interface(local_interface="br" + str(l*10), remote_interface="NOTHING", remote_device="NOTHING",
									local_ip="NOTHING", remote_ip="NOTHING", remote_as="", vni=(l*10), interface_type="bridge"))
				
			for j in range((EDGE_NUM*LAN_NUM*i) + (l-1)*EDGE_NUM, (EDGE_NUM*LAN_NUM*(i+1)) - (LAN_NUM-l)*EDGE_NUM):
				linf = 'swp%d' % (1+j-(EDGE_NUM*LAN_NUM*i))
				rip = ip_fetch(network)
	
				LEAFS[i].append_interface(Interface(local_interface=linf, remote_interface='eth1', remote_device=HOSTS[j].get_device_name(),
									local_ip='0.0.0.0', remote_ip=rip, remote_as=HOSTS[j].get_as_number(), vni=(l*10), interface_type="dummy"))	#add vni
				
				HOSTS[j].append_interface(Interface(local_interface='eth1', remote_interface=linf, remote_device=LEAFS[i].get_device_name(),
									local_ip=rip, remote_ip=lip, remote_as=LEAFS[i].get_as_number(), interface_type="x"))	

def ip_fetch(network):
	lst = network.split('.')
	new = lst[3]

	while 1:
		new = ("%d" % (int(new, 10)+1))
		lst[3] = new
		new_ip = '.'.join(lst)
		if new_ip not in IP_LIST:
			IP_LIST.append(new_ip)
			break
	return new_ip

def nt_fetch(prefix, nt_list, Nbyte, offset):
	lst = prefix.split('.')
	new = lst[Nbyte]

	while 1:
		new = ("%d" % (int(new, 10)+offset))
		lst[Nbyte] = new
		new_nt = '.'.join(lst)
		if new_nt not in nt_list:
			nt_list.append(new_nt)
			break
	return new_nt			

def clean_files():
	print_delete_files()
	for directory in os.listdir("./"):
		if directory == "Vagrantfile" or directory == "topology.dot":
			try:
				os.remove("./" + directory)
			except Exception as e:
				print_fail(e)
				exit(1)
					
def clean_temp_scripts():
	print_delete_temp()
	for directory in os.listdir(TEMP_PATH):
		if directory == "interfaces.txt":
			os.remove(TEMP_PATH + directory)
		elif directory != ".gitignore":
			try:
				if os.listdir(TEMP_PATH + directory):
					for file in os.listdir(TEMP_PATH + directory):
						os.remove(TEMP_PATH + directory + "/" + file)		
				os.rmdir(TEMP_PATH + directory)
			except Exception as e:
				print_fail(e)
				exit(1)

def create_temp_scripts():
	if len(os.listdir(TEMP_PATH)) > 1:
		clean_temp_scripts()

	print_create_temp()
	create_device_files(SPINES)
	create_device_files(LEAFS)
	for hst in HOSTS:
		path = create_dir(hst.get_device_name())
		render_file(template=HOST_CONFIG_TEMPLATE, 
					path=(path + '/config.sh'),
					device=hst,
					protocol=PROTOCOL,
					devices=HOSTS)

	render_info_file(SPINES, LEAFS, HOSTS)

def create_device_files(devices):
	for device in devices:
		path = create_dir(device.get_device_name())
		if PROTOCOL == 'evpn':
			render_file(template=RR_TEMPLATE, path=(path + '/bgpd.conf'), device=device, protocol=None, devices=None)
		elif PROTOCOL == 'bgp':
			render_file(template=BGPD_TEMPLATE, path=(path + '/bgpd.conf'), device=device, protocol=None, devices=None)
		render_file(template=ZEBRA_TEMPLATE, path=(path + '/zebra.conf'), device=device, protocol=None, devices=None)
		render_file(template=CONFIG_TEMPLATE, path=(path + '/config.sh'), device=device, protocol=PROTOCOL, devices=None)	

def create_dir(dir_name):
	try:
		path = TEMP_PATH + dir_name
		os.mkdir(path=path)
	except Exception as e:
		print_fail(e)
		exit(1)
	return path

def render_file(template, path, device, protocol, devices):
	try:		
		#le arquivo do template
		template = jinja2.Template(open(template).read())
	except Exception as e:
			print_fail(e)
			exit(1)
	try:
		#renderiza o template lido previamente com as informacoes extraidas da topologia
		with open(path, 'w') as outfile:
			outfile.write(template.render(device=device, protocol=protocol, devices=devices))
	except Exception as e:
		print_fail(e)
		exit(1)

def render_info_file(spines, leafs, hosts):
	print_write_info()
	try:		
		#le arquivo do template
		template = jinja2.Template(open(INFO_TEMPLATE).read())
	except Exception as e:
			print_fail(e)
			exit(1)
	try:
		#renderiza o template lido previamente com as informacoes extraidas da topologia
		with open(TEMP_PATH + "/interfaces.txt", 'w') as outfile:
			outfile.write(template.render(spines=spines, leafs=leafs, hosts=hosts))
	except Exception as e:
		print_fail(e)
		exit(1)							

def add_double_quotes(string):
	return '"' + string + '"' 

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

def create_edge(src_dev, rmt_dev, src_i, rmt_i):
	return pydotplus.graphviz.Edge(src=(add_double_quotes(src_dev) + ':' + add_double_quotes(src_i)), 
								dst=(add_double_quotes(rmt_dev) + ':' + add_double_quotes(rmt_i)), obj_dict=None)

def add_nodes(graph, devices):
	for device in devices:
		graph.add_node(create_node(device))

def add_edges(graph, devices):
	for device in devices:	
		for interface in device.get_interfaces():
			if interface.get_interface_type() != "bridge" and interface.get_interface_type() != "vxlan":
				graph.add_edge(create_edge( src_dev=device.get_device_name(),
											rmt_dev=interface.get_remote_device(),
											src_i=interface.get_local_interface(),
											rmt_i=interface.get_remote_interface()
											))

def write_graph():
	graph = pydotplus.graphviz.Dot( graph_name='vx', 
									graph_type='graph', 
									strict=False,
									simplify=True)

	add_nodes(graph, SPINES)
	add_nodes(graph, LEAFS)
	add_nodes(graph, HOSTS)

	add_edges(graph, SPINES)
	add_edges(graph, LEAFS)
	add_edges(graph, HOSTS)

	try:
		print_write_graph()	
		graph.write(path="./topology.dot", prog='dot', format='raw')
	except Exception as e:
		print_fail(e)
		exit(1)		

#
##  MAIN
###

def main():
	os.system('color 7')		
	parser()
	if CLEAN:
		clean_files()
		clean_temp_scripts()
	else:	
		create_machine()
		spine_leaf_interface()
		leaf_host_interface()
		create_temp_scripts()
		write_graph()

	list(LEAFS)
	list(HOSTS)

if __name__ == "__main__":
	main()
exit(0)
####
## This Python file uses the following encoding: utf-8
## Dev by Rafael Basso
####

import sys

class Device: 
	def __init__(self, device_name, memory, os, tunnel_ip, 
					vagrant, config, function, version):
		self.device_name = device_name
		self.memory = memory
		self.os = os
		self.tunnel_ip = tunnel_ip
		self.config = config
		self.vagrant = vagrant
		self.function = function
		self.version = version
		self.interfaces = []

	# setters	
	def set_device_name(self, device_name):
		self.device_name = device_name

	def set_memory(self, memory):
		self.memory = memory

	def set_os(self, os):
		self.os = os

	def set_tunnel_ip(self, tunnel_ip):
		self.tunnel_ip = tunnel_ip

	def set_config(self, config):
		self.config = config

	def set_vagrant(self, vagrant):
		self.vagrant = vagrant

	def set_function(self, function):
		self.function = function

	def set_version(self, function):
		self.version = version

	def set_interfaces(self, interfaces):
		self.interfaces = interfaces

	# getters
	def get_device_name(self):
		return self.device_name

	def get_memory(self):
		return self.memory

	def get_os(self):
		return self.os

	def get_tunnel_ip(self):
		return self.tunnel_ip

	def get_config(self):
		return self.config

	def get_vagrant(self):
		return self.vagrant

	def get_function(self):
		return self.function

	def get_version(self):
		return self.version

	def get_interfaces(self):
		return self.interfaces								
	
	# printer	
	def print_info(self):
		print("- device_name"	+ ":".ljust(9)	+ "%s" % self.device_name)
		print("- os"			+ ":".ljust(18)	+ "%s" % self.os)
		print("- memory"		+ ":".ljust(14)	+ "%s" % self.memory)
		print("- vagrant" 		+ ":".ljust(13)	+ "%s" % self.vagrant)
		print("- tunnel_ip" 	+ ":".ljust(11) + "%s" % self.tunnel_ip)
		print("- config" 		+ ":".ljust(14)	+ "%s" % self.config)
		print("- function" 		+ ":".ljust(12)	+ "%s" % self.function)
		print("- version" 		+ ":".ljust(13)	+ "%s" % self.version)
		print("- interfaces:")
		for interface in self.interfaces:
			interface.print_info()

		print("\n")

	# functions
	def append_interface(self, interface):
		self.interfaces.append(interface)

class Spine(Device):
	def __init__(self, device_name=None, memory=None, os=None, tunnel_ip=None, 
					vagrant=None, config=None, function=None, version=None):
		super(Spine, self).__init__(device_name, memory, os, tunnel_ip, 
					vagrant, config, function, version)

class Router(Device):
	def __init__(self, device_name=None, memory=None, os=None, tunnel_ip=None, 
					vagrant=None, config=None, function=None, version=None):
		super(Router, self).__init__(device_name, memory, os, tunnel_ip, 
					vagrant, config, function, version)

class Switch(Device):
	def __init__(self, device_name=None, memory=None, os=None, tunnel_ip=None, 
					vagrant=None, config=None, function=None, version=None):
		super(Switch, self).__init__(device_name, memory, os, tunnel_ip, 
					vagrant, config, function, version)

class Leaf(Device):
	def __init__(self, device_name=None, memory=None, os=None, tunnel_ip=None, 
					vagrant=None, config=None, function=None, version=None):
		super(Leaf, self).__init__(device_name, memory, os, tunnel_ip, 
					vagrant, config, function, version)

class Host(Device):
	def __init__(self, device_name=None, memory=None, os=None, tunnel_ip=None, 
					vagrant=None, config=None, function=None, version=None):
		super(Host, self).__init__(device_name, memory, os, tunnel_ip, 
					vagrant, config, function, version)

class Interface:
	def __init__(self, local_interface=None, local_ip=None, local_port=None, mac=None, 
		remote_device=None, remote_interface=None, remote_ip=None, remote_port=None):
		self.local_interface = local_interface
		self.local_ip = local_ip
		self.local_port = local_port
		self.mac = mac
		self.remote_device = remote_device
		self.remote_interface = remote_interface
		self.remote_ip = remote_ip
		self.remote_port = remote_port

	# setters
	def set_local_interface(self, local_interface):
		self.local_interface = local_interface

	def set_local_ip(self, local_ip):
		self.local_ip = local_ip

	def set_local_port(self, local_port):
		self.local_port = local_port

	def set_mac(self, mac):
		self.mac = mac

	def set_remote_device(self, remote_device):
		self.remote_device = remote_device

	def set_remote_interface(self, remote_interface):
		self.remote_interface = remote_interface

	def set_remote_ip(self, remote_ip):
		self.remote_ip = remote_ip

	def set_remote_port(self, remote_port):
		self.remote_port = remote_port

	# getters
	def get_local_interface(self):
		return self.local_interface

	def get_local_ip(self):
		return self.local_ip

	def get_local_port(self):
		return self.local_port

	def get_mac(self):
		return self.mac

	def get_remote_device(self):
		return self.remote_device

	def get_remote_interface(self):
		return self.remote_interface

	def get_remote_ip(self):
		return self.remote_ip

	def get_remote_port(self):
		return self.remote_port

	# printer	
	def print_info(self):
		print("".ljust(22) + "local_interface"	+ ":".ljust(13) + "%s" % self.local_interface)
		print("".ljust(22) + "local_ip"			+ ":".ljust(20) + "%s" % self.local_ip)
		print("".ljust(22) + "local_port"		+ ":".ljust(18) + "%s" % self.local_port)
		print("".ljust(22) + "mac"				+ ":".ljust(25) + "%s" % self.mac)
		print("".ljust(22) + "remote_device"	+ ":".ljust(15) + "%s" % self.remote_device)
		print("".ljust(22) + "remote_interface"	+ ":".ljust(12) + "%s" % self.remote_interface)
		print("".ljust(22) + "remote_ip" 		+ ":".ljust(19) + "%s" % self.remote_ip)
		print("".ljust(22) + "remote_port"		+ ":".ljust(17) + "%s" % self.remote_port)
		print("\n")
		

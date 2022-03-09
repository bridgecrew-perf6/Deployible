# This file is designed to take in a list of IP addresses
# It then formats said IPs and appends them to the Ansible Inventory

import sys
import os.path
import ipaddress
import re

def dict_factory(targets):
	target_ip_lst = ''
	target_vpc_lst = ''
	num_targets = int(len(targets)+1)
	t_index = list(range(1, num_targets, 4))
	for plc in t_index:
		target_ip_lst += str(targets[plc] + "\n")

	v_index = list(range(-1, num_targets, 4))
	for plc in v_index:
		target_vpc_lst += str(targets[plc] + "\n")

	#Use two lists to make dict - locate VPC where host is as target VPC
	#Remove all other IPS outside that VPC
	#Return dict of valid IPs. Send to wrtie function

def main():
	if sys.argv[1] == "0":
		# We are using AWS IPs
		if os.path.exists("./vars/target_info.txt"):
			f = open("./vars/target_info.txt", "r")
			ct = 0
			for l in f.readlines():
				if ct == 0:
					host_ip = l.strip()
					ct += 1
				else:
					instance_ips = l.split("'")[1::2]
					dict_factory(instance_ips)
		else:
			pass

	else:
		# We are using NMAP IPs
		print("fail")


main()


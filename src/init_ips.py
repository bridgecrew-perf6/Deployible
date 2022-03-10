# This file is designed to take in a list of IP addresses
# It then formats said IPs and appends them to the Ansible Inventory

import sys
import os
import ipaddress
import re
import shutil


def dict_factory(targets, host_ip):
	target_ip_lst = []
	target_vpc_lst = []
	num_targets = int(len(targets)+1)
	t_index = list(range(1, num_targets, 4))
	for plc in t_index:
		target_ip_lst.append(targets[plc])

	v_index = list(range(-1, num_targets, 4))
	for plc in v_index:
		target_vpc_lst.append(targets[plc])

	target_index = int(len(targets)/4)+1

	ip_dict = dict(zip(target_ip_lst, target_vpc_lst))
	
	for key in ip_dict:
		if key == host_ip:
			target_vpc = ip_dict.get(key)
		else:
			pass
	target_factory(ip_dict, target_vpc)


def target_factory(target_dict, target_vpc):
	f_target_list = []
	for key in target_dict:
		if target_dict.get(key) == target_vpc:
			f_target_list.append(key)
		else:
			pass

	f_target_list_frmt_str = ''
	for ip in f_target_list:
		f_target_list_frmt_str += str(ip + ' ansible_python_interpreter=/usr/bin/python3\n')	

	ans_hosts_f = str("/etc/ansible/hosts")
	if os.path.exists(ans_hosts_f):
		os.remove(ans_hosts_f)
		shutil.copyfile("./vars/hosts", ans_hosts_f)
		r = open(ans_hosts_f, "a+")
		r.write("\n[targets]\n")
		r.write(f_target_list_frmt_str)
		r.close()
	else:
		pass

def main():
	if sys.argv[1] == "0":
		# We are using AWS IPs
		if os.path.exists("./vars/target_info.tmp"):
			f = open("./vars/target_info.tmp", "r")
			ct = 0
			for l in f.readlines():
				if ct == 0:
					host_ip = l.strip()
					ct += 1
				else:
					instance_ips = l.split("'")[1::2]
					dict_factory(instance_ips, host_ip)
		else:
			pass

	else:
		# We are using NMAP IPs
		pass


main()

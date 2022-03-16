# This file is designed to take in a list of IP addresses
# It then formats said IPs and appends them to the Ansible Inventory

import sys
import os
import ipaddress
import re
import shutil
import logging
from datetime import datetime

logf = datetime.now().strftime('../logs/host_discovery_proc_%H_%M_%d_%m.log')
logging.basicConfig(level=logging.DEBUG, filename=logf)
logging.info(str(datetime.now()))

def cleanup():
	nmap_targets = str("./vars/nmap_targets.tmp")
	aws_targets = str("./vars/target_info.tmp")

	if os.path.exists(nmap_targets):
		os.remove(nmap_targets)
		logging.info("nmap_targets.tmp has been deleted")
	else:
		logging.debug("nmap_targets.tmp doesnt exist: Most likely an error occured in Host Discovery")

	if os.path.exists(aws_targets):
		os.remove(aws_targets)
		logging.info("target_info.tmp has been deleted")
	else:
		logging.debug("target_info.tmp doesnt exist: Most likely an error occured in Host Discovery")


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
	logging.debug("IP Dictionary Created Successfully")
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

	logging.debug("Targets formatted correctly")
	write_to_host(f_target_list_frmt_str)

def write_to_host(frmt_str):
	ans_hosts_f = str("/etc/ansible/hosts")
	if os.path.exists(ans_hosts_f):
		os.remove(ans_hosts_f)
		shutil.copyfile("./vars/templates/hosts", ans_hosts_f)
		r = open(ans_hosts_f, "a+")
		r.write("\n[targets]\n")
		r.write(frmt_str)
		r.close()
		logging.info("Targets Successfully written to Ansible Inventory")
	else:
		logging.error("Failed to write targets to Ansible Inventory. Check Permissions")


def main():

	if sys.argv[1] == "0":
		logging.info("Using AWS generated IP Addresses")
		target_file_path = "./vars/target_info.tmp"
		if os.path.exists(target_file_path):
			f = open(target_file_path, "r")
			ct = 0
			for l in f.readlines():
				if ct == 0:
					host_ip = l.strip()
					ct += 1
				else:
					instance_ips = l.split("'")[1::2]
					dict_factory(instance_ips, host_ip)
		else:
			logging.error("AWS Targets were not generated properly. target_info.tmp most likely missing")

	elif sys.argv[1] == "1":
		logging.info("Using NMAP generated IP Addresses")
		target_file_path = ("./vars/nmap_targets.tmp")
		if os.path.exists(target_file_path):
			f = open(target_file_path)
			ct = 0
			f_target = ""
			print_target = ""
			for l in f.readlines():
				l = l.strip()
				print_target += str(l + ", ")
				f_target += str(l + ' ansible_python_interpreter=/usr/bin/python3\n')
			write_to_host(f_target)
			logging.info("Targets Discovered: " + str(print_target[:-2]))
			f.close()
		else:
			logging.error("NMAP Targets were not gathered properly. target_info.tmp most likely missing")
	else:
		logging.error("Invalid arguements passed. Check host_disc_aws.yml OR aws_disc_nmap.yml")

main()
cleanup()





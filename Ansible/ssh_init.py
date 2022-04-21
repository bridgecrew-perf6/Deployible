# This file helps initiate proper OS targeting and customization for SSH
# SSH is used by ansible to connect to hosts
#
import shutil
import os

def write_to_hosts(rhel_based, deb_based):
	ans_hosts_f = str("/etc/ansible/hosts")
	ans_temp = str("/home/hosts.tmp")

	shutil.copy(ans_hosts_f, ans_temp)




	r = open(ans_temp, "a+")
	r.write("\n[Debian]\n")
	for x in deb_based:
		r.write(str(x) + " ansible_ssh_user=ubuntu ansible_python_interpreter=/usr/bin/python3\n")

	r.write("\n[Redhat]\n")
	for y in rhel_based:
		r.write(str(y) + " ansible_ssh_user=ec2-user ansible_python_interpreter=/usr/bin/python3\n")

	r.write("\n# Finalized\n")

	r.close()

	os.remove(ans_hosts_f)
	shutil.copy(ans_temp, ans_hosts_f)

def main():
	with open('/home/rhel_ip.txt') as f:
 		rhel_based = f.readlines()
	rhel_based = [x.strip() for x in rhel_based]
	
	with open('/home/all_ip.txt') as g:
		all_ip = g.readlines()
	all_ip = [x.strip() for x in all_ip]

	deb_based = [item for item in all_ip if item not in rhel_based]

	write_to_hosts(rhel_based, deb_based)

main()	
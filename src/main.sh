#! /bin/bash

# This script is the main controller for this program.
# It is responsible for launching the appropriate scirpts and playbooks
#

#ansible-playbook -C ../Ansible/init.yml

read -p "Do you wish to use your AWS Credentials to Speed up Host Discovery? [Y/N]: " ans

if [[ "$ans" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	python3 ./vault.py
	ansible-playbook ../Ansible/host_disc_aws.yml --ask-vault-pass
else
	ansible-playbook ../Ansible/host_disc_nmap.yml
fi 


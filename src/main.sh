#! /bin/bash

# This script is the main controller for this program.
# It is responsible for launching the appropriate scirpts and playbooks
#

# Intro
echo -e "Welcome to Deployible!\nThis program uses a collection of Ansible Playbooks and Scripts to map a subnet and install Snort"
read -p "Press Enter to continue"
#  Intro

# Install Dependencies
echo -e "\nInstalling Dependencies...\n"
#ansible-playbook -C ../Ansible/init.yml &>/dev/null
echo -e "Dependencies Installed\n"
# Install Dependencies

# Host Discovery
echo -e "Discovering Hosts\nThis is done via AWS Credentialed login, or NMAP\nConsult the README for additional information on generating AWS Keys"
read -p "Do you wish to use your AWS Credentials for Host Discovery? [Y/N]: " ans

if [[ "$ans" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	echo -e "Discovering Hosts via AWS API\n"
	python3 ./vault.py
	echo -e "\nEnter Ansible Vault Password"
	ansible-playbook ../Ansible/host_disc_aws.yml --ask-vault-pass &>/dev/null
	sudo python3 ./init_ips.py 0 
else
	echo -e "\nDiscovering Hosts via NMAP\n"
	ansible-playbook ../Ansible/host_disc_nmap.yml &>/dev/null
	echo -e "Hosts Discovered"
	echo -e "Writing Targets to Ansible Configuration"
	sudo python3 ./init_ips.py 1

	echo -e "\nTargets Successfully Loaded"
fi
echo -e "Host Discovery Complete\n"
# Host Discovery

# Snort Installation

# Snort Installation



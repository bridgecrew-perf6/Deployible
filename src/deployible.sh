#! /bin/bash

# This script is the main controller for this program.
# It is responsible for launching the appropriate scirpts and playbooks
#

#Logging Setup
exec 3>&1 4>&2
trap 'exec 2>&4 1>&3' 0 1 2 3
exec 1>deploy.log&1 2>&1

#Logging Setup

# Intro
echo -e "Welcome to Deployible!\nThis program uses a collection of Ansible Playbooks and Scripts to map a subnet and install Snort" >&3
read -p "Press Enter to continue" >&3
#  Intro

# Install Dependencies
echo -e "\nInstalling Dependencies...\n" >&3
echo -e "\nInstalling Dependencies...\n"
sudo ansible-playbook -C ../Ansible/init.yml &>/dev/null
export ANSIBLE_HOST_KEY_CHECKING=False
echo -e "Dependencies Installed\n" >&3
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
	sudo ansible-playbook ../Ansible/host_disc_aws.yml --ask-vault-pass &>/dev/null
	sudo python3 ./init_ips.py 0 
else
	echo -e "\nDiscovering Hosts via NMAP\n"
	sudo ansible-playbook ../Ansible/host_disc_nmap.yml &>/dev/null
	echo -e "Hosts Discovered"
	echo -e "Writing Targets to Ansible Configuration"
	sudo python3 ./init_ips.py 1 

	echo -e "\nTargets Successfully Loaded"
fi
echo -e "Host Discovery Complete\n"
# Host Discovery


# Snort Installation
# Check target Operating System
sudo ansible-playbook ../Ansible/ssh_name.yml &>/dev/null
sudo python3 ../Ansible/ssh_init.py &>/dev/null
#sudo ansible-playbook ../Ansible/snort_kickoff.yml

#########
sudo ansible-playbook ./config/snort_config.yml &>/dev/null
sudo ansible-playbook ../Ansible/snort_install.yml &>/dev/null
# Snort Installation

# Snort Configuration
sudo ansible-playbook ../Snort/pulledpork/pulled_pork.yml &>/dev/null
# Snort Configuration

# Alerting Setup
sudo ansible-playbook ../Snort/alerting/setsys.yml &>/dev/null
sudo ansible-playbook ../Snort/alerting/target_sys.yml &>/dev/null
sudo python3 ../Snort/alerting/swatch_config.py
# Alerting Setup


# Verification
sudo ansible-playbook ../Ansible/verify.yml &>/dev/null
# Verification

read -p "Do you want this terminal to monitor?? [Y/N]: " ans2

if [[ "$ans2" =~ ^([yY][eE][sS]|[yY])$ ]]
then
	sudo swatchdog -c /home/ubuntu/.swatchdogrc -t /var/log/auth.log
else
	echo "\nTo monitor logs, SSH into and open a terminal on this machine\nRun ./monitor.sh in the base Deployible Directory"
fi



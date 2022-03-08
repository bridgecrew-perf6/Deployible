#! /bin/bash

MAINIP=$(ip route | grep src | awk '{print $9}')
GATEWAYIP=$(ip route | grep default | awk '{print $3}')
SUBNET=$(ip route | grep proto | grep -v default | awk '{print $1}')
echo ${SUBNET}

python3 vault.py
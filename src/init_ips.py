# This file is designed to take in a list of IP addresses
# It then formats said IPs and appends them to the Ansible Inventory

import sys
import os.path


def main():
	print(sys.argv[1])
	if sys.argv[1] == "0":
		# We are using AWS IPs
		if os.path.exists("./priv.txt"):
			f = open("./priv.txt", "r")
			ft = f.readline()
			frmt = ft.split('"')[1::2]

			print(frmt)
			#HERE

		else:
			print("Fail1")

	else:
		# We are using NMAP IPs
		print("fail")

main()
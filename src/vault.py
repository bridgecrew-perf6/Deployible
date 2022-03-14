import os
import subprocess
import getpass

if os.path.exists("./vars/VAULT.yml"):
	print("Vault File Exists\nIf the previously loaded keys are correct - Proceed\n")
else:
	print("Creating Ansible Vault\nThis Vault holds your encrypted keys\nEncrypting with AES-256")
	ec2_access_key = getpass.getpass("Enter your AWS EC2 Access Key (Hidden): \n")
	ec2_secret_key = getpass.getpass("Enter your AWS EC2 Secret Key (Hidden): \n")
	kyz = str("ec2_access_key: "+ ec2_access_key + "\nec2_secret_key: " + ec2_secret_key)
	f = open("./vars/VAULT.yml", "w")
	f.write(kyz)
	f.close()
	subprocess.run(["ansible-vault", "encrypt", "./vars/VAULT.yml"])


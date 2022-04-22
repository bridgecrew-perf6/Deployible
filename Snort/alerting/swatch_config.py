#
# Configures the swatchrc template for a specific host, and level of alerting
#
import os
import getpass

def main():
	print("\nWelcome to the Alerting Module!\nHere we configure how you want to be alerted.\n You have two options:\n1:Swatchdog Terminal Alterts\n2:Email Alerts (AWS SES REQUIRED)\n")
	
	if os.path.exists("/home/ubuntu/.swatchdogrc"):
		os.remove("/home/ubuntu/.swatchdogrc")

	choice = int(input("Choice: "))
	if choice == 1:
		term()
	elif choice == 2:
		email()
	else:
		print("Invalid Input")
		main()

def email():
	print("Email Alerting Selected!\nWARNING: If YOU DO NOT HAVE AWS SES SET UP EMAIL WILL NOT WORK\n")
	email_addr = input("\nEnter an email to forward alerts to: ")
	email_addr_comp = input("\nReenter email to confirm: ")
	if str(email_addr) == str(email_addr_comp):
		pass
	else:
		print("Emails do not match!")
		email()

	print("\n~Alerting Description~\nSee README for in-depth description of alerting levels.\n3 - Low Severity\n2 - Moderate Severity\n1 - High Severity")
	alerting_lvl = int(input("\nEnter an Alerting Level: "))

	if alerting_lvl != 1 and alerting_lvl != 2 and alerting_lvl != 3:	
		print("Invalid Choice!")
		term()
	else:
		pass

	conf_email(email_addr, alerting_lvl)


def term():
	print("\nSwatch alerts selected!\nThis will open a terminal that displays alerts, as well as log them.\nThis terminal is started upon startup as well")
	color = str("red")
	print("\n~Alerting Description~\nSee README for in-depth description of alerting levels.\n3 - Low Severity\n2 - Moderate Severity\n1 - High Severity")
	alerting_lvl = int(input("Alerting Level: "))

	if alerting_lvl != 1 and alerting_lvl != 2 and alerting_lvl != 3:	
		print("Invalid Choice!")
		term()
	else:
		pass

	conf_term(alerting_lvl)


def conf_term(alerting_lvl):

	conf_file = str("/home/ubuntu/.swatchdogrc")

	if alerting_lvl == 1:
		f = open(conf_file, "a")
		f.write("watchfor /[Priority: 1]/\necho red\n")
		f.write("watchfor /[Priority: 2]/\necho red\n")
		f.write("watchfor /[Priority: 3]/\necho red\n")		
		f.close()

	elif alerting_lvl == 2:
		f = open(conf_file, "a")
		f.write("watchfor /[Priority: 2]/\necho red\n")
		f.write("watchfor /[Priority: 3]/\necho red\n")
		f.close()

	elif alerting_lvl == 3:
		f = open(conf_file, "a")
		f.write("watchfor /[Priority: 3]/\necho red\n")
		f.close()

	else:
		print("Internal Error")
		main()

	print("Swatchdog Configured!")


def conf_email(email_addr, alerting_lvl):

	conf_file = str("/home/ubuntu/.swatchdogrc")
	mail_conf = str("mail="+str(email_addr)+", subject='Snort Logging Alert!'")	

	if alerting_lvl == 1:
		f = open(conf_file, "a")
		f.write("watchfor /[Priority: 1]/\necho red\n" + mail_conf + "\n")
		f.write("watchfor /[Priority: 2]/\necho red\n" + mail_conf + "\n")
		f.write("watchfor /[Priority: 3]/\necho red\n" + mail_conf + "\n")		
		f.close()

	elif alerting_lvl == 2:
		f = open(conf_file, "a")
		f.write("watchfor /[Priority: 2]/\necho red\n" + mail_conf + "\n")
		f.write("watchfor /[Priority: 3]/\necho red\n" + mail_conf + "\n")
		f.close()

	elif alerting_lvl == 3:
		f = open(conf_file, "a")
		f.write("watchfor /[Priority: 3]/\necho red\n" + mail_conf + "\n")
		f.close()

	else:
		print("Internal Error")
		main() 

	print("Swatchdog Configured!")

main()	

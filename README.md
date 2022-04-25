# Deployible

Deployible is a collection of Ansible Playbooks, Python, and Bash scripts that allow the user to install Snort across Amazon Web Services EC2 instances. This program automatically discovers hosts within your network, configures Snort per the network environment and OS, installs Snort, and then sets up alert forwarding.

The intent of this program is to allow an untrained user to utilize Snort in their environment, without the hassle of learning how to set up the tool.


## Installation & Dependencies

### Ansible Installation

```
sudo apt install ansible
```
### Deployible Installation
There is no need to install Deployible. 
When you run the program, it checks for its dependencies and installs them if needed.

## Prerequisties

#### SSH Keys
* SSH keys are required to be set up and consistent amoungst target machines
* If you are using AWS, this is set up for you, you just need to generate and select the proper key when building your EC2 instance

#### AWS Keys
* In order to use the AWS Host Discovery method of detection, you need to provide Deployible with your AWS Access and Secret Keys
* These can be generated in your AWS Console under Your Account -> Security Credentials -> Access Keys -> Create New Access Key
* Your credentials are stored in an AES-256 encrypted [Ansible Vault](https://docs.ansible.com/ansible/latest/user_guide/vault.html)

## Usage

Once you have installed Ansible and downloaded the Deployible package, move into the src directory and launch the script below.

```bash
cd deployible/src
sudo ./deployible.sh
```
## Host Discovery
Hosts are discovered two ways:<br />
1 - NMAP Scans <br />
2 - AWS EC2 & VPC API <br />

NMAP scans are used to enumerate the network to determine the IP addresses of potential targets on the network. AWS's API is used to pull in metadata on instance that are within the same VPC as the host running Deployible.

## Snort and Rules
Snort is configured per OS of each target. Templates are used to do this. If you want to integrate your own Snort.conf file with this tool, replace the snort.conf or snort.conf.rh files in the src/vars/templates directory.

Rules are pulled from the newest set of registered free rules from Snort.org using the PulledPork program. There is also a set of default rules that are transferred to the targets in the event that PulledPork should fail.

## Alerting and Logging
* Deployible Alerts can be viewed at any point by examining the log files on the host machine
* It is reccomended to connect to the machine running deployible in a separate console and monitoring via the terminal output
* You can view incoming messages at any time using the monitor.sh script in the Deployible directory
* Plan accordingly with disk space for logs.

### Email Alerts
* If you plan on utilizing Email Alerts with Deployible, you <ins>must </ins> have AWS Simple Email Service set up

## Alerting Levels
Alerting levels in Deployible are based on the Snort Rules Classification level. A basic outline is below: <br />
1 - High, Moderate, and Low priority alerts  <br />
2 - High and Moderate priority Alerts  <br />
3 - High priority alerts only  <br />

Details on alert classifications can be found in the classification.config file within Snort or [here](https://github.com/threatstream/snort/blob/master/etc/classification.config)

## Limitations
* Debian, Redhat/CentOS, AMZN Linux are the only operating systems supported
* AWS integration only
* Email Alerts require AWS SES configuration

### Code Walkthrough
https://youtu.be/dyE_UsZtNSE

## License
[APACHE2](http://www.apache.org/licenses/)

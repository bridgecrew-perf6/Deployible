#! /bin/bash

cd /home
sudo git clone https://github.com/shirkdog/pulledpork.git
cd pulledpork/

sudo cp pulledpork.pl /usr/local/bin
sudo chmod +x /usr/local/bin/pulledpork.pl
sudo cp ./etc/*.conf /etc/snort
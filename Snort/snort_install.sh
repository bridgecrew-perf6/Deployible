#! /bin/bash

wget https://www.snort.org/downloads/snort/daq-2.0.7.tar.gz
tar xvzf daq-2.0.7.tar.gz                      
cd daq-2.0.7
sudo ./configure && make && sudo make install

cd ..

wget https://www.snort.org/downloads/snort/snort-2.9.19.tar.gz
tar xvzf snort-2.9.19.tar.gz
                      
cd snort-2.9.19
./configure --enable-sourcefire && make && sudo make install

sudo ldconfig
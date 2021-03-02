#!/bin/bash
# This script will install pywebdriver and a signed ssl certificate for localhost to avoid having to accept the self-signed certificate in the browser

sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 305CB544DDFC7A97
sudo apt-add-repository 'deb [arch=amd64] http://apt.akretion.com/ pywebdriver-nightly main'
sudo apt update
sudo apt install pywebdriver libnss3-tools
cd /etc/pywebdriver
sudo mkdir cert
sudo chown pywebdriver:$USER cert
cd cert
sudo wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.1/mkcert-v1.4.1-linux-amd64
sudo chmod +x mkcert-v1.4.1-linux-amd64
sudo ./mkcert-v1.4.1-linux-amd64 -install
sudo ./mkcert-v1.4.1-linux-amd64 localhost 127.0.0.1
cd /etc/pywebdriver
sudo chown -R pywebdriver:$USER cert
sudo sed -i 's/\/etc\/ssl\/certs\/ssl-cert-snakeoil.pem/\/etc\/pywebdriver\/cert\/localhost+1.pem/g' config.ini
sudo sed -i 's/\/etc\/ssl\/private\/ssl-cert-snakeoil.key/\/etc\/pywebdriver\/cert\/localhost+1-key.pem/g' config.ini
sudo service pywebdriver stop
sudo service pywebdriver start

#sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python si vous voulez utiliser un port < 1024
#sudo sed -i 's/bind\=127\.0\.0\.1\:8069/bind=127.0.0.1:443/g' config.ini

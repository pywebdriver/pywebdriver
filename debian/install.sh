#!/bin/bash
# This script will install pywebdriver and a signed ssl certificate for localhost to avoid having to accept the self-signed certificate in the browser

set -euxo pipefail

export $(cat /etc/os-release | grep UBUNTU_CODENAME)
wget https://github.com/akretion/pywebdriver/releases/latest/download/pywebdriver_${UBUNTU_CODENAME}.deb
sudo apt update
sudo apt install --reinstall --yes ./pywebdriver_${UBUNTU_CODENAME}.deb
rm -f ./pywebdriver_${UBUNTU_CODENAME}.deb
sudo mkdir -p /etc/pywebdriver/cert
sudo chown pywebdriver:$(whoami) /etc/pywebdriver/cert
sudo wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.1/mkcert-v1.4.1-linux-amd64 -P /etc/pywebdriver/cert
sudo chmod +x /etc/pywebdriver/cert/mkcert-v1.4.1-linux-amd64
cd /etc/pywebdriver/cert
sudo /etc/pywebdriver/cert/mkcert-v1.4.1-linux-amd64 -install
sudo /etc/pywebdriver/cert/mkcert-v1.4.1-linux-amd64 localhost 127.0.0.1
sudo chown -R pywebdriver:$(whoami) /etc/pywebdriver/cert
sed -i -e '/cors_origins=/a\' -e 'sslcert=\/etc\/pywebdriver\/cert\/localhost+1.pem' /etc/pywebdriver/config.ini
sed -i -e '/sslcert=/a\' -e 'sslkey=\/etc\/pywebdriver\/cert\/localhost+1-key.pem' /etc/pywebdriver/config.ini
sudo service pywebdriver stop
sudo service pywebdriver start

#sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python si vous voulez utiliser un port < 1024
#sudo sed -i 's/bind\=127\.0\.0\.1\:8069/bind=127.0.0.1:443/g' config.ini

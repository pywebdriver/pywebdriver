#!/bin/bash
# This script will install pywebdriver and a signed ssl certificate for localhost to avoid having to accept the self-signed certificate in the browser
# Lauch without sudo

set -euo pipefail

echo -e "\e[1;33m## Installation of Pywebdriver \e[0m"
export $(cat /etc/os-release | grep UBUNTU_CODENAME)
case "$(uname -m)" in
	x86_64) deb_suffix=""; mkcert_arch="amd64" ;;
	aarch64 | arm64) deb_suffix="_arm64"; mkcert_arch="arm64" ;;
	*) echo "Unsupported architecture: $(uname -m)"; exit 1 ;;
esac
deb="pywebdriver_${UBUNTU_CODENAME}${deb_suffix}.deb"
wget https://github.com/pywebdriver/pywebdriver/releases/latest/download/${deb}
sudo apt update
sudo apt install --reinstall --yes ./${deb}
rm -f ./${deb}

# Variables
host=$(cat /etc/pywebdriver/config.ini | grep -m 1 host | awk '{print substr($0,6)}')
port=$(cat /etc/pywebdriver/config.ini | grep -m 1 port= | awk '{print substr($0,6)}')

# HTTPS
echo -e "\e[1;33m## Handle HTTPS ? (y/n) \e[0m"
read -p "" -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]
then
	sudo mkdir -p /etc/pywebdriver/cert
	sudo chown pywebdriver:$(whoami) /etc/pywebdriver/cert
	mkcert="mkcert-v1.4.4-linux-${mkcert_arch}"
	sudo wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.4/${mkcert} -P /etc/pywebdriver/cert
	sudo chmod +x /etc/pywebdriver/cert/${mkcert}
	cd /etc/pywebdriver/cert
	sudo /etc/pywebdriver/cert/${mkcert} -install
	sudo /etc/pywebdriver/cert/${mkcert} localhost 127.0.0.1
	sudo chown -R pywebdriver:$(whoami) /etc/pywebdriver/cert
	sudo sed -i 's/.*sslcert.*/sslcert=\/etc\/pywebdriver\/cert\/localhost+1.pem/' /etc/pywebdriver/config.ini
	sudo sed -i 's/.*sslkey.*/sslkey=\/etc\/pywebdriver\/cert\/localhost+1-key.pem/' /etc/pywebdriver/config.ini
	sudo service pywebdriver stop
	sudo service pywebdriver start
	http="https"
else
	sudo sed -i 's/.*sslkey.*/;sslkey/' /etc/pywebdriver/config.ini
	sudo sed -i 's/.*sslcert.*/;sslcert/' /etc/pywebdriver/config.ini
	sudo service pywebdriver stop
	sudo service pywebdriver start
	http="http"
fi

echo -e "\e[1;33m## END of installation of Pywebdriver \e[0m"
echo -e "\e[1;32m## You might check on $http://$host:$port \e[0m"
echo -e "\e[1;33m## ⚠ You might need to reboot your computer to make it work \e[0m"
echo -e "\e[1;33m## ⚠ Check journalctl -feu pywebdriver otherwise \e[0m"


#sudo setcap 'cap_net_bind_service=+ep' /usr/bin/python si vous voulez utiliser un port < 1024
#sudo sed -i 's/bind\=127\.0\.0\.1\:8069/bind=127.0.0.1:443/g' config.ini

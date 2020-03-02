#!/bin/bash
cd /etc/pywebdriver
sudo mkdir cert
sudo chown $USER:$USER cert
cd cert
wget https://github.com/FiloSottile/mkcert/releases/download/v1.4.1/mkcert-v1.4.1-linux-amd64
chmod +x mkcert-v1.4.1-linux-amd64
./mkcert-v1.4.1-linux-amd64 -install
./mkcert-v1.4.1-linux-amd64 localhost 127.0.0.1
cd /etc/pywebdriver
sudo sed -i 's/\/etc\/ssl\/certs\/ssl-cert-snakeoil.pem/\/etc\/pywebdriver\/cert\/localhost+1.pem/g' config.ini
sudo sed -i 's/\/etc\/ssl\/private\/ssl-cert-snakeoil.key/\/etc\/pywebdriver\/cert\/localhost+1-key.pem/g' config.ini
sudo chown -R pywebdriver cert
sudo service pywebdriver stop
sudo service pywebdriver start

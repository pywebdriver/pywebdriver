#!/bin/bash
cd /etc/pywebdriver
sudo mkdir cert
sudo chown $USER:$USER cert
cd cert
# mkcert only publishes linux-arm64 binaries since v1.4.4
case "$(uname -m)" in
    aarch64 | arm64) mkcert_version="v1.4.4"; mkcert_arch="arm64" ;;
    *) mkcert_version="v1.4.1"; mkcert_arch="amd64" ;;
esac
mkcert="mkcert-$mkcert_version-linux-$mkcert_arch"
wget https://github.com/FiloSottile/mkcert/releases/download/$mkcert_version/$mkcert
chmod +x $mkcert
./$mkcert -install
./$mkcert localhost 127.0.0.1 ::1
cd /etc/pywebdriver
sudo sed -i 's/\/etc\/ssl\/certs\/ssl-cert-snakeoil.pem/\/etc\/pywebdriver\/cert\/localhost+2.pem/g' config.ini
sudo sed -i 's/\/etc\/ssl\/private\/ssl-cert-snakeoil.key/\/etc\/pywebdriver\/cert\/localhost+2-key.pem/g' config.ini
sudo chown -R pywebdriver cert
sudo service pywebdriver stop
sudo service pywebdriver start

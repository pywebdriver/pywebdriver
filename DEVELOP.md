# Develop Locally

## Install pywebdriver locally

Run the following commands:

```bash
python3 -m venv env
source env/bin/activate
./env/bin/python -m pip install --upgrade pip
./env/bin/python -m pip install -r ./requirements.txt

cp ./config/config.ini.tmpl ./config.ini

sudo groupadd --force usbusers
sudo adduser $USERNAME usbusers --quiet
sudo adduser $USERNAME dialout --quiet
sudo adduser $USERNAME ssl-cert --quiet
sudo cp ./debian/99-pywebdriver.rules /etc/udev/rules.d/

sudo service udev restart
```

## Run pywebdriver locally

```bash
source env/bin/activate
./pywebdriverd
```

If everything is OK, you could access to the pywebdriver web interface here
http://localhost:8069/

## Generate a build locally

As a requirement, docker should be installed.

```bash
./build_ubuntu_22_04.sh
```

if you want to install the generated package, run:

```
sudo apt-get  install ./build/pywebdriver_20230809_amd64.deb
```

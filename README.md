# pywebdriver

## Summary

Python Web Services to communicate wih Devices.

The aim of this project is to ease the communication between application and Devices,
providing light WebServices based on Python-Flask libraries. The software can be
installed on a computer or a Raspberry-like device. It is compatible with Linux
distribution.

## Table of Content

- [Features](#features)
  - [Web Page](#feature-a)
  - [Specific WebServices for Odoo](#feature-b)
  - [Generic WebServices using CUP](#feature-c)
- [End-Users / Customers Section](#customers)
- [Contributors](#contributors)
- [Developers Section](#developers)
  - [Installation on Debian/Ubuntu](#install-debian)
  - [Installation on Mac OS X](#install-osx)
  - [Installation on Windows 10](#install-windows)
  - [Browser settings](#browser-settings)
  - [Specific configuration](#specific-configuration)
  - [Development](#development)
  - [Contribute](#contribute)
  - [Localization](#localization)
  - [Other Projects](#other-projects)

# <a name="features"></a>Features

## <a name="feature-a"></a>Web Page

This apps provides a light flask app to:

- know the state of the devices;
- know informations about system;
- test communication with some devices (e.g. send a test message to the customer
  display, print a test ticket, etc...).

## <a name="feature-b"></a>Specific WebServices for Odoo

The aim of this sub project is to provide WebServices and Web Page to simulate the
behaviour of Odoo Apps (hw_proxy applications & co) to allow Odoo users to use Odoo
Point of Sale with PyWebDriver as a Proxy.

- **Odoo8**:
  - **Printers** :
    - Epson TM-T20
  - **Credit Card Reader**:
    - Ingenico and Sagem credit card readers with Telium Manager version 37783600 or
      superior
    - Ingenico i2200 check reader and writer
  - **Customer Display**:
    - Bixolon BCD-1100
    - Bixolon BCD-1000
    - [Epson OCD300](http://www.aures-support.fr/NEWSITE/ocd300/)
  - **Scale**:
    - TODO : planned by GRAP (Any help welcome);
  - **Barcode Reader**, **Cash Box** :
    - Not Planned

## <a name="feature-c"></a>Generic WebServices using CUP

Done.

# <a name="customers"></a>End-Users / Customers Section

If you're interested by a feature that is not currently supported, please
[contact our team](http://www.akretion.com) for a quotation.

Otherwise, if you like this project, feel free to make a donation.

# <a name="contributors"></a>Contributors

The main contributors of this project are :

- Sylvain Le Gal <https://twitter/legalsylvain>
- Sébastien Beau <sebastien.beau@akretion.com>
- Arthur Vuillard <arthur@hashbang.fr>
- Sylvain Calador <sylvain.calador@akretion.com>

A lot of the code come from other projects. Licences and copyright are mentionned in
each file or in a readme file of the folder. The main other contributors are:

- Odoo Part: **Odoo S.A.** <http://odoo.com>
- Cros Decorator for Flask: **Armin Ronacher** <http://flask.pocoo.org/snippets/56/>
- ESCPOS driver: **Manuel F Martinez** <manpaz@bashlinux.com>

# <a name="developers"></a>Developers Section

## <a name="install-debian"></a>Installation on Debian/Ubuntu [OLD]

```
sudo add-apt-repository ppa:akretion-team/pywebdriver
sudo apt-get update
sudo apt-get install pywebdriver
```

## <a name="install-bionic"></a>Installation on Ubuntu 18.04 [NEW]

```
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 305CB544DDFC7A97
sudo apt-add-repository 'deb [arch=amd64] http://apt.akretion.com/ pywebdriver-nightly main'
sudo apt update
sudo apt install pywebdriver
```

If you update from the OLD version, you will need to uninstall nginx after upgrading or
you could face port reservation problems. Also it is not required anymore so there is no
reason to have it.

## <a name="install-script"></a>Installation on Ubuntu 18.04 with a signed certificate using mkcert

Alternatively you can use the script
[debian/install.sh](https://github.com/akretion/pywebdriver/tree/master/debian/install.sh).
It will install pywebdriver and you will not have to accept the self-signed certificate
anymore on https.

## <a name="install-osx"></a>Installation on Mac OS X

Pywebdriver can be installed on Mac OS X and is successfully used in production on a Mac
OS X computer with Bixolon customer display, Ingenico credit card reader and check
printer. TODO: write installation instructions.

## <a name="install-windows"></a>Installation on Windows 10

In Windows 10, pywebdriver works as a Windows service that communicates with printers.

### Install your printer

#### For Epson TM-T20IIII

- Go there :
  https://epson.com/Support/Point-of-Sale/Thermal-Printers/Epson-TM-T20III-Series/s/SPT_C31CH51001
- Download and install :
  - OPOS ADK v3.00ER6 (might be useless, to be tested)
  - Advanced Printer Driver v6.01

Launch "Advanced Printer Driver v6.01", select your `Port Type` (e.g USB), save Settings
and click `Test Print` : it should print something !

### Get Build and install

- In this repo, get the latest build in releases :
  https://github.com/akretion/pywebdriver/releases
- Unzip it
- Generate certificate for making https to work
- It will create two files in C:\pywebdriver
- Move the files you unzipped in this folder (some paths are absolute and would not
  accept that the folder could be move later on)

### Configuration

- Open config/config.ini with your favorite editor
- (optional) Add or remove drivers according to your needs (connection to
  display_driver, bank terminal)
- (optional) Change host or port number
- Add two lines in flask option for certificates (under cors_origins=\*)

```
sslcert=c:/pywebdriver/localhost+2.pem
sslkey=c:/pywebdriver/localhost+2-key.pem
```

### Install pywebdriver as a service

- Go to your pywebdriver driver
- Right click on install.bat file and execute it as administrator (beware, with normal
  display, file is just named `install`)
- It will create a Windows service : at Windows start, pywebdriver will be launched
- Open your browser et go to the host and port you choose. By default
  https://localhost:8069
- Try to print and succeed !

### If you change some config

- Go to your pywebdriver driver
- Right click on install.bat file and it will restart the service

## <a name="browser-settings"></a>Browser settings

You need to confirmed security exception on your browers for the following paths:
http://localhost and https://localhost

see
<a href="https://support.mozilla.org/en-US/kb/what-does-your-connection-is-not-secure-mean">here</a>
and click on 'Advanced' and 'confirm security exception'

## <a name="browser-settings"></a>Base configuration

#### config.ini file

Copy the config.ini.tmpl file to config.ini and make modifications as wished.

It is possible to load selectively drivers you need as some are incompatible.

Add a line in config.ini file like :

```
[application]
drivers=odoo8,cups_driver
```

If not, default drivers will be loaded:

- cups_driver
- display_driver
- escpos_driver
- serial_driver
- signature_driver
- telium_driver
- opcua_driver
- odoo7
- odoo8

## <a name="browser-settings"></a>Specific configuration

#### <a name="browser-settings"></a>SSL support

It is possible to enable SSL on Flask level to avoid mixed content on browsers.

Generate private and public key (e.g.: self-signed with openssl
<https://www.openssl.org/docs/manmaster/man1/openssl.html>) and place them at the root.

Add entries in config file like:

```
[flask]
sslcert=cert.pem
sslkey=privkey.pem

```

#### <a name="browser-settings"></a>Epson OCD300

For the customer display **Epson OCD300**, you need to change the config file
(config/config.ini).

Change line device_name in category [display_driver] with this :

```
device_name=/dev/ttyACM0
```

## <a name="development"></a>Development

To test this module, do the following steps:

- download it from git;

```
git clone https://github.com/akretion/pywebdriver.git
```

- Install dependency by running this two command

```
sudo apt-get install cups python-cups python-pip python-netifaces
sudo pip install -r requirement.txt
```

- set correct parameters in the config/config.ini file;
- call this command:

```
   python pywebdriver.py
```

- Call the url : http://localhost:8069 (by default, but depending of your config.ini
  file) in a browser to see devices state;

## <a name="contribute"></a>Contribute

If you find a bug, feel free to report it and submit a bugfix.

If you want to propose extra features not yet covered, please contact us or submit a
Pull Request.

## <a name="localization"></a>Localization

For the moment, localization is managed for english and french languages. If you want to
manage extra lozalisation, do the following:

- call this command to generate '.pot' file:

```
pybabel extract -F translations/settings_babel.cfg -o translations/i18n.pot .
```

- call one of the two commands to generate '.po' file:

```
pybabel init -i translations/i18n.pot -d translations -l <code>  # (First time)
pybabel update -i translations/i18n.pot -d translations          # (Next times)
```

- Edit your '.po' file and write correct translation;
- call this command to generate '.mo' file:

```
pybabel compile -d translations
```

- Change your config.ini file to test the result;
- Do a Pull Request to share your work;

## <a name="other-projects"></a>Other Projects

If you're interested by this project, you could perhaps take a look at these other
projects:

- [Odoo](https://github.com/odoo/odoo)
- [OCA pos](https://github.com/OCA/pos)
- [OpenERP-ledDisplay](https://github.com/guerrerocarlos/OpenERP-ledDisplay)
- [ProxyPoS](https://github.com/Fedrojesa/ProxyPoS/)

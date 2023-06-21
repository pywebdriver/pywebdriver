# pywebdriver

## Summary

Python Web Services to communicate with Devices.

The aim of this project is to ease the communication between application and Devices,
providing light WebServices based on Python-Flask libraries. The software can be
installed on a computer or a Raspberry-like device. It is compatible with Linux and
Windows distributions.

## Table of Content

- [Features](#features)
  - [Web Page](#feature-a)
  - [Specific WebServices for Odoo](#feature-b)
- [End-Users / Customers Section](#customers)
- [Contributors](#contributors)
- [Developers Section](#developers)
  - [Installation on Debian/Ubuntu](#install-ubuntu)
  - [Installation on Mac OS X](#install-osx)
  - [Installation on Windows 10](#install-windows)
  - [Compilation on Windows 11](#compile-windows)
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

- **Odoo8 - Odoo12**:
  - **Printers** :
    - Epson TM-T20 II and Epson TM-T20 III
    - Epson TM-T70
    - Epson TM-P20
    - Netchip POS Printer Aures ODP 333
  - **Credit Card Reader**:
    - Ingenico and Sagem credit card readers with Telium Manager version 37783600 or
      superior
    - Ingenico i2200 check reader and writer
    - Adyen terminals (compatible with Adyen Terminal API 3.0 -
      https://docs.adyen.com/point-of-sale/terminal-api-fundamentals)
  - **Customer Display**:
    - Bixolon BCD-1100
    - Bixolon BCD-1000
    - [Epson OCD300](http://www.aures-support.fr/NEWSITE/ocd300/)
    - SAGA SGDP240
    - Labau LD240 (non-optimal)
  - **Scale**:
    - 8217 Mettler Toledo protocol
      - Mettler Toledo Ariva-S
  - **Barcode Reader**:
    - They are usually recognized as keyboards and do not need pywebdriver to function
  - **Cash Box** :
    - The communication is usually handled by the receipt printer via Esc/Pos

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

## <a name="install-ubuntu"></a>Installation on Ubuntu 18.04 and 20.04 with a signed certificate using mkcert

```
wget https://raw.githubusercontent.com/akretion/pywebdriver/master/debian/install.sh
sudo chmod +x install.sh
sudo ./install.sh
```

If you update from an OLD version, you will need to uninstall nginx after upgrading or
you could face port reservation problems. Also it is not required anymore so there is no
reason to have it.

If your Firefox has a master password, there will be an extra step. The terminal will
ask _Enter Password or Pin for "NSS Certificate DB"_ and you have to write your Firefox
master password.

## <a name="install-osx"></a>Installation on Mac OS X

Pywebdriver can be installed on Mac OS X and is successfully used in production on a Mac
OS X computer with Bixolon customer display, Ingenico credit card reader and check
printer. TODO: write installation instructions.

## <a name="install-windows"></a>Installation on Windows 10

In Windows 10, pywebdriver works as a Windows service that communicates with printers.
It doesn't work on Windows 7.

### Install your printer

#### For Epson TM-T20III

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
- Run generate_certificates.bat to make https work
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

- You have to fit Windows printer's name (1) and config.ini `printer_name`(2) in
  `escpos` category. Either you change (1)to fit (2) or otherwise. By default,
  config.ini variable is `escpos` so you can change (1) in Windows printers
  configuration.

### Install pywebdriver as a service

- Go to your pywebdriver folder
- Right click on install.bat file and execute it as administrator (beware, with normal
  display, file is just named `install`)
- It will create a Windows service : at Windows start, pywebdriver will be launched
- Open your browser et go to the host and port you choose. By default
  https://localhost:8069
- Try to print and succeed !

### If you change some config

- Go to your pywebdriver folder
- Execute (as an admin) install.bat file and it will restart the service.

## <a name="compile-windows"></a>Compilation on Windows 11

If you need to compile pywebdriver from scratch in Windows 11, it is a prerequisite to
install these:

You can help yourself by using [Chocolatey](https://chocolatey.org/) to install these
softwares more easily

- [Git](https://git-scm.com/download/win)
- [Python 3.9](https://www.python.org/downloads/windows/)
  - Click on add to `PATH` variable while installing, or remember where it is installed
    to specify later the full path to the binary.
- [Microsoft Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  - It's enough to select `Desktop development with C++`, suboptions `MSVC build tools`
    and `Windows 11 SDK`
- [InnoSetup](https://jrsoftware.org/isdl.php)
  - Remember where you install it. You will later need to specify the full path to the
    `iscc.exe` binary (`C:\Program Files....`).

Open a command window and clone the git repository. Change directory into the cloned
one. Then, you can follow the installation steps outlined for `windows-latest` in the
[GitHub workflow file](https://github.com/akretion/pywebdriver/blob/master/.github/workflows/main.yml).
If you use the `CMD` native terminal instead of `Git-Bash`, you will need to change `/`
by `\`. If `python.exe` or `iscc.exe` commands are not recognized, try specifying the
full path.

## <a name="browser-settings"></a>Browser settings

You need to confirmed security exception on your browers for the following paths
https://localhost:8069, click on 'Advanced' and 'confirm security exception'. See
<a href="https://support.mozilla.org/en-US/kb/what-does-your-connection-is-not-secure-mean">here</a>

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

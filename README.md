pywebdriver
===========

Summary
-------
Python Web Services to communicate wih Devices.

The aim of this project is to ease the communication between application and Devices, providing light WebServices based on Python-Flask libraries. The software can be installed on a computer or a Raspberry-like device. It is compatible with Linux distribution.

Table of Content
----------------
* [Features](#features)
  * [Web Page](#feature-a)
  * [Specific WebServices for Odoo](#feature-b)
  * [Generic WebServices using CUP](#feature-c)
* [End-Users / Customers Section](#customers)
* [Contributors](#contributors) 
* [Developers Section](#developers)
  * [Installation on Debian/Ubuntu](#install-debian)
  * [Installation on Mac OS X](#install-osx)
  * [Browser settings](#browser-settings)
  * [Development](#development)
  * [Contribute](#contribute)
  * [Localization](#localization)
  * [Other Projects](#other-projects)



# <a name="features"></a>Features

## <a name="feature-a"></a>Web Page
This apps provides a light flask app to:
* know the state of the devices;
* know informations about system;
* test communication with some devices (e.g. send a test message to the customer display, print a test ticket, etc...).

## <a name="feature-b"></a>Specific WebServices for Odoo
The aim of this sub project is to provide WebServices and Web Page to simulate the behaviour of Odoo Apps (hw_proxy applications & co) to allow Odoo users to use Odoo Point of Sale with PyWebDriver as a Proxy.
* **Odoo8**:
  * **Printers** :
    * Epson TM-T20
  * **Credit Card Reader**:
    * Ingenico and Sagem credit card readers with Telium Manager version 37783600 or superior
    * Ingenico i2200 check reader and writer
  * **Customer Display**:
    * Bixolon BCD-1100
    * Bixolon BCD-1000
  * **Scale**:
    * TODO : planned by GRAP (Any help welcome);
  * **Barcode Reader**, **Cash Box** :
    * Not Planned

## <a name="feature-c"></a>Generic WebServices using CUP
Done.

# <a name="customers"></a>End-Users / Customers Section
If you're interested by a feature that is not currently supported, please [contact our team](http://www.akretion.com) for a quotation.

Otherwise, if you like this project, feel free to make a donation.

# <a name="contributors"></a>Contributors
The main contributors of this project are : 
* Sylvain Le Gal <https://twitter/legalsylvain>
* Sébastien Beau <sebastien.beau@akretion.com>
* Arthur Vuillard <arthur@hashbang.fr>
* Sylvain Calador <sylvain.calador@akretion.com>

A lot of the code come from other projects. Licences and copyright are mentionned in each file or in a readme file of the folder. The main other contributors are:
* Odoo Part: **Odoo S.A.** <http://odoo.com>
* Cros Decorator for Flask: **Armin Ronacher** <http://flask.pocoo.org/snippets/56/>
* ESCPOS driver: **Manuel F Martinez** <manpaz@bashlinux.com>

# <a name="developers"></a>Developers Section

## <a name="install-debian"></a>Installation on Debian/Ubuntu
```
sudo add-apt-repository ppa:akretion-team/pywebdriver
sudo apt-get update
sudo apt-get install pywebdriver
```

## <a name="install-osx"></a>Installation on Mac OS X

Pywebdriver can be installed on Mac OS X and is successfully used in production on a Mac OS X computer with Bixolon customer display, Ingenico credit card reader and check printer. TODO: write installation instructions.


## <a name="browser-settings"></a>Browser settings

You need to confirmed security exception on your browers for the following paths: http://localhost and https://localhost

see <a href="https://support.mozilla.org/en-US/kb/what-does-your-connection-is-not-secure-mean">here</a> and click on 'Advanced' and 'confirm security exception'

## <a name="development"></a>Development

To test this module, do the following steps:
* download it from git;
```
git clone https://github.com/akretion/pywebdriver.git
```
* Install dependency by running this two command
```
sudo apt-get install cups python-cups python-pip python-netifaces
sudo pip install -r requirement.txt
```
* set correct parameters in the config/config.ini file;
* call this command:
```
   python pywebdriver.py
```
* Call the url : http://localhost:8069 (by default, but depending of your config.ini file) in a browser to see devices state;

## <a name="contribute"></a>Contribute

If you find a bug, feel free to report it and submit a bugfix. 

If you want to propose extra features not yet covered, please contact us or submit a Pull Request.

## <a name="localization"></a>Localization

For the moment, localization is managed for english and french languages. If you want to manage extra lozalisation, do the following:
* call this command to generate '.pot' file:
```
pybabel extract -F translations/settings_babel.cfg -o translations/i18n.pot .
```
* call one of the two commands to generate '.po' file:
```
pybabel init -i translations/i18n.pot -d translations -l <code>  # (First time)
pybabel update -i translations/i18n.pot -d translations          # (Next times)
```
* Edit your '.po' file and write correct translation;
* call this command to generate '.mo' file:

```
pybabel compile -d translations
```
* Change your config.ini file to test the result;
* Do a Pull Request to share your work;

## <a name="other-projects"></a>Other Projects
If you're interested by this project, you could perhaps take a look at these other projects:
* [Odoo](https://github.com/odoo/odoo)
* [OCA pos](https://github.com/OCA/pos)
* [OpenERP-ledDisplay](https://github.com/guerrerocarlos/OpenERP-ledDisplay)
* [ProxyPoS](https://github.com/Fedrojesa/ProxyPoS/)


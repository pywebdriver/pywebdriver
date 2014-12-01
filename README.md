pywebdriver
===========

Summary
-------
Python Web Services to communicate wih Devices.

The aim of this project is to make easier communication between application and Devices, providing light WebServices based on Python-Flask libraries. The software can be installed on a computer or a Raspberry-like device. It is compatible with Linux distribution.

Table of Content
----------------
* [Features](#features)
  * [Specific WebServices for Odoo](#feature-a)
  * [Generic WebServices using CUP](#feature-b)
* [End-Users / Customers Section](#customers)
* [Contributors](#contributors) 
* [Developers Section](#developers)
  * [Deployment](#deployment)
  * [Contribute](#contribute)
  * [Localization](#localization)
  * [Other Projects](#other-projects)



# <a name="features"></a>Features

## <a name="feature-a"></a>Specific WebServices for Odoo
The aim of this sub project is provide WebServices and Web Page to simulate the behaviour of Odoo Apps (hw_proxy applications & co) to allow Odoo users to use Odoo Point of Sale with PyWebDriver as a Proxy.
* **State** (depending of devices type):
 * **Printers** : To be released for 7.0 and 8.0 Series;
 * **Scale**, **Barcode Reader**, **Cash Box**, **Credit Carte Reader** : Not Planned;
* **Compatibility** : Odoo 7.0; Odoo 8.0;

## <a name="feature-b"></a>Generic WebServices using CUP
* **State** : Planned;

# <a name="customers"></a>End-Users / Customers Section
If a you're interested by a feature that is not currently supported, please [contact our team](http://www.akretion.com) for a quotation.

Otherwise, if you like this project, feel free to make a donation.

# <a name="contributors"></a>Contributors
The main contributors of this project are : 
* Sylvain Le Gal <https://twitter/legalsylvain>
* Sébastien Beau <sebastien.beau@akretion.com>
* Arthur Vuillard <arthur@hashbang.fr>

A lot of the code come from other projects. Licences and copyright are mentionned in each file or in a readme file of the folder. The main other contributors are: 
* Odoo Part: **Odoo S.A.** <http://odoo.com>
* Cros Decorator for Flask: **Armin Ronacher** <http://flask.pocoo.org/snippets/56/>
* ESCPOS driver: **Manuel F Martinez** <manpaz@bashlinux.com>

# <a name="developers"></a>Developers Section

## <a name="deployment"></a>Deployment

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

for the moment, localization is managed for english and french languages. If you want to manage extra lozalisation, do the following step:
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
If you're interested by this project, you could perhaps take a look on this others projects:
* [Odoo](https://github.com/odoo/odoo)
* [OpenERP-ledDisplay](https://github.com/guerrerocarlos/OpenERP-ledDisplay)
* [ProxyPoS](https://github.com/Fedrojesa/ProxyPoS/)


pywebdriver
===========

Summary
-------
Python Web Services to communicate wih Devices.

The aim of this project is to make more easy communication between application and Devices, providing light WebServices based on Python-Flask librairies. The software can be installed on a computer or a Raspberry-like device. It is compatible with Linux distribution.

Table of Content
----------------
* [End-Users / Customers Section](#customers)
* [Features](#features)
  * [Specific WebServices for Odoo](#feature-a)
  * [Generic WebServices using CUP](#feature-b)
* [Contributors](#contributors) 
* [Developers Section](#developers)
  * [Deployment](#deployment)
  * [Contribute](#contribute)
  * [Localization](#localization)

# <a name="customers"></a>End-Users / Customers Section


# <a name="features"></a>Features

## <a name="feature-a"></a>Specific WebServices for Odoo
* **Main State** : To be released;
* **Compatibility** : Odoo 7.0; Odoo 8.0;
The aim of this sub project is provide WebServices and Web Page to simulate the behaviour of Odoo Apps (hw_proxy applications & co) to allow Odoo users to use Odoo Point of Sale with PyWebDriver. 
State of the project depending of devices type :
* **Printers** : To be release for 7.0 and 8.0 Series;
* **Scale**, **Barcode Reader**, **Cash Box**, **Credit Carte Reader** : Not Planned;

## <a name="feature-b"></a>Generic WebServices using CUP
* **Main State** : Planned;

# <a name="contributors"></a>Contributors
The main contributors of this project are : 
* Sylvain Le Gal <https://twitter/legalsylvain>
* Sébastien Beau <sebastien.beau@akretion.com>
* Arthur Vuillard <arthur@hashbang.fr>

A lot of the code come from other projects. Licences and copyright are mentionned in each file or in a readme file of the current folder. The main other contributors : 
* For the Odoo Part : **Odoo S.A.** <http://odoo.com>
* For the Cros Decorator for Flask : **Armin Ronacher** <http://flask.pocoo.org/snippets/56/>
* for the ESCPOS driver : **Manuel F Martinez** <manpaz@bashlinux.com>

# <a name="developers"></a>Developers Section

## <a name="deployment"></a>Deployment

To test this module, do the following steps : 
* download it from git;
* set correct parameters in the config/config.ini file;
* call this command:
```
   python pywebdriver.py
```
* Call the url : http://localhost:8237 (by default, but depending of your config.ini file) in a browser to see devices state;

## <a name="contribute"></a>Contribute

If you find a bug, feel free to report it and submit a bugfix. 

If you want to propose extra features not yet covered, please contact us or submit a Pull Request.

## <a name="localization"></a>Localization

Localization is managed for english and french languages only for the moment. If you want to manage extra lozalisation, do the following step:
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

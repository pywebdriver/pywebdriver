To Manage translation
=====================

Generate template '.pot' file
-----------------------------
pybabel extract -F translations/settings_babel.cfg -o translations/i18n.pot .

First time - Generate '.po' files
---------------------------------
pybabel init -i translations/i18n.pot -d translations -l fr

Update time - Generate '.po' files
----------------------------------
pybabel update -i translations/i18n.pot -d translations


Generate '.mo' file
-------------------
pybabel compile -d translations

# To Manage translation

# Generate Or update template '.pot' file
pybabel extract -F translations/settings_babel.cfg -o translations/i18n.pot .

# Generate '.po' file for the first time
pybabel init -i translations/i18n.pot -d translations -l fr

# Update 'pot' file
pybabel extract -F translations/settings_babel.cfg -o translations/i18n.pot .
# Update all 'po' files
pybabel update -i translations/i18n.pot -d translations

# Generate '.mo' file for use
pybabel compile -d translations

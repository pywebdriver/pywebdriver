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
./build_ubuntu.sh [version]
```

Example:

```bash
./build_ubuntu.sh 24.04
```

if you want to install the generated package, run:

```
sudo apt-get  install ./build/pywebdriver_20230809_amd64.deb
```

## Windows Configurator Translations

The Windows configurator uses a simple JSON-based translation system.

### Translation Files

- **JSON Files**: `windows/configurator/web/locales/*.json` - Browser-consumable
  translations
- **PO Files**: `windows/configurator/i18n/*.po` - Optional for professional translators

### How It Works

English strings in the code are the source of truth for both JavaScript and Python.

**JavaScript:** Uses `t("English string")` calls in `app.js`.

**Python:**

- For data sent to frontend (like `drivers_meta.py` labels/descriptions): Use English
  strings directly. These are translated by the frontend via `t()`.
- For Python-specific messages (error messages, print statements): Use
  `_("English string")` from `i18n.py`.

The `en.json` file is a template with empty string values (like a POT file). Other
language files (es.json, fr.json, etc.) have the same keys with translated values.

If a key is missing in a language file, the English string (the key itself) is used as
fallback.

### Adding a New Language

1. **Copy en.json** as a starting point:

   ```bash
   cp windows/configurator/web/locales/en.json windows/configurator/web/locales/ll.json
   ```

2. **Translate the JSON file** by editing the values (keep keys unchanged).

3. **Update the PyInstaller spec** (`windows/pywebdriver.spec`) to include the new JSON
   file:

   ```python
   datas=[
       # ... existing files ...
       ("configurator\\web\\locales\\LANG.json", "configurator_web\\locales"),
   ],
   ```

4. **Add language button** to `windows/configurator/web/index.html`:

   ```html
   <button data-lang="LANG">LANGUAGE</button>
   ```

5. **Add plural rules** to `windows/configurator/web/gettext.js` if needed:
   ```javascript
   'LANG': function (n) { /* plural logic */ },
   ```

**Optional:** For professional translators, export to PO format:

```bash
python windows/configurator/i18n/generate_pot.py --export-po
```

### Updating Translations

When adding or changing translation strings in the code:

**For JavaScript:**

1. **Add or update the English string** in `app.js`:
   ```javascript
   t("Your new English text here");
   ```

**For Python:**

1. **Add or update the English string** in `drivers_meta.py`:

   ```python
   "label": "Your new English text here",
   "description": "Your description here",
   ```

2. **Extract strings to en.json and sync to all language files**:

   ```bash
   python windows/configurator/i18n/extract_pot.py --sync
   ```

   This scans both app.js (for t() calls) and drivers_meta.py (for labels/descriptions),
   updates en.json, and adds missing keys to all language JSON files with English as
   fallback. Keys that are no longer in the code are moved to an "unused" section in the
   JSON files (preserving their translations in case they're needed later).

3. **Translate the new keys** in each language JSON file

**Optional:** If using PO files for professional translation:

```bash
python windows/configurator/i18n/generate_pot.py --export-po   # Export to PO
# ... translate PO files ...
python windows/configurator/i18n/generate_pot.py --import-po   # Import back to JSON
```

### Supported Languages

Currently supported languages:

- English (en) - Default
- Spanish (es)
- French (fr)

#!/usr/bin/env python3
"""Simplify translation management for the configurator.

English strings in the code (app.js t() calls) are the source of truth.
en.json mirrors these strings as keys. Other language files should have
all keys from en.json, with English as fallback for untranslated strings.

Usage:
    python generate_pot.py --sync       # Sync new keys from en.json to all languages
    python generate_pot.py --export-po  # Export all languages to PO files
    python generate_pot.py --import-po  # Import from PO files to JSON
"""

import argparse
import json
import os

import polib

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "web", "locales")
I18N_DIR = SCRIPT_DIR
EN_JSON = os.path.join(JSON_DIR, "en.json")


def sync_keys():
    """Sync new keys from en.json to all other language JSON files."""
    with open(EN_JSON, "r", encoding="utf-8") as f:
        en_data = json.load(f)

    json_files = [
        f for f in os.listdir(JSON_DIR) if f.endswith(".json") and f != "en.json"
    ]

    for json_file in json_files:
        json_path = os.path.join(JSON_DIR, json_file)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Add missing keys with English fallback (key itself is the English text)
        updated = False
        for key in en_data.keys():
            if key == "":
                continue
            if key not in data:
                data[key] = key  # English fallback is the key itself
                updated = True

        if updated:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated: {json_file}")

    print(f"Synced {len(json_files)} language files from en.json")


def export_to_po():
    """Export all JSON files to PO format for translators."""
    with open(EN_JSON, "r", encoding="utf-8") as f:
        en_data = json.load(f)

    json_files = [
        f for f in os.listdir(JSON_DIR) if f.endswith(".json") and f != "en.json"
    ]

    for json_file in json_files:
        lang_code = os.path.splitext(json_file)[0]
        json_path = os.path.join(JSON_DIR, json_file)
        po_path = os.path.join(I18N_DIR, f"{lang_code}.po")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        po = polib.POFile()
        po.metadata = {
            "Project-Id-Version": "PyWebDriver Configurator",
            "Report-Msgid-Bugs-To": "",
            "POT-Creation-Date": "",
            "PO-Revision-Date": "",
            "Last-Translator": "",
            "Language-Team": "",
            "Language": lang_code,
            "MIME-Version": "1.0",
            "Content-Type": "text/plain; charset=UTF-8",
            "Content-Transfer-Encoding": "8bit",
        }

        for key in en_data.keys():
            if key == "":
                continue
            entry = polib.POEntry(msgid=key, msgstr=data.get(key, ""))
            po.append(entry)

        po.save(po_path)
        print(f"Exported: {po_path}")

    print(f"Exported {len(json_files)} languages to PO format")


def import_from_po():
    """Import PO files back to JSON format."""
    with open(EN_JSON, "r", encoding="utf-8") as f:
        en_data = json.load(f)

    po_files = [f for f in os.listdir(I18N_DIR) if f.endswith(".po")]

    for po_file in po_files:
        lang_code = os.path.splitext(po_file)[0]
        po_path = os.path.join(I18N_DIR, po_file)
        json_path = os.path.join(JSON_DIR, f"{lang_code}.json")

        po = polib.pofile(po_path)

        json_data = {
            "": {"lang": lang_code, "plural-forms": "nplurals=2; plural=(n != 1);"}
        }

        for entry in po:
            if entry.msgid:
                json_data[entry.msgid] = entry.msgstr or en_data.get(
                    entry.msgid, entry.msgid
                )

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)

        print(f"Imported: {json_path}")

    print(f"Imported {len(po_files)} languages from PO format")


def main():
    parser = argparse.ArgumentParser(description="Manage configurator translations")
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Sync new keys from en.json to all languages",
    )
    parser.add_argument(
        "--export-po", action="store_true", help="Export all languages to PO files"
    )
    parser.add_argument(
        "--import-po", action="store_true", help="Import from PO files to JSON"
    )
    args = parser.parse_args()

    if args.sync:
        sync_keys()
    elif args.export_po:
        export_to_po()
    elif args.import_po:
        import_from_po()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

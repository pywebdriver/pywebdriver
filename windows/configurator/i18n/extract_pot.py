#!/usr/bin/env python3
"""Extract translation strings from app.js and Python files to generate en.json.

This script scans app.js for t() calls and Python files for translatable strings,
then extracts the English strings to create an en.json template file with empty
string values (like a POT file).

Usage:
    python extract_pot.py          # Extract to en.json only
    python extract_pot.py --sync   # Extract and sync to all language files
"""

import argparse
import json
import os
import re

# Paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
APP_JS = os.path.join(os.path.dirname(SCRIPT_DIR), "web", "app.js")
CONFIG_DIR = os.path.dirname(SCRIPT_DIR)
JSON_DIR = os.path.join(os.path.dirname(SCRIPT_DIR), "web", "locales")
EN_JSON = os.path.join(JSON_DIR, "en.json")


def extract_strings_from_js(js_file):
    """Extract all t() call strings from JavaScript file."""
    with open(js_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Match t("string") and t('string') patterns
    # Handle both single and double quotes
    pattern = r't\(["\']([^"\']+)["\']\)'
    matches = re.findall(pattern, content)

    # Also handle multiline strings with string concatenation
    # t("string" + "string")
    concat_pattern = r't\(["\']([^"\']+)["\']\s*\+\s*["\']([^"\']+)["\']\)'
    concat_matches = re.findall(concat_pattern, content)
    for match in concat_matches:
        matches.append("".join(match))

    return sorted(set(matches))


def extract_strings_from_python(config_dir):
    """Extract translatable strings from Python files (drivers_meta.py)."""
    strings = set()

    # Scan drivers_meta.py for label and description strings
    drivers_meta = os.path.join(config_dir, "drivers_meta.py")
    if os.path.exists(drivers_meta):
        with open(drivers_meta, "r", encoding="utf-8") as f:
            content = f.read()

        # Match "label": "string" and "description": "string" patterns
        label_pattern = r'"label":\s*"([^"]+)"'
        desc_pattern = r'"description":\s*"([^"]+)"'

        strings.update(re.findall(label_pattern, content))
        strings.update(re.findall(desc_pattern, content))

    return sorted(strings)


def generate_pot_json(strings, output_file):
    """Generate en.json with empty string values."""
    en_data = {"": {"lang": "en", "plural-forms": "nplurals=2; plural=(n != 1);"}}

    for string in strings:
        en_data[string] = ""

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(en_data, f, indent=2, ensure_ascii=False)

    print(f"Generated {output_file} with {len(strings)} strings")


def sync_to_languages(en_data):
    """Sync en.json keys to all other language JSON files."""
    json_files = [
        f for f in os.listdir(JSON_DIR) if f.endswith(".json") and f != "en.json"
    ]

    for json_file in json_files:
        json_path = os.path.join(JSON_DIR, json_file)
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = False

        # Preserve existing unused section
        unused_data = data.get("unused", {})

        # Identify and move unused keys to "unused" section
        for key in list(data.keys()):
            if key == "" or key == "unused":
                continue
            if key not in en_data:
                # Preserve the translation before deleting
                unused_data[key] = data[key]
                del data[key]
                updated = True

        # Add missing keys with English fallback (key itself is the English text)
        for key in en_data.keys():
            if key == "":
                continue
            if key not in data:
                data[key] = key  # English fallback is the key itself
                updated = True

        # Store unused keys in a special section if any
        if unused_data:
            data["unused"] = unused_data
            updated = True

        if updated:
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            print(f"Updated: {json_file}")

    print(f"Synced {len(json_files)} language files from en.json")


def main():
    parser = argparse.ArgumentParser(
        description="Extract translation strings from app.js and Python files"
    )
    parser.add_argument(
        "--sync",
        action="store_true",
        help="Sync to all language files after extracting",
    )
    args = parser.parse_args()

    # Extract from both JavaScript and Python
    js_strings = extract_strings_from_js(APP_JS)
    py_strings = extract_strings_from_python(CONFIG_DIR)
    all_strings = sorted(set(js_strings + py_strings))

    generate_pot_json(all_strings, EN_JSON)
    print(f"Extracted {len(all_strings)} unique translation strings")
    print(f"  - {len(js_strings)} from JavaScript")
    print(f"  - {len(py_strings)} from Python")

    if args.sync:
        with open(EN_JSON, "r", encoding="utf-8") as f:
            en_data = json.load(f)
        sync_to_languages(en_data)


if __name__ == "__main__":
    main()

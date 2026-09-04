#!/usr/bin/env python3
#//// Neoffice — added file (no upstream equivalent): one-off script that
#//// replays the TRANSLATIONS / CRM_TERMS dictionaries of translate_po.py onto
#//// crm/locale/fr.po. It hardcodes /Users/jeremy/GitHub/crm, so it only ever ran on
#//// one machine, and it rewrites the PO by regex instead of going through
#//// bench generate-pot-file / update-po-files / compile-po-to-mo. It is not
#//// imported by the app: nothing but apply_translations.py reads it.
#//// TO REVIEW: origin unknown — commit 5afea979 ("Remove pre-built frontend assets and auto-build workflow")
#//// added it at the repo root without saying why, so it ships to every
#//// instance with the app. Delete rather than merge.
"""
Apply all available translations to the fr.po file
"""
import re

# Import translations from translate_po
import sys
sys.path.insert(0, '/Users/jeremy/GitHub/crm')
from translate_po import TRANSLATIONS, CRM_TERMS

def apply_translations(filepath):
    """Apply all available translations to the PO file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    output_lines = []
    i = 0
    translated_count = 0

    while i < len(lines):
        line = lines[i]

        # Check if this is a msgid line (not the empty header msgid)
        if line.startswith('msgid "') and line != 'msgid ""':
            # Extract msgid text
            msgid_match = re.match(r'msgid "(.*)"\s*$', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)

                # Add the msgid line
                output_lines.append(line)
                i += 1

                # Check if next line is msgstr
                if i < len(lines) and lines[i].startswith('msgstr'):
                    msgstr_line = lines[i]

                    # Check if msgstr is empty
                    if msgstr_line == 'msgstr ""':
                        # Try to find translation
                        translation = None

                        # Check direct translations
                        if msgid_text in TRANSLATIONS:
                            translation = TRANSLATIONS[msgid_text]
                        elif msgid_text in CRM_TERMS:
                            translation = CRM_TERMS[msgid_text]

                        if translation:
                            output_lines.append(f'msgstr "{translation}"')
                            translated_count += 1
                        else:
                            output_lines.append(msgstr_line)
                    else:
                        output_lines.append(msgstr_line)

                    i += 1
                else:
                    # No msgstr found, just continue
                    pass
            else:
                output_lines.append(line)
                i += 1
        else:
            output_lines.append(line)
            i += 1

    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Applied {translated_count} translations")
    return translated_count

if __name__ == '__main__':
    po_file = '/Users/jeremy/GitHub/crm/crm/locale/fr.po'
    count = apply_translations(po_file)
    print(f"\nTotal translations applied: {count}")

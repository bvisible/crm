#!/usr/bin/env python3
#//// Neoffice — added file (no upstream equivalent): one-off script that
#//// extracts the untranslated entries of, and prepares an MCP batch for,
#//// crm/locale/fr.po. It hardcodes /Users/jeremy/GitHub/crm, so it only ever ran on
#//// one machine, and it rewrites the PO by regex instead of going through
#//// bench generate-pot-file / update-po-files / compile-po-to-mo. It is not
#//// imported by the app: nothing but apply_translations.py reads it.
#//// TO REVIEW: origin unknown — commit 5afea979 ("Remove pre-built frontend assets and auto-build workflow")
#//// added it at the repo root without saying why, so it ships to every
#//// instance with the app. Delete rather than merge.
"""
Extract untranslated entries and prepare them for translation via MCP
"""
import json
import subprocess

# Run MCP analysis
result = subprocess.run([
    'mcp', 'analyze_po_file',
    '--po_file_path', '/Users/jeremy/GitHub/crm/crm/locale/fr.po',
    '--locale', 'fr'
], capture_output=True, text=True)

data = json.loads(result.stdout)

print(f"Total: {data['statistics']['total']}")
print(f"Translated: {data['statistics']['translated']}")
print(f"Untranslated: {data['statistics']['untranslated']}")
print(f"\nFirst 20 untranslated entries:")

for i, entry in enumerate(data['untranslated_entries'][:20]):
    print(f"\n{i+1}. msgid: {entry['msgid'][:100]}")
    print(f"   reference: {entry['reference']}")

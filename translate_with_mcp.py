#!/usr/bin/env python3
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

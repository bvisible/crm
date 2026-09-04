#!/usr/bin/env python3
#//// Neoffice — added file (no upstream equivalent): one-off script that
#//// applies the last hand-written batch of strings to
#//// crm/locale/fr.po. It hardcodes /Users/jeremy/GitHub/crm, so it only ever ran on
#//// one machine, and it rewrites the PO by regex instead of going through
#//// bench generate-pot-file / update-po-files / compile-po-to-mo. It is not
#//// imported by the app: nothing but apply_translations.py reads it.
#//// TO REVIEW: origin unknown — commit 5afea979 ("Remove pre-built frontend assets and auto-build workflow")
#//// added it at the repo root without saying why, so it ships to every
#//// instance with the app. Delete rather than merge.
"""
Translate the last remaining untranslated strings in fr.po
"""
import re

# Last batch of translations
TRANSLATIONS = {
    '<p>Dear {{ lead_name }},</p>\\n\\n<p>This is a reminder for the payment of {{ grand_total }}.</p>\\n\\n<p>Thanks,</p>\\n<p>Frappé</p>': '<p>Cher {{ lead_name }},</p>\\n\\n<p>Ceci est un rappel pour le paiement de {{ grand_total }}.</p>\\n\\n<p>Merci,</p>\\n<p>Frappé</p>',
    'Automatically update "Expected Deal Value" based on the total value of associated products in a deal': 'Mettre à jour automatiquement "Valeur attendue de l\'affaire" en fonction de la valeur totale des produits associés dans une affaire',
    'Dear {{ lead_name }}, \\n\\nThis is a reminder for the payment of {{ grand_total }}. \\n\\nThanks, \\nFrappé': 'Cher {{ lead_name }}, \\n\\nCeci est un rappel pour le paiement de {{ grand_total }}. \\n\\nMerci, \\nFrappé',
    'File "{0}" was skipped because of invalid file type': 'Le fichier "{0}" a été ignoré en raison d\'un type de fichier invalide',
    'File "{0}" was skipped because only {1} uploads are allowed': 'Le fichier "{0}" a été ignoré car seulement {1} téléchargements sont autorisés',
    'File "{0}" was skipped because only {1} uploads are allowed for DocType "{2}"': 'Le fichier "{0}" a été ignoré car seulement {1} téléchargements sont autorisés pour le DocType "{2}"',
    'Hi John, \\n\\nCan you please provide more details on this...': 'Bonjour John, \\n\\nPouvez-vous fournir plus de détails à ce sujet...',
    'It will make deal\'s "Expected Closure Date" & "Expected Deal Value" mandatory to get accurate forecasting insights': 'Cela rendra obligatoires la "Date de clôture attendue" et la "Valeur attendue de l\'affaire" pour obtenir des prévisions précises',
    'Lost notes are required when lost reason is "Other"': 'Les notes de perte sont requises lorsque la raison de perte est "Autre"',
    'Makes "Expected Closure Date" and "Expected Deal Value" mandatory for deal value forecasting': 'Rend obligatoires la "Date de clôture attendue" et la "Valeur attendue de l\'affaire" pour la prévision de la valeur des affaires',
    'Sync Successful, CRM Lead: ${frappe.utils.get_form_link("CRM Lead", message.name, true)}!': 'Synchronisation réussie, Prospect CRM : ${frappe.utils.get_form_link("CRM Lead", message.name, true)} !',
    'The rate used to convert the deal\'s currency to your crm\'s base currency (set in CRM Settings). It is set once when the currency is first added and doesn\'t change automatically.': 'Le taux utilisé pour convertir la devise de l\'affaire en devise de base de votre CRM (défini dans les Paramètres CRM). Il est défini une fois lorsque la devise est ajoutée pour la première fois et ne change pas automatiquement.',
    'The rate used to convert the organization\'s currency to your crm\'s base currency (set in CRM Settings). It is set once when the currency is first added and doesn\'t change automatically.': 'Le taux utilisé pour convertir la devise de l\'organisation en devise de base de votre CRM (défini dans les Paramètres CRM). Il est défini une fois lorsque la devise est ajoutée pour la première fois et ne change pas automatiquement.',
    '⚠️ Avoid using "trigger" as a field name — it conflicts with the built-in trigger() method.': '⚠️ Évitez d\'utiliser "trigger" comme nom de champ — cela entre en conflit avec la méthode trigger() intégrée.',
    '⚠️ Method "{0}" not found in class.': '⚠️ Méthode "{0}" introuvable dans la classe.',
    '⚠️ No class found for doctype: {0}, it is mandatory to have a class for the parent doctype. it can be empty, but it should be present.': '⚠️ Aucune classe trouvée pour le doctype : {0}, il est obligatoire d\'avoir une classe pour le doctype parent. Elle peut être vide, mais elle doit être présente.',
    '⚠️ No data found for parent field: {0}': '⚠️ Aucune donnée trouvée pour le champ parent : {0}',
    '⚠️ No row found for idx: {0} in parent field: {1}': '⚠️ Aucune ligne trouvée pour idx : {0} dans le champ parent : {1}',
}

def translate_po_file():
    """Apply translations to the fr.po file"""
    po_file = '/Users/jeremy/GitHub/crm/crm/locale/fr.po'

    with open(po_file, 'r', encoding='utf-8') as f:
        content = f.read()

    translated_count = 0

    for msgid, msgstr in TRANSLATIONS.items():
        # Escape special regex characters but preserve our placeholders
        escaped_msgid = re.escape(msgid)

        # Pattern to match the msgid and empty msgstr
        pattern = f'msgid "{escaped_msgid}"\\nmsgstr ""'
        replacement = f'msgid "{msgid}"\\nmsgstr "{msgstr}"'

        if pattern in content:
            content = content.replace(pattern, replacement)
            translated_count += 1

    with open(po_file, 'w', encoding='utf-8') as f:
        f.write(content)

    return translated_count

if __name__ == '__main__':
    print("Applying last batch of translations...")
    count = translate_po_file()
    print(f"\nTranslated {count} strings")

    # Check remaining
    import subprocess
    result = subprocess.run(
        ['grep', '-c', 'msgstr ""', '/Users/jeremy/GitHub/crm/crm/locale/fr.po'],
        capture_output=True,
        text=True
    )
    remaining = int(result.stdout.strip()) - 1  # Subtract 1 for the header msgstr ""
    print(f"Remaining untranslated: {remaining}")

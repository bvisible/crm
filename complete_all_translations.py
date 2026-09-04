#!/usr/bin/env python3
#//// Neoffice — added file (no upstream equivalent): one-off script that
#//// applies a ~300-entry hand-written French dictionary to the empty msgstr of
#//// crm/locale/fr.po. It hardcodes /Users/jeremy/GitHub/crm, so it only ever ran on
#//// one machine, and it rewrites the PO by regex instead of going through
#//// bench generate-pot-file / update-po-files / compile-po-to-mo. It is not
#//// imported by the app: nothing but apply_translations.py reads it.
#//// TO REVIEW: origin unknown — commit 5afea979 ("Remove pre-built frontend assets and auto-build workflow")
#//// added it at the repo root without saying why, so it ships to every
#//// instance with the app. Delete rather than merge.
"""
Complete ALL French translations in fr.po file using comprehensive dictionary
"""
import re
import html

# Massive comprehensive translation dictionary
COMPREHENSIVE_TRANSLATIONS = {
    # Meta and UI elements
    "<b>META</b>": "<b>META</b>",
    "<b>SHORTCUTS</b>": "<b>RACCOURCIS</b>",
    "<span class=\"h5\"><b>PORTAL</b></span>": "<span class=\"h5\"><b>PORTAIL</b></span>",

    # Common actions and verbs
    "Accept": "Accepter",
    "Accept Invitation": "Accepter l'invitation",
    "Accept call": "Accepter l'appel",
    "Accepted": "Accepté",
    "Accepted At": "Accepté le",
    "Access Denied": "Accès refusé",
    "Access key": "Clé d'accès",
    "Access key for Exchangerate Host. Required for fetching exchange rates.": "Clé d'accès pour Exchangerate Host. Requise pour récupérer les taux de change.",
    "Access token is required": "Le jeton d'accès est requis",
    "Account SID": "SID du compte",
    "Account name is required": "Le nom du compte est requis",
    "Add Account": "Ajouter un compte",
    "Add Assignee": "Ajouter un assigné",
    "Add Existing User": "Ajouter un utilisateur existant",
    "Add Field": "Ajouter un champ",
    "Add Lead or Deal": "Ajouter un prospect ou une affaire",
    "Add Row": "Ajouter une ligne",
    "Add Sort": "Ajouter un tri",
    "Add Tab": "Ajouter un onglet",
    "Add a condition": "Ajouter une condition",
    "Add a name for your source": "Ajouter un nom pour votre source",
    "Add a task": "Ajouter une tâche",
    "Add chart": "Ajouter un graphique",
    "Add column": "Ajouter une colonne",
    "Add condition": "Ajouter une condition",
    "Add condition group": "Ajouter un groupe de conditions",
    "Add description...": "Ajouter une description...",
    "Add existing system users to this CRM. Assign them a role to grant access with their current credentials.": "Ajouter des utilisateurs système existants à ce CRM. Attribuez-leur un rôle pour leur accorder l'accès avec leurs identifiants actuels.",
    "Add filter": "Ajouter un filtre",
    "Add note": "Ajouter une note",
    "Add sample data": "Ajouter des données d'exemple",
    "Add svg code or use feather icons e.g 'settings'": "Ajouter du code svg ou utiliser les icônes feather ex: 'settings'",
    "Add task": "Ajouter une tâche",
    "Add your first comment": "Ajouter votre premier commentaire",
    "Add, edit, and manage email templates for various CRM communications": "Ajouter, modifier et gérer les modèles d'e-mail pour diverses communications CRM",
    "Add, edit, and manage sources for automatic lead syncing to your CRM": "Ajouter, modifier et gérer les sources pour la synchronisation automatique des prospects vers votre CRM",
    "Agent is unavailable to take the call, please call after some time.": "L'agent n'est pas disponible pour prendre l'appel, veuillez rappeler plus tard.",
    "All day": "Toute la journée",
    "Amount after discount": "Montant après remise",
    "An error occurred": "Une erreur s'est produite",
    "An error occurred while updating the document": "Une erreur s'est produite lors de la mise à jour du document",
    "API Key is required": "La clé API est requise",
    "API Token": "Jeton API",
    "A lead sync source is already enabled for this Facebook Lead Form!": "Une source de synchronisation de prospects est déjà activée pour ce formulaire Facebook Lead !",
    "@John, can you please check this?": "@John, peux-tu vérifier ceci ?",

    # Template strings (keep placeholders)
    "<p>Dear {{ lead_name }},</p>\\n\\n<p>This is a reminder for the payment of {{ grand_total }}.</p>\\n\\n<p>Thanks,</p>\\n<p>Frappé</p>": "<p>Cher(e) {{ lead_name }},</p>\\n\\n<p>Ceci est un rappel pour le paiement de {{ grand_total }}.</p>\\n\\n<p>Merci,</p>\\n<p>Frappé</p>",
}

def smart_translate(text):
    """
    Intelligent translation function that handles various cases
    """
    if not text or text.strip() == '':
        return ''

    # Direct lookup
    if text in COMPREHENSIVE_TRANSLATIONS:
        return COMPREHENSIVE_TRANSLATIONS[text]

    # Common patterns
    translations_map = {
        # Actions with objects
        "Add ": "Ajouter ",
        "Edit ": "Modifier ",
        "Delete ": "Supprimer ",
        "Remove ": "Retirer ",
        "Create ": "Créer ",
        "Update ": "Mettre à jour ",
        "View ": "Voir ",
        "Show ": "Afficher ",
        "Hide ": "Masquer ",
        "Clear ": "Effacer ",
        "Reset ": "Réinitialiser ",
        "Save ": "Enregistrer ",
        "Cancel ": "Annuler ",
        "Close ": "Fermer ",
        "Open ": "Ouvrir ",
        "Select ": "Sélectionner ",
        "Choose ": "Choisir ",
        "Upload ": "Télécharger ",
        "Download ": "Télécharger ",
        "Export ": "Exporter ",
        "Import ": "Importer ",
        "Search ": "Rechercher ",
        "Filter ": "Filtrer ",
        "Sort ": "Trier ",
        "Group ": "Grouper ",
        "Copy ": "Copier ",
        "Paste ": "Coller ",
        "Cut ": "Couper ",
        "Duplicate ": "Dupliquer ",
        "Clone ": "Cloner ",
        "Move ": "Déplacer ",
        "Rename ": "Renommer ",
        "Archive ": "Archiver ",
        "Restore ": "Restaurer ",
        "Enable ": "Activer ",
        "Disable ": "Désactiver ",
        "Activate ": "Activer ",
        "Deactivate ": "Désactiver ",
        "Publish ": "Publier ",
        "Unpublish ": "Dépublier ",
        "Lock ": "Verrouiller ",
        "Unlock ": "Déverrouiller ",
        "Approve ": "Approuver ",
        "Reject ": "Rejeter ",
        "Accept ": "Accepter ",
        "Decline ": "Refuser ",
        "Submit ": "Soumettre ",
        "Send ": "Envoyer ",
        "Receive ": "Recevoir ",
        "Forward ": "Transférer ",
        "Reply ": "Répondre ",
        "Share ": "Partager ",
        "Print ": "Imprimer ",
        "Scan ": "Scanner ",
        "Convert ": "Convertir ",
        "Transform ": "Transformer ",
        "Translate ": "Traduire ",
        "Merge ": "Fusionner ",
        "Split ": "Diviser ",
        "Join ": "Joindre ",
        "Leave ": "Quitter ",
        "Enter ": "Entrer ",
        "Exit ": "Sortir ",
        "Start ": "Démarrer ",
        "Stop ": "Arrêter ",
        "Pause ": "Mettre en pause ",
        "Resume ": "Reprendre ",
        "Continue ": "Continuer ",
        "Skip ": "Ignorer ",
        "Retry ": "Réessayer ",
        "Refresh ": "Actualiser ",
        "Reload ": "Recharger ",
        "Sync ": "Synchroniser ",
        "Backup ": "Sauvegarder ",
        "Restore ": "Restaurer ",
        "Undo ": "Annuler ",
        "Redo ": "Refaire ",
        "Apply ": "Appliquer ",
        "Confirm ": "Confirmer ",
        "Verify ": "Vérifier ",
        "Validate ": "Valider ",
        "Check ": "Vérifier ",
        "Test ": "Tester ",
        "Debug ": "Déboguer ",
        "Fix ": "Corriger ",
        "Repair ": "Réparer ",
        "Optimize ": "Optimiser ",
        "Improve ": "Améliorer ",
        "Enhance ": "Améliorer ",
        "Upgrade ": "Mettre à niveau ",
        "Downgrade ": "Rétrograder ",
        "Install ": "Installer ",
        "Uninstall ": "Désinstaller ",
        "Configure ": "Configurer ",
        "Customize ": "Personnaliser ",
        "Personalize ": "Personnaliser ",
        "Assign ": "Attribuer ",
        "Unassign ": "Retirer l'attribution ",
        "Link ": "Lier ",
        "Unlink ": "Délier ",
        "Attach ": "Joindre ",
        "Detach ": "Détacher ",
        "Connect ": "Connecter ",
        "Disconnect ": "Déconnecter ",
        "Follow ": "Suivre ",
        "Unfollow ": "Ne plus suivre ",
        "Subscribe ": "S'abonner ",
        "Unsubscribe ": "Se désabonner ",
        "Mark as ": "Marquer comme ",
        "Set as ": "Définir comme ",
        "Change to ": "Changer en ",
        "Switch to ": "Basculer vers ",
        "Go to ": "Aller à ",
        "Navigate to ": "Naviguer vers ",
        "Redirect to ": "Rediriger vers ",
        "Load ": "Charger ",
        "Unload ": "Décharger ",
        "Fetch ": "Récupérer ",
        "Retrieve ": "Récupérer ",
        "Get ": "Obtenir ",
        "Set ": "Définir ",
        "Put ": "Mettre ",
        "Post ": "Publier ",
        "Patch ": "Corriger ",
        "Process ": "Traiter ",
        "Execute ": "Exécuter ",
        "Run ": "Exécuter ",
        "Build ": "Construire ",
        "Compile ": "Compiler ",
        "Deploy ": "Déployer ",
        "Release ": "Publier ",
        "Publish ": "Publier ",
        "Generate ": "Générer ",
        "Create ": "Créer ",
        "Make ": "Créer ",
        "Produce ": "Produire ",
        "Develop ": "Développer ",
        "Design ": "Concevoir ",
        "Plan ": "Planifier ",
        "Schedule ": "Planifier ",
        "Organize ": "Organiser ",
        "Arrange ": "Organiser ",
        "Order ": "Commander ",
        "Rank ": "Classer ",
        "Rate ": "Noter ",
        "Review ": "Examiner ",
        "Evaluate ": "Évaluer ",
        "Assess ": "Évaluer ",
        "Measure ": "Mesurer ",
        "Calculate ": "Calculer ",
        "Compute ": "Calculer ",
        "Count ": "Compter ",
        "Sum ": "Additionner ",
        "Total ": "Total ",
        "Add up ": "Additionner ",
        "Subtract ": "Soustraire ",
        "Multiply ": "Multiplier ",
        "Divide ": "Diviser ",
        "Increase ": "Augmenter ",
        "Decrease ": "Diminuer ",
        "Expand ": "Développer ",
        "Collapse ": "Réduire ",
        "Minimize ": "Minimiser ",
        "Maximize ": "Maximiser ",
        "Resize ": "Redimensionner ",
        "Scale ": "Mettre à l'échelle ",
        "Zoom in": "Zoomer",
        "Zoom out": "Dézoomer",
        "Fit ": "Ajuster ",
        "Fill ": "Remplir ",
        "Empty ": "Vider ",
        "Clear all": "Tout effacer",
        "Select all": "Tout sélectionner",
        "Deselect all": "Tout désélectionner",
        "Invert selection": "Inverser la sélection",
    }

    # Try pattern matching for common prefixes
    for eng_prefix, fr_prefix in translations_map.items():
        if text.startswith(eng_prefix):
            rest = text[len(eng_prefix):]
            # Recursively translate the rest if possible
            rest_translated = smart_translate(rest) if rest else rest
            if rest_translated and rest_translated != rest:
                return fr_prefix + rest_translated

    # Common suffixes
    if text.endswith(" is required"):
        base = text[:-12]
        return f"{smart_translate(base)} est requis"

    if text.endswith(" are required"):
        base = text[:-13]
        return f"{smart_translate(base)} sont requis"

    # Return None if no translation found
    return None

def process_po_file(filepath):
    """Process the PO file and translate all empty msgstr entries."""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    translated_count = 0

    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Check for msgid line (not empty header)
        if line.startswith('msgid "') and line != 'msgid ""':
            # Extract msgid
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)
                # Unescape the string
                msgid_text = msgid_text.encode().decode('unicode_escape')

                output_lines.append(lines[i].rstrip('\n'))
                i += 1

                # Check next line for msgstr
                if i < len(lines) and lines[i].startswith('msgstr'):
                    msgstr_line = lines[i].rstrip('\n')

                    # Check if empty
                    if msgstr_line == 'msgstr ""':
                        # Try to translate
                        translation = smart_translate(msgid_text)

                        if translation:
                            # Escape the translation properly
                            translation_escaped = translation.replace('\\', '\\\\').replace('"', '\\"')
                            output_lines.append(f'msgstr "{translation_escaped}"')
                            translated_count += 1
                        else:
                            output_lines.append(msgstr_line)
                    else:
                        output_lines.append(msgstr_line)

                    i += 1
                continue

        output_lines.append(line)
        i += 1

    # Write output
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    return translated_count

if __name__ == '__main__':
    po_file = '/Users/jeremy/GitHub/crm/crm/locale/fr.po'
    print("Processing fr.po file...")
    count = process_po_file(po_file)
    print(f"\nTranslated {count} additional strings")

    # Check remaining
    import subprocess
    result = subprocess.run(['grep', '-c', 'msgstr ""', po_file], capture_output=True, text=True)
    remaining = result.stdout.strip()
    print(f"Remaining untranslated: {remaining}")

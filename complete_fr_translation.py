#!/usr/bin/env python3
"""
Complete French translation for CRM fr.po file
"""
import re

# Comprehensive translation dictionary
translations = {
    # Time expressions
    " (New)": " (Nouveau)",
    "(No title)": "(Sans titre)",
    "01/04/2024 11:30 PM": "01/04/2024 23:30",
    "1 hour ago": "Il y a 1 heure",
    "1 hr": "1 heure",
    "1 minute ago": "Il y a 1 minute",
    "1 month ago": "Il y a 1 mois",
    "1 week ago": "Il y a 1 semaine",
    "1 year ago": "Il y a 1 an",
    "2 hr": "2 heures",
    "hours ago": "Il y a {0} heures",
    "minutes ago": "Il y a {0} minutes",
    "months ago": "Il y a {0} mois",
    "weeks ago": "Il y a {0} semaines",
    "years ago": "Il y a {0} ans",
    "days ago": "Il y a {0} jours",
    "Just now": "À l'instant",
    "Today": "Aujourd'hui",
    "Yesterday": "Hier",
    "Tomorrow": "Demain",
    "Last Modified": "Dernière modification",

    # Numbers ranges
    "1-10": "1-10",
    "11-50": "11-50",
    "51-200": "51-200",
    "201-500": "201-500",
    "501-1000": "501-1000",
    "1000+": "1000+",

    # A
    "About": "À propos",
    "Actions": "Actions",
    "Active": "Actif",
    "Activities": "Activités",
    "Activity": "Activité",
    "Add": "Ajouter",
    "Add a comment": "Ajouter un commentaire",
    "Add a note": "Ajouter une note",
    "Add Call Log": "Ajouter un journal d'appel",
    "Add Comment": "Ajouter un commentaire",
    "Add Contact": "Ajouter un contact",
    "Add Deal": "Ajouter une affaire",
    "Add Email": "Ajouter un e-mail",
    "Add Filter": "Ajouter un filtre",
    "Add Lead": "Ajouter un prospect",
    "Add Link": "Ajouter un lien",
    "Add Note": "Ajouter une note",
    "Add Organization": "Ajouter une organisation",
    "Add Section": "Ajouter une section",
    "Add Task": "Ajouter une tâche",
    "Add to favorites": "Ajouter aux favoris",
    "Address": "Adresse",
    "All": "Tout",
    "All Contacts": "Tous les contacts",
    "All Deals": "Toutes les affaires",
    "All Leads": "Tous les prospects",
    "All Organizations": "Toutes les organisations",
    "All Tasks": "Toutes les tâches",
    "Amount": "Montant",
    "Annual Revenue": "Chiffre d'affaires annuel",
    "Apply": "Appliquer",
    "Apply Filter": "Appliquer le filtre",
    "Archived": "Archivé",
    "Are you sure?": "Êtes-vous sûr ?",
    "Are you sure you want to": "Êtes-vous sûr de vouloir",
    "Are you sure you want to delete": "Êtes-vous sûr de vouloir supprimer",
    "Assign": "Attribuer",
    "Assign to": "Attribuer à",
    "Assigned": "Attribué",
    "Assigned To": "Attribué à",
    "Assigned to": "Attribué à",
    "Assignment Rule": "Règle d'attribution",
    "Attachment": "Pièce jointe",
    "Attachments": "Pièces jointes",

    # B
    "Back": "Retour",
    "Birthday": "Date de naissance",
    "Browse": "Parcourir",
    "Bulk Actions": "Actions groupées",
    "Bulk Delete": "Suppression groupée",
    "Bulk Update": "Mise à jour groupée",
    "Business": "Entreprise",

    # C
    "Calendar": "Calendrier",
    "Call": "Appel",
    "Call Duration": "Durée de l'appel",
    "Call From": "Appel de",
    "Call Log": "Journal d'appel",
    "Call Logs": "Journaux d'appels",
    "Call To": "Appeler",
    "Calls": "Appels",
    "Cancel": "Annuler",
    "Change": "Modifier",
    "Change Status": "Changer le statut",
    "City": "Ville",
    "Clear": "Effacer",
    "Clear All": "Tout effacer",
    "Clear Filters": "Effacer les filtres",
    "Click to add": "Cliquer pour ajouter",
    "Click to edit": "Cliquer pour modifier",
    "Close": "Fermer",
    "Closed": "Fermé",
    "Closing Amount": "Montant de clôture",
    "Closing Date": "Date de clôture",
    "Column": "Colonne",
    "Columns": "Colonnes",
    "Comment": "Commentaire",
    "Comments": "Commentaires",
    "Company": "Société",
    "Company Name": "Nom de la société",
    "Completed": "Terminé",
    "Completed Tasks": "Tâches terminées",
    "Confirm": "Confirmer",
    "Contact": "Contact",
    "Contact Details": "Coordonnées",
    "Contact Name": "Nom du contact",
    "Contacts": "Contacts",
    "Convert": "Convertir",
    "Convert to Deal": "Convertir en affaire",
    "Country": "Pays",
    "Create": "Créer",
    "Create Call Log": "Créer un journal d'appel",
    "Create Contact": "Créer un contact",
    "Create Deal": "Créer une affaire",
    "Create Lead": "Créer un prospect",
    "Create New": "Créer nouveau",
    "Create Note": "Créer une note",
    "Create Organization": "Créer une organisation",
    "Create Task": "Créer une tâche",
    "Created": "Créé",
    "Created By": "Créé par",
    "Created On": "Créé le",
    "Creation": "Création",
    "Currency": "Devise",
    "Custom": "Personnalisé",
    "Custom Field": "Champ personnalisé",
    "Custom Fields": "Champs personnalisés",
    "Customer": "Client",

    # D
    "Dashboard": "Tableau de bord",
    "Data": "Données",
    "Date": "Date",
    "Deal": "Affaire",
    "Deal Amount": "Montant de l'affaire",
    "Deal Details": "Détails de l'affaire",
    "Deal Name": "Nom de l'affaire",
    "Deal Owner": "Propriétaire de l'affaire",
    "Deal Value": "Valeur de l'affaire",
    "Deals": "Affaires",
    "Default": "Par défaut",
    "Delete": "Supprimer",
    "Deleted": "Supprimé",
    "Description": "Description",
    "Details": "Détails",
    "Disable": "Désactiver",
    "Disabled": "Désactivé",
    "Discard": "Abandonner",
    "Discard changes": "Abandonner les modifications",
    "Document": "Document",
    "Documents": "Documents",
    "Download": "Télécharger",
    "Drag and drop": "Glisser-déposer",
    "Due": "Échéance",
    "Due Date": "Date d'échéance",
    "Duplicate": "Dupliquer",
    "Duration": "Durée",

    # E
    "Edit": "Modifier",
    "Edit Field": "Modifier le champ",
    "Email": "E-mail",
    "Email Address": "Adresse e-mail",
    "Email ID": "Adresse e-mail",
    "Email Template": "Modèle d'e-mail",
    "Emails": "E-mails",
    "Enable": "Activer",
    "Enabled": "Activé",
    "End Date": "Date de fin",
    "End Time": "Heure de fin",
    "Enter": "Entrer",
    "Enter a value": "Entrer une valeur",
    "Error": "Erreur",
    "Event": "Événement",
    "Events": "Événements",
    "Export": "Exporter",

    # F
    "Failed": "Échoué",
    "Favorite": "Favori",
    "Favorites": "Favoris",
    "Field": "Champ",
    "Field Name": "Nom du champ",
    "Field Type": "Type de champ",
    "Fields": "Champs",
    "File": "Fichier",
    "Files": "Fichiers",
    "Filter": "Filtre",
    "Filter by": "Filtrer par",
    "Filters": "Filtres",
    "First Name": "Prénom",
    "Follow Up": "Suivi",
    "Follow up": "Suivi",
    "From": "De",
    "Full Name": "Nom complet",

    # G
    "Gender": "Genre",
    "General": "Général",
    "Go": "Aller",
    "Go back": "Retour",
    "Group": "Groupe",
    "Group By": "Grouper par",

    # H
    "Help": "Aide",
    "Hide": "Masquer",
    "Hide Filters": "Masquer les filtres",
    "History": "Historique",
    "Home": "Accueil",

    # I
    "ID": "ID",
    "Icon": "Icône",
    "Image": "Image",
    "Import": "Importer",
    "In Progress": "En cours",
    "Inactive": "Inactif",
    "Incoming": "Entrant",
    "Industry": "Secteur",
    "Info": "Info",
    "Information": "Information",
    "Insert": "Insérer",
    "Invalid": "Invalide",
    "Is Archived": "Est archivé",

    # J
    "Job Title": "Poste",

    # K
    "Kanban": "Kanban",

    # L
    "Label": "Libellé",
    "Language": "Langue",
    "Last": "Dernier",
    "Last Modified": "Dernière modification",
    "Last Modified By": "Dernière modification par",
    "Last Modified On": "Modifié le",
    "Last Name": "Nom de famille",
    "Last Updated": "Dernière mise à jour",
    "Lead": "Prospect",
    "Lead Details": "Détails du prospect",
    "Lead Name": "Nom du prospect",
    "Lead Owner": "Propriétaire du prospect",
    "Lead Source": "Source du prospect",
    "Lead Status": "Statut du prospect",
    "Leads": "Prospects",
    "Link": "Lien",
    "List": "Liste",
    "List View": "Vue liste",
    "Load More": "Charger plus",
    "Loading": "Chargement",
    "Loading...": "Chargement...",
    "Location": "Emplacement",
    "Log": "Journal",
    "Logs": "Journaux",
    "Lost": "Perdu",
    "Lost Reason": "Raison de la perte",

    # M
    "Male": "Masculin",
    "Female": "Féminin",
    "Manager": "Responsable",
    "Mark as Done": "Marquer comme terminé",
    "Mark as Lost": "Marquer comme perdu",
    "Mark as Won": "Marquer comme gagné",
    "Meeting": "Réunion",
    "Meetings": "Réunions",
    "Message": "Message",
    "Mobile": "Mobile",
    "Mobile No": "N° de mobile",
    "Modified": "Modifié",
    "Modified By": "Modifié par",
    "More": "Plus",
    "Move": "Déplacer",
    "Move to": "Déplacer vers",

    # N
    "Name": "Nom",
    "New": "Nouveau",
    "New Contact": "Nouveau contact",
    "New Deal": "Nouvelle affaire",
    "New Lead": "Nouveau prospect",
    "New Organization": "Nouvelle organisation",
    "New Task": "Nouvelle tâche",
    "Next": "Suivant",
    "No": "Non",
    "No Data": "Aucune donnée",
    "No data": "Aucune donnée",
    "No items found": "Aucun élément trouvé",
    "No items to display": "Aucun élément à afficher",
    "No records found": "Aucun enregistrement trouvé",
    "No results": "Aucun résultat",
    "No results found": "Aucun résultat trouvé",
    "None": "Aucun",
    "Not Started": "Pas commencé",
    "Note": "Note",
    "Notes": "Notes",
    "Notification": "Notification",
    "Notifications": "Notifications",

    # O
    "of": "de",
    "Ok": "Ok",
    "Open": "Ouvert",
    "Open Deals": "Affaires ouvertes",
    "Open Leads": "Prospects ouverts",
    "Open Tasks": "Tâches ouvertes",
    "Opportunity": "Opportunité",
    "Options": "Options",
    "Organization": "Organisation",
    "Organization Details": "Détails de l'organisation",
    "Organization Name": "Nom de l'organisation",
    "Organizations": "Organisations",
    "Other": "Autre",
    "Others": "Autres",
    "Outgoing": "Sortant",
    "Owner": "Propriétaire",

    # P
    "Page": "Page",
    "Password": "Mot de passe",
    "Pending": "En attente",
    "Phone": "Téléphone",
    "Phone No": "N° de téléphone",
    "Phone Number": "Numéro de téléphone",
    "Pipeline": "Pipeline",
    "Please select": "Veuillez sélectionner",
    "Post": "Publier",
    "Postal Code": "Code postal",
    "Preview": "Aperçu",
    "Previous": "Précédent",
    "Primary": "Principal",
    "Priority": "Priorité",
    "Profile": "Profil",
    "Progress": "Progrès",

    # Q
    "Qualification": "Qualification",
    "Qualified": "Qualifié",
    "Quantity": "Quantité",
    "Quick Add": "Ajout rapide",
    "Quick Entry": "Saisie rapide",
    "Quote": "Devis",
    "Quotes": "Devis",

    # R
    "Recent": "Récent",
    "record": "enregistrement",
    "records": "enregistrements",
    "Refresh": "Actualiser",
    "Reload": "Recharger",
    "Remark": "Remarque",
    "Remarks": "Remarques",
    "Remove": "Supprimer",
    "Remove from favorites": "Retirer des favoris",
    "Reply": "Répondre",
    "Report": "Rapport",
    "Reports": "Rapports",
    "Required": "Obligatoire",
    "Reset": "Réinitialiser",
    "Result": "Résultat",
    "Results": "Résultats",
    "Revenue": "Chiffre d'affaires",
    "Role": "Rôle",
    "Roles": "Rôles",

    # S
    "Sales": "Ventes",
    "Sales Person": "Commercial",
    "Salutation": "Titre de civilité",
    "Save": "Enregistrer",
    "Save changes": "Enregistrer les modifications",
    "Saved": "Enregistré",
    "Search": "Rechercher",
    "Search...": "Rechercher...",
    "Section": "Section",
    "Select": "Sélectionner",
    "Select a value": "Sélectionner une valeur",
    "Select All": "Tout sélectionner",
    "Select an option": "Sélectionner une option",
    "Selected": "Sélectionné",
    "Send": "Envoyer",
    "Settings": "Paramètres",
    "Show": "Afficher",
    "Show Filters": "Afficher les filtres",
    "Show More": "Afficher plus",
    "Showing": "Affichage",
    "Sidebar": "Barre latérale",
    "Sort": "Trier",
    "Sort By": "Trier par",
    "Source": "Source",
    "Stage": "Étape",
    "Start": "Début",
    "Start Date": "Date de début",
    "Start Time": "Heure de début",
    "Started": "Commencé",
    "State": "État",
    "Status": "Statut",
    "Subject": "Sujet",
    "Submit": "Soumettre",
    "Success": "Succès",
    "Summary": "Résumé",

    # T
    "Table": "Tableau",
    "Tag": "Tag",
    "Tags": "Tags",
    "Task": "Tâche",
    "Task Details": "Détails de la tâche",
    "Tasks": "Tâches",
    "Team": "Équipe",
    "Territory": "Territoire",
    "Text": "Texte",
    "The field is required": "Le champ est obligatoire",
    "There was an error": "Une erreur s'est produite",
    "This field is required": "Ce champ est obligatoire",
    "Time": "Heure",
    "Title": "Titre",
    "To": "À",
    "Total": "Total",
    "Type": "Type",

    # U
    "Unassigned": "Non attribué",
    "Undo": "Annuler",
    "Unknown": "Inconnu",
    "Unqualified": "Non qualifié",
    "Update": "Mettre à jour",
    "Updated": "Mis à jour",
    "Upload": "Télécharger",
    "Upload File": "Télécharger un fichier",
    "User": "Utilisateur",
    "Users": "Utilisateurs",
    "Username": "Nom d'utilisateur",

    # V
    "Value": "Valeur",
    "View": "Voir",
    "View All": "Tout voir",
    "View Details": "Voir les détails",
    "View more": "Voir plus",

    # W
    "Warning": "Avertissement",
    "Website": "Site web",
    "Welcome": "Bienvenue",
    "Won": "Gagné",
    "Work": "Travail",

    # Y
    "Year": "Année",
    "Yes": "Oui",

    # Z
    "Zip": "Code postal",
    "Zip Code": "Code postal",

    # Additional phrases
    "Add a section": "Ajouter une section",
    "Add field": "Ajouter un champ",
    "Add new": "Ajouter nouveau",
    "Add row": "Ajouter une ligne",
    "All fields": "Tous les champs",
    "Are you sure you want to delete this": "Êtes-vous sûr de vouloir supprimer ceci",
    "Assigned to me": "Attribué à moi",
    "Call log created successfully": "Journal d'appel créé avec succès",
    "Click to select": "Cliquer pour sélectionner",
    "Contact created successfully": "Contact créé avec succès",
    "Deal created successfully": "Affaire créée avec succès",
    "Lead created successfully": "Prospect créé avec succès",
    "No items selected": "Aucun élément sélectionné",
    "Note created successfully": "Note créée avec succès",
    "Organization created successfully": "Organisation créée avec succès",
    "Please enter a value": "Veuillez entrer une valeur",
    "Save and close": "Enregistrer et fermer",
    "Select a date": "Sélectionner une date",
    "Select a time": "Sélectionner une heure",
    "Task created successfully": "Tâche créée avec succès",
    "This action cannot be undone": "Cette action ne peut pas être annulée",
    "Updated successfully": "Mis à jour avec succès",
}

def complete_fr_translation(input_file, output_file):
    """Complete the French translation in the PO file"""
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    translated_count = 0

    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Check if this is a msgid line
        if line.startswith('msgid "') and not line.startswith('msgid ""'):
            # Extract the msgid text
            msgid_text = line[7:-1]  # Remove 'msgid "' and trailing '"'

            # Handle multiline msgid
            full_msgid = msgid_text
            j = i + 1
            while j < len(lines) and lines[j].startswith('"') and not lines[j].startswith('msgstr'):
                full_msgid += lines[j].strip()[1:-1]  # Remove quotes
                j += 1

            # Output the msgid line(s)
            output_lines.append(line)
            for k in range(i + 1, j):
                output_lines.append(lines[k].rstrip('\n'))

            # Now check the msgstr
            if j < len(lines) and lines[j].startswith('msgstr'):
                msgstr_line = lines[j].rstrip('\n')

                # Check if msgstr is empty
                if msgstr_line == 'msgstr ""' or msgstr_line == 'msgstr ""':
                    # Try to translate
                    if full_msgid in translations:
                        output_lines.append(f'msgstr "{translations[full_msgid]}"')
                        translated_count += 1
                    else:
                        output_lines.append(msgstr_line)
                else:
                    output_lines.append(msgstr_line)

                i = j + 1
            else:
                i = j
        else:
            output_lines.append(line)
            i += 1

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    print(f"Translation complete!")
    print(f"Translated {translated_count} additional strings")
    print(f"Output written to {output_file}")

if __name__ == "__main__":
    input_file = "/Users/jeremy/GitHub/crm/crm/locale/fr.po"
    output_file = "/Users/jeremy/GitHub/crm/crm/locale/fr.po"

    complete_fr_translation(input_file, output_file)

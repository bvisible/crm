#!/usr/bin/env python3
#//// Neoffice — added file (no upstream equivalent): one-off script that
#//// applies a comprehensive French dictionary to every untranslated entry of
#//// crm/locale/fr.po. It hardcodes /Users/jeremy/GitHub/crm, so it only ever ran on
#//// one machine, and it rewrites the PO by regex instead of going through
#//// bench generate-pot-file / update-po-files / compile-po-to-mo. It is not
#//// imported by the app: nothing but apply_translations.py reads it.
#//// TO REVIEW: origin unknown — commit 5afea979 ("Remove pre-built frontend assets and auto-build workflow")
#//// added it at the repo root without saying why, so it ships to every
#//// instance with the app. Delete rather than merge.
"""
Translate ALL untranslated entries in fr.po using comprehensive dictionary
"""
import re

# Massive comprehensive CRM translation dictionary
TRANSLATIONS = {
    # Templates and HTML
    "<p>Dear {{ lead_name }},</p>\\n\\n<p>This is a reminder for the payment of {{ grand_total }}.</p>\\n\\n<p>Thanks,</p>\\n<p>Frappé</p>":
        "<p>Cher(e) {{ lead_name }},</p>\\n\\n<p>Ceci est un rappel pour le paiement de {{ grand_total }}.</p>\\n\\n<p>Merci,</p>\\n<p>Frappé</p>",
    "Dear {{ lead_name }}, \\n\\nThis is a reminder for the payment of {{ grand_total }}. \\n\\nThanks, \\nFrappé":
        "Cher(e) {{ lead_name }}, \\n\\nCeci est un rappel pour le paiement de {{ grand_total }}. \\n\\nMerci, \\nFrappé",
    "Hi John, \\n\\nCan you please provide more details on this...":
        "Bonjour John, \\n\\nPouvez-vous fournir plus de détails à ce sujet...",

    # Confirmations and questions
    "An image with 1:1 & 2:1 ratio is preferred": "Une image avec un ratio 1:1 ou 2:1 est préférée",
    "And": "Et",
    "Annual Revenue should be a number": "Le chiffre d'affaires annuel doit être un nombre",
    "Any failed lead syncs will show up here": "Toutes les synchronisations de prospects échouées apparaîtront ici",
    "Appears in the left sidebar. Recommended size is 32x32 px in PNG or SVG": "Apparaît dans la barre latérale gauche. Taille recommandée : 32x32 px en PNG ou SVG",
    "Appears next to the title in your browser tab. Recommended size is 32x32 px in PNG or ICO": "Apparaît à côté du titre dans l'onglet de votre navigateur. Taille recommandée : 32x32 px en PNG ou ICO",
    "Apply on": "Appliquer sur",
    "Apps": "Applications",
    "Are you sure you want to delete this attachment?": "Êtes-vous sûr de vouloir supprimer cette pièce jointe ?",
    "Are you sure you want to delete this contact?": "Êtes-vous sûr de vouloir supprimer ce contact ?",
    "Are you sure you want to delete this event?": "Êtes-vous sûr de vouloir supprimer cet événement ?",
    "Are you sure you want to delete this organization?": "Êtes-vous sûr de vouloir supprimer cette organisation ?",
    "Are you sure you want to delete this task?": "Êtes-vous sûr de vouloir supprimer cette tâche ?",
    "Are you sure you want to delete {0} linked item(s)?": "Êtes-vous sûr de vouloir supprimer {0} élément(s) lié(s) ?",
    "Are you sure you want to discard unsaved changes to this event?": "Êtes-vous sûr de vouloir abandonner les modifications non enregistrées de cet événement ?",
    "Are you sure you want to go back? Unsaved changes will be lost.": "Êtes-vous sûr de vouloir revenir en arrière ? Les modifications non enregistrées seront perdues.",
    "Are you sure you want to reset 'Create Quotation from CRM Deal' Form Script?": "Êtes-vous sûr de vouloir réinitialiser le script de formulaire 'Créer un devis depuis une affaire CRM' ?",
    "Are you sure you want to set the currency as {0}? This cannot be changed later.": "Êtes-vous sûr de vouloir définir la devise comme {0} ? Cela ne pourra pas être modifié ultérieurement.",
    "Are you sure you want to unlink {0} linked item(s)?": "Êtes-vous sûr de vouloir délier {0} élément(s) lié(s) ?",
    "Ask your manager to set up the Exchange Rate Provider, as default provider does not support currency conversion for {0} to {1}.": "Demandez à votre responsable de configurer le fournisseur de taux de change, car le fournisseur par défaut ne prend pas en charge la conversion de devise de {0} vers {1}.",

    # Assignment and rules
    "Assign conditions are invalid": "Les conditions d'attribution sont invalides",
    "Assignee Rules": "Règles d'attribution",
    "Assignees": "Assignés",
    "Assignment": "Attribution",
    "Assignment Schedule": "Planification d'attribution",
    "Assignment cleared successfully": "Attribution effacée avec succès",
    "Assignment condition": "Condition d'attribution",
    "Assignment rule": "Règle d'attribution",
    "Assignment rule created": "Règle d'attribution créée",
    "Assignment rule deleted": "Règle d'attribution supprimée",
    "Assignment rule duplicated": "Règle d'attribution dupliquée",
    "Assignment rule updated": "Règle d'attribution mise à jour",
    "Assignment rule {0} updated": "Règle d'attribution {0} mise à jour",
    "Assignment rules": "Règles d'attribution",
    "Assignment rules automatically assign lead/deal to the right sales user based on predefined conditions": "Les règles d'attribution attribuent automatiquement un prospect/affaire au bon commercial en fonction de conditions prédéfinies",

    # Files and attachments
    "Attach a file": "Joindre un fichier",
    "Auth Token": "Jeton d'authentification",
    "Auto Update Expected Deal Value": "Mise à jour automatique de la valeur prévisionnelle de l'affaire",
    "Auto update expected deal value": "Mise à jour automatique de la valeur prévisionnelle de l'affaire",
    "Auto update of expected deal value disabled": "Mise à jour automatique de la valeur prévisionnelle de l'affaire désactivée",
    "Auto update of expected deal value enabled": "Mise à jour automatique de la valeur prévisionnelle de l'affaire activée",
    "Automatically update \"Expected Deal Value\" based on the total value of associated products in a deal": "Met à jour automatiquement la \"Valeur prévisionnelle de l'affaire\" en fonction de la valeur totale des produits associés dans une affaire",
    "Automation & Rules": "Automatisation et règles",

    # Statistics
    "Average deal value of non won/lost deals": "Valeur moyenne des affaires en cours",
    "Average deal value of ongoing & won deals": "Valeur moyenne des affaires en cours et gagnées",
    "Average deal value of won deals": "Valeur moyenne des affaires gagnées",
    "Average time taken from deal creation to deal closure": "Temps moyen entre la création et la clôture d'une affaire",
    "Average time taken from lead creation to deal closure": "Temps moyen entre la création d'un prospect et la clôture d'une affaire",
    "Avg deal value": "Valeur moyenne des affaires",
    "Avg ongoing deal value": "Valeur moyenne des affaires en cours",
    "Avg time to close a deal": "Temps moyen pour conclure une affaire",
    "Avg time to close a lead": "Temps moyen pour convertir un prospect",
    "Avg won deal value": "Valeur moyenne des affaires gagnées",
    "Avg. deal value": "Valeur moy. des affaires",
    "Avg. ongoing deal value": "Valeur moy. des affaires en cours",
    "Avg. time to close a deal": "Temps moy. pour conclure une affaire",
    "Avg. time to close a lead": "Temps moy. pour convertir un prospect",
    "Avg. won deal value": "Valeur moy. des affaires gagnées",

    # Charts and visualizations
    "Axis chart": "Graphique à axes",
    "BCC": "CCI",
    "Back to all logs": "Retour à tous les journaux",
    "Back to file upload": "Retour au téléchargement de fichier",
    "Background Sync Frequency": "Fréquence de synchronisation en arrière-plan",
    "Backlog": "En attente",

    # Brand settings
    "Brand Settings": "Paramètres de marque",
    "Brand logo": "Logo de marque",
    "Brand name": "Nom de marque",
    "Brand settings": "Paramètres de marque",
    "Branding": "Image de marque",
    "Bulk Edit": "Modification groupée",

    # Email
    "CC": "CC",

    # CRM DocTypes
    "CRM Call Log": "Journal d'appel CRM",
    "CRM Communication Status": "Statut de communication CRM",
    "CRM Contacts": "Contacts CRM",
    "CRM Dashboard": "Tableau de bord CRM",
    "CRM Deal": "Affaire CRM",
    "CRM Deal Status": "Statut d'affaire CRM",
    "CRM Dropdown Item": "Élément de liste déroulante CRM",
    "CRM Exotel Settings": "Paramètres Exotel CRM",
    "CRM Fields Layout": "Disposition des champs CRM",
    "CRM Form Script": "Script de formulaire CRM",
    "CRM Global Settings": "Paramètres globaux CRM",
    "CRM Holiday": "Jour férié CRM",
    "CRM Holiday List": "Liste des jours fériés CRM",
    "CRM Industry": "Secteur CRM",
    "CRM Invitation": "Invitation CRM",
    "CRM Lead": "Prospect CRM",
    "CRM Lead Source": "Source de prospect CRM",
    "CRM Lead Status": "Statut de prospect CRM",
    "CRM Lost Reason": "Raison de perte CRM",
    "CRM Notification": "Notification CRM",
    "CRM Organization": "Organisation CRM",
    "CRM Portal Page": "Page portail CRM",
    "CRM Product": "Produit CRM",
    "CRM Products": "Produits CRM",
    "CRM Rolling Response Time": "Temps de réponse mobile CRM",
    "CRM Service Day": "Jour de service CRM",
    "CRM Service Level Agreement": "Accord de niveau de service CRM",
    "CRM Service Level Priority": "Priorité de niveau de service CRM",
    "CRM Status Change Log": "Journal des changements de statut CRM",
    "CRM Task": "Tâche CRM",
    "CRM Telephony Agent": "Agent de téléphonie CRM",
    "CRM Telephony Phone": "Téléphone de téléphonie CRM",
    "CRM Territory": "Territoire CRM",
    "CRM Twilio Settings": "Paramètres Twilio CRM",
    "CRM View Settings": "Paramètres d'affichage CRM",
    "CRM currency for all monetary values. Once set, cannot be edited.": "Devise CRM pour toutes les valeurs monétaires. Une fois définie, ne peut pas être modifiée.",

    # Export formats
    "CSV": "CSV",

    # Call features
    "Call duration in seconds": "Durée de l'appel en secondes",
    "Call log": "Journal d'appel",
    "Call using {0}": "Appeler avec {0}",
    "Call with John Doe": "Appel avec John Doe",
    "Caller": "Appelant",
    "Calling Medium": "Moyen d'appel",
    "Calling...": "Appel en cours...",
    "Can't retry sync for this without source!": "Impossible de réessayer la synchronisation sans source !",
    "Cannot change role of user with Admin access": "Impossible de modifier le rôle d'un utilisateur ayant un accès Administrateur",
    "Cannot delete standard items {0}": "Impossible de supprimer les éléments standards {0}",
    "Cannot enable rule without adding users in it": "Impossible d'activer la règle sans y ajouter d'utilisateurs",
    "Capture": "Capturer",
    "Capturing leads": "Capture de prospects",

    # Status changes
    "Change deal status": "Changer le statut de l'affaire",
    "Change image": "Changer l'image",
    "Change status": "Changer le statut",

    # Choice modals
    "Choose Existing": "Choisir un existant",
    "Choose Existing Contact": "Choisir un contact existant",
    "Choose Existing Organization": "Choisir une organisation existante",
    "Choose how {0} are assigned among salespeople.": "Choisissez comment les {0} sont attribués parmi les commerciaux.",
    "Choose the days of the week when this rule should be active.": "Choisissez les jours de la semaine où cette règle doit être active.",
    "Choose the email service provider you want to configure.": "Choisissez le fournisseur de service de messagerie que vous souhaitez configurer.",
    "Choose which {0} are affected by this un-assignment rule.": "Choisissez quels {0} sont affectés par cette règle de désattribution.",

    # Clear actions
    "Clear Assignment": "Effacer l'attribution",
    "Clear Sort": "Effacer le tri",
    "Clear all Filter": "Effacer tous les filtres",
    "Close panel": "Fermer le panneau",
    "Closed Date": "Date de clôture",

    # Column and view settings
    "Column Field": "Champ de colonne",
    "Common reasons for losing deals": "Raisons courantes de perte d'affaires",
    "Communication Status": "Statut de communication",
    "Communication Statuses": "Statuts de communication",
    "Company in ERPNext Site": "Société sur le site ERPNext",
    "Condition": "Condition",
    "Conditions for this rule were created from": "Les conditions de cette règle ont été créées depuis",
    "Configure actions that appear on the home dropdown": "Configurer les actions qui apparaissent dans le menu déroulant d'accueil",
    "Configure forecasting feature to help predict sales performance and growth": "Configurer la fonction de prévision pour aider à prédire les performances et la croissance des ventes",
    "Configure telephony settings for your CRM": "Configurer les paramètres de téléphonie pour votre CRM",
    "Configure the currency and exchange rate provider for your CRM": "Configurer la devise et le fournisseur de taux de change pour votre CRM",
    "Configure the exchange rate provider for your CRM": "Configurer le fournisseur de taux de change pour votre CRM",
    "Configure your brand name, logo, and favicon": "Configurer le nom de votre marque, le logo et le favicon",

    # Confirmations
    "Confirm Delete": "Confirmer la suppression",
    "Confirm Password": "Confirmer le mot de passe",
    "Confirm Remove": "Confirmer la suppression",
    "Confirm overwrite": "Confirmer l'écrasement",

    # Connection
    "Connect your email": "Connecter votre e-mail",

    # Contact management
    "Contact Already Exists": "Le contact existe déjà",
    "Contact Support": "Contacter le support",
    "Contact Us": "Nous contacter",
    "Contact added": "Contact ajouté",
    "Contact already added": "Contact déjà ajouté",
    "Contact already exists with {0}": "Un contact existe déjà avec {0}",
    "Contact image updated": "Image du contact mise à jour",
    "Contact removed": "Contact retiré",
    "Contact updated": "Contact mis à jour",

    # Conversion
    "Convert lead to deal": "Convertir le prospect en affaire",
    "Converted successfully": "Converti avec succès",

    # Creation
    "Create View": "Créer une vue",
    "Create an event": "Créer un événement",
    "Create customer on status change": "Créer un client lors du changement de statut",
    "Create event": "Créer un événement",
    "Create lead": "Créer un prospect",
    "Create your first lead": "Créer votre premier prospect",
    "Create your first note": "Créer votre première note",
    "Create your first task": "Créer votre première tâche",

    # Currency
    "Currency & Exchange Rate": "Devise et taux de change",
    "Currency & Exchange rate provider": "Devise et fournisseur de taux de change",
    "Currency set as {0} successfully": "Devise définie comme {0} avec succès",
    "Current pipeline distribution": "Distribution actuelle du pipeline",

    # Customization
    "Custom actions": "Actions personnalisées",
    "Custom branding": "Image de marque personnalisée",
    "Custom fields": "Champs personnalisés",
    "Custom list actions": "Actions de liste personnalisées",
    "Custom statuses": "Statuts personnalisés",
    "Customer created successfully": "Client créé avec succès",
    "Customize quick filters": "Personnaliser les filtres rapides",

    # Time periods
    "Daily": "Quotidien",
    "Daily performance of leads, deals, and wins": "Performance quotidienne des prospects, affaires et gains",

    # Data
    "Data Fields": "Champs de données",
    "Date & Time": "Date et heure",

    # Deal management
    "Deal Status": "Statut de l'affaire",
    "Deal Statuses": "Statuts d'affaire",
    "Deal generation channel analysis": "Analyse des canaux de génération d'affaires",
    "Deal owner": "Propriétaire de l'affaire",
    "Deal value": "Valeur de l'affaire",
    "Deals by ongoing & won stage": "Affaires par étape en cours et gagnée",
    "Deals by salesperson": "Affaires par commercial",
    "Deals by source": "Affaires par source",
    "Deals by stage": "Affaires par étape",
    "Deals by territory": "Affaires par territoire",

    # Default settings
    "Default Medium": "Moyen par défaut",
    "Default Service Level Agreement already exists for {0}": "L'accord de niveau de service par défaut existe déjà pour {0}",
    "Default calling medium for logged in user": "Moyen d'appel par défaut pour l'utilisateur connecté",
    "Default calling medium set successfully to {0}": "Moyen d'appel par défaut défini avec succès sur {0}",
    "Default calling medium updated successfully": "Moyen d'appel par défaut mis à jour avec succès",
    "Default medium": "Moyen par défaut",
    "Default statuses, custom fields and layouts restored successfully.": "Statuts par défaut, champs personnalisés et mises en page restaurés avec succès.",

    # Delete operations
    "Delete & Restore": "Supprimer et restaurer",
    "Delete Task": "Supprimer la tâche",
    "Delete View": "Supprimer la vue",
    "Delete all": "Tout supprimer",
    "Delete attachment": "Supprimer la pièce jointe",
    "Delete contact": "Supprimer le contact",
    "Delete event": "Supprimer l'événement",
    "Delete invitation": "Supprimer l'invitation",
    "Delete linked item": "Supprimer l'élément lié",
    "Delete or unlink linked documents": "Supprimer ou délier les documents liés",
    "Delete or unlink these linked documents before deleting this document": "Supprimer ou délier ces documents liés avant de supprimer ce document",
    "Delete organization": "Supprimer l'organisation",
    "Delete {0} item(s)": "Supprimer {0} élément(s)",
    "Delete {0} items": "Supprimer {0} éléments",

    # Device
    "Device": "Appareil",
    "Discard unsaved changes?": "Abandonner les modifications non enregistrées ?",

    # Document types
    "DocType": "DocType",
    "Document Type": "Type de document",
    "Document does not exist": "Le document n'existe pas",
    "Document not found": "Document non trouvé",
    "Document updated successfully": "Document mis à jour avec succès",
    "Documentation": "Documentation",

    # Status
    "Done": "Terminé",
    "Donut chart": "Graphique en anneau",

    # Drag and drop
    "Drag and drop files here or upload from": "Glissez-déposez les fichiers ici ou téléchargez depuis",
    "Drop files here": "Déposez les fichiers ici",
    "Dropdown Items": "Éléments de liste déroulante",

    # Duplicate
    "Duplicate Assignment Rule": "Dupliquer la règle d'attribution",
    "Duplicate View": "Dupliquer la vue",
    "Duplicate an event": "Dupliquer un événement",
    "Duplicate event": "Dupliquer l'événement",
    "Duplicate template": "Dupliquer le modèle",

    # ERPNext
    "ERPNext": "ERPNext",
    "ERPNext CRM Settings": "Paramètres ERPNext CRM",
    "ERPNext Site API's": "API du site ERPNext",
    "ERPNext Site URL": "URL du site ERPNext",
    "ERPNext is not installed in the current site": "ERPNext n'est pas installé sur le site actuel",
    "ERPNext is not integrated with the CRM": "ERPNext n'est pas intégré au CRM",
    "ERPNext settings": "Paramètres ERPNext",
    "ERPNext settings updated": "Paramètres ERPNext mis à jour",

    # Edit operations
    "Edit Call Log": "Modifier le journal d'appel",
    "Edit Data Fields Layout": "Modifier la disposition des champs de données",
    "Edit Email": "Modifier l'e-mail",
    "Edit Field Layout": "Modifier la disposition des champs",
    "Edit Grid Fields Layout": "Modifier la disposition des champs de grille",
    "Edit Grid Row Fields Layout": "Modifier la disposition des champs de ligne de grille",
    "Edit Note": "Modifier la note",
    "Edit Quick Entry Layout": "Modifier la disposition d'entrée rapide",
    "Edit Task": "Modifier la tâche",
    "Edit View": "Modifier la vue",
    "Edit an event": "Modifier un événement",
    "Edit call log": "Modifier le journal d'appel",
    "Edit event": "Modifier l'événement",
    "Edit fields layout": "Modifier la disposition des champs",
    "Edit grid fields": "Modifier les champs de grille",
    "Edit note": "Modifier la note",
    "Edit row": "Modifier la ligne",
    "Edit task": "Modifier la tâche",
    "Editing Row {0}": "Modification de la ligne {0}",
    "Editing event": "Modification de l'événement",

    # Email
    "Email Accounts": "Comptes e-mail",
    "Email Sent At": "E-mail envoyé le",
    "Email account created successfully": "Compte e-mail créé avec succès",
    "Email account updated successfully": "Compte e-mail mis à jour avec succès",
    "Email accounts": "Comptes e-mail",
    "Email communication": "Communication par e-mail",
    "Email from Lead": "E-mail du prospect",
    "Email template": "Modèle d'e-mail",
    "Email templates": "Modèles d'e-mail",

    # Empty states
    "Empty - Choose a field to filter by": "Vide - Choisissez un champ pour filtrer",
    "Empty - Choose a field to sort by": "Vide - Choisissez un champ pour trier",

    # Enable/Disable
    "Enable Forecasting": "Activer les prévisions",
    "Enable forecasting": "Activer les prévisions",

    # Time
    "End time should be after start time": "L'heure de fin doit être après l'heure de début",
    "Enter Access Token": "Entrer le jeton d'accès",
    "Enter Source Name": "Entrer le nom de la source",
    "Enter access key": "Entrer la clé d'accès",
    "Enter brand name": "Entrer le nom de la marque",
    "Enter your Facebook Access Token": "Entrez votre jeton d'accès Facebook",

    # Errors
    "Error converting to deal: {0}": "Erreur lors de la conversion en affaire : {0}",
    "Error creating Lead Sync Source": "Erreur lors de la création de la source de synchronisation de prospects",
    "Error syncing lead": "Erreur lors de la synchronisation du prospect",
    "Error syncing leads": "Erreur lors de la synchronisation des prospects",
    "Error updating Lead Sync Source": "Erreur lors de la mise à jour de la source de synchronisation de prospects",
    "Error updating field": "Erreur lors de la mise à jour du champ",
    "Error while creating customer in ERPNext, check error log for more details": "Erreur lors de la création du client dans ERPNext, consultez le journal d'erreurs pour plus de détails",
    "Error while creating prospect in ERPNext, check error log for more details": "Erreur lors de la création du prospect dans ERPNext, consultez le journal d'erreurs pour plus de détails",
    "Error while fetching customer in ERPNext, check error log for more details": "Erreur lors de la récupération du client dans ERPNext, consultez le journal d'erreurs pour plus de détails",

    # Event
    "Event details": "Détails de l'événement",
    "Event title": "Titre de l'événement",

    # Frequency
    "Every 10 Minutes": "Toutes les 10 minutes",
    "Every 15 Minutes": "Toutes les 15 minutes",
    "Every 5 Minutes": "Toutes les 5 minutes",

    # Export
    "Excel": "Excel",
    "Exchange Rate Provider": "Fournisseur de taux de change",
    "Exchange rate provider": "Fournisseur de taux de change",

    # Exotel
    "Exotel": "Exotel",
    "Exotel Exception": "Exception Exotel",
    "Exotel Number": "Numéro Exotel",
    "Exotel Number Missing": "Numéro Exotel manquant",
    "Exotel Number {0} is not valid": "Le numéro Exotel {0} n'est pas valide",
    "Exotel is not enabled": "Exotel n'est pas activé",
    "Exotel settings updated successfully": "Paramètres Exotel mis à jour avec succès",

    # Expected values
    "Expected Closure Date": "Date de clôture prévue",
    "Expected Closure Date is required.": "La date de clôture prévue est obligatoire.",
    "Expected Deal Value": "Valeur prévisionnelle de l'affaire",
    "Expected Deal Value is required.": "La valeur prévisionnelle de l'affaire est obligatoire.",

    # Export
    "Export All {0} Record(s)": "Exporter tous les {0} enregistrement(s)",

    # FCRM
    "FCRM Note": "Note FCRM",
    "FCRM Settings": "Paramètres FCRM",

    # Facebook
    "Facebook": "Facebook",
    "Facebook Form ID": "ID du formulaire Facebook",
    "Facebook Lead Form": "Formulaire de prospect Facebook",
    "Facebook Lead Form Question": "Question du formulaire de prospect Facebook",
    "Facebook Lead ID": "ID du prospect Facebook",
    "Facebook Page": "Page Facebook",

    # Failed operations
    "Failed Lead Sync Log": "Journal de synchronisation de prospects échouée",
    "Failed to add users": "Échec de l'ajout d'utilisateurs",
    "Failed to capture Twilio recording": "Échec de la capture de l'enregistrement Twilio",
    "Failed to create email account, Invalid credentials": "Échec de la création du compte e-mail, identifiants invalides",
    "Failed to create template": "Échec de la création du modèle",
    "Failed to delete Lead Sync Source": "Échec de la suppression de la source de synchronisation de prospects",
    "Failed to delete template": "Échec de la suppression du modèle",
    "Failed to fetch exchange rate from {0} to {1} on {2}. Please check your internet connection or try again later.": "Échec de la récupération du taux de change de {0} vers {1} le {2}. Veuillez vérifier votre connexion Internet ou réessayer plus tard.",
    "Failed to load form controller: {0}": "Échec du chargement du contrôleur de formulaire : {0}",
    "Failed to rename template": "Échec du renommage du modèle",
    "Failed to update Twilio call status": "Échec de la mise à jour du statut d'appel Twilio",
    "Failed to update email account, Invalid credentials": "Échec de la mise à jour du compte e-mail, identifiants invalides",
    "Failed to update password": "Échec de la mise à jour du mot de passe",
    "Failed to update profile": "Échec de la mise à jour du profil",
    "Failed to update source": "Échec de la mise à jour de la source",
    "Failed to update template": "Échec de la mise à jour du modèle",

    # Failure
    "Failure": "Échec",
    "Failure Logs": "Journaux d'échecs",

    # Favicon
    "Favicon": "Favicon",

    # Fields
    "Fields Order": "Ordre des champs",
    "File \"{0}\" was skipped because of invalid file type": "Le fichier \"{0}\" a été ignoré en raison d'un type de fichier invalide",
    "File \"{0}\" was skipped because only {1} uploads are allowed": "Le fichier \"{0}\" a été ignoré car seuls {1} téléchargements sont autorisés",
    "File \"{0}\" was skipped because only {1} uploads are allowed for DocType \"{2}\"": "Le fichier \"{0}\" a été ignoré car seuls {1} téléchargements sont autorisés pour le DocType \"{2}\"",

    # First name
    "First Name is mandatory": "Le prénom est obligatoire",
    "First Response Due": "Première réponse due",
    "First Response TIme": "Délai de première réponse",
    "First name": "Prénom",

    # Forecasting
    "Forecasted revenue": "Chiffre d'affaires prévisionnel",
    "Forecasting": "Prévisions",
    "Forecasting disabled successfully": "Prévisions désactivées avec succès",
    "Forecasting enabled successfully": "Prévisions activées avec succès",

    # Form
    "Form Name": "Nom du formulaire",
    "Form Script updated successfully": "Script de formulaire mis à jour avec succès",

    # Frappe
    "Frappe CRM": "Frappe CRM",
    "Frappe CRM mobile": "Frappe CRM mobile",

    # Days of week
    "Friday": "Vendredi",

    # From
    "From Date": "Date de début",
    "From Type": "Type de",
    "From User": "De l'utilisateur",

    # Funnel
    "Funnel conversion": "Conversion de l'entonnoir",

    # GMT
    "GMT+5:30": "GMT+5:30",

    # Geographic
    "Geographic distribution of deals and revenue": "Distribution géographique des affaires et du chiffre d'affaires",

    # GitHub
    "GitHub Repository": "Dépôt GitHub",

    # Navigation
    "Go to invite page": "Aller à la page d'invitation",
    "Go to website": "Aller au site web",

    # Grid
    "Grid Row": "Ligne de grille",
    "Group By Field": "Grouper par champ",

    # Call actions
    "Hang up": "Raccrocher",

    # Helpdesk
    "Helpdesk": "Service d'assistance",
    "Helpdesk CRM Settings": "Paramètres CRM du service d'assistance",
    "Helpdesk Site API's": "API du site de service d'assistance",
    "Helpdesk Site URL": "URL du site de service d'assistance",
    "Helpdesk is not installed in the current site": "Le service d'assistance n'est pas installé sur le site actuel",
    "Helpdesk is not integrated with the CRM": "Le service d'assistance n'est pas intégré au CRM",
    "Helpdesk settings": "Paramètres du service d'assistance",
    "Helpdesk settings updated": "Paramètres du service d'assistance mis à jour",

    # Hide/Show
    "Hide Password": "Masquer le mot de passe",
    "Hide Recording": "Masquer l'enregistrement",
    "Hide border": "Masquer la bordure",
    "Hide label": "Masquer le libellé",
    "Hide preview": "Masquer l'aperçu",

    # Holidays
    "Holidays": "Jours fériés",

    # Home
    "Home Actions": "Actions d'accueil",
    "Home actions": "Actions d'accueil",

    # Understanding
    "I understand, add conditions": "Je comprends, ajouter des conditions",

    # Conditional statements
    "If enabled, all outgoing emails will be sent from this account. Note: Only one account can be default outgoing.": "Si activé, tous les e-mails sortants seront envoyés depuis ce compte. Remarque : Un seul compte peut être défini comme sortant par défaut.",
    "If enabled, all replies to your company (eg: replies@yourcomany.com) will come to this account. Note: Only one account can be default incoming.": "Si activé, toutes les réponses à votre entreprise (ex: replies@yourcompany.com) viendront sur ce compte. Remarque : Un seul compte peut être défini comme entrant par défaut.",
    "If enabled, outgoing emails can be sent from this account.": "Si activé, les e-mails sortants peuvent être envoyés depuis ce compte.",
    "If enabled, records can be created from the incoming emails on this account.": "Si activé, des enregistrements peuvent être créés à partir des e-mails entrants sur ce compte.",

    # Time expressions
    "In less than a minute": "Dans moins d'une minute",

    # Call types
    "Inbound Call": "Appel entrant",
    "Incoming call...": "Appel entrant...",

    # Industries
    "Industries": "Secteurs",

    # Call status
    "Initiating call...": "Lancement de l'appel...",

    # Insert
    "Insert Email Template": "Insérer un modèle d'e-mail",
    "Insert Emoji": "Insérer un emoji",

    # Integration
    "Integration Not Enabled": "Intégration non activée",

    # Introduction
    "Introduction": "Introduction",

    # Invalid states
    "Invalid Account SID or Auth Token.": "SID de compte ou jeton d'authentification invalide.",
    "Invalid Email": "E-mail invalide",
    "Invalid Exotel Number": "Numéro Exotel invalide",
    "Invalid access token provided for Facebook.": "Jeton d'accès invalide fourni pour Facebook.",
    "Invalid chart name": "Nom de graphique invalide",
    "Invalid credentials": "Identifiants invalides",
    "Invalid email ID": "ID d'e-mail invalide",
    "Invalid fields, check if all are filled in and values are correct.": "Champs invalides, vérifiez que tous sont remplis et que les valeurs sont correctes.",
    "Invalid page or not permitted to access": "Page invalide ou accès non autorisé",
    "Invalid start or end time": "Heure de début ou de fin invalide",
    "Invalid website URL": "URL de site web invalide",

    # Invite
    "Invite New User": "Inviter un nouvel utilisateur",
    "Invite User": "Inviter un utilisateur",
    "Invite agent": "Inviter un agent",
    "Invite as": "Inviter en tant que",
    "Invite users": "Inviter des utilisateurs",
    "Invite users to access CRM. Specify their roles to control access and permissions": "Inviter des utilisateurs à accéder au CRM. Spécifiez leurs rôles pour contrôler l'accès et les permissions",
    "Invite your team": "Invitez votre équipe",
    "Invited By": "Invité par",

    # ERPNext questions
    "Is ERPNext installed on a different site?": "ERPNext est-il installé sur un site différent ?",
    "Is Group": "Est un groupe",
    "Is Helpdesk installed on a different site?": "Le service d'assistance est-il installé sur un site différent ?",

    # Forecasting
    "It will make deal's \"Expected Closure Date\" & \"Expected Deal Value\" mandatory to get accurate forecasting insights": "Cela rendra obligatoires la \"Date de clôture prévue\" et la \"Valeur prévisionnelle de l'affaire\" pour obtenir des prévisions précises",

    # JSON
    "JSON": "JSON",

    # Names
    "John Doe": "Jean Dupont",

    # Kanban
    "Kanban Columns": "Colonnes Kanban",
}

def translate_po_file(filepath):
    """Translate all empty msgstr in PO file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    translated_count = 0

    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Check for msgid line
        if line.startswith('msgid "') and line != 'msgid ""':
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)

                output_lines.append(line)
                i += 1

                # Check msgstr
                if i < len(lines) and lines[i].startswith('msgstr'):
                    msgstr_line = lines[i].rstrip('\n')

                    if msgstr_line == 'msgstr ""' and msgid_text in TRANSLATIONS:
                        translation = TRANSLATIONS[msgid_text]
                        output_lines.append(f'msgstr "{translation}"')
                        translated_count += 1
                    else:
                        output_lines.append(msgstr_line)
                    i += 1
                continue

        output_lines.append(line)
        i += 1

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))

    return translated_count

if __name__ == '__main__':
    po_file = '/Users/jeremy/GitHub/crm/crm/locale/fr.po'
    print("Translating fr.po file...")
    count = translate_po_file(po_file)
    print(f"\nTranslated {count} strings")

    # Check remaining
    import subprocess
    result = subprocess.run(['grep', '-c', 'msgstr ""', po_file], capture_output=True, text=True)
    remaining = result.stdout.strip()
    print(f"Remaining untranslated: {remaining}")

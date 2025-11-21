#!/usr/bin/env python3
"""
Final batch of translations for remaining 457 strings
"""
import re

FINAL_TRANSLATIONS = {
    # Empty string
    "": "",

    # Templates with placeholders
    "<p>Dear {{ lead_name }},</p>\\n\\n<p>This is a reminder for the payment of {{ grand_total }}.</p>\\n\\n<p>Thanks,</p>\\n<p>Frappé</p>":
        "<p>Cher(e) {{ lead_name }},</p>\\n\\n<p>Ceci est un rappel pour le paiement de {{ grand_total }}.</p>\\n\\n<p>Merci,</p>\\n<p>Frappé</p>",
    "Automatically update \"Expected Deal Value\" based on the total value of associated products in a deal":
        "Met à jour automatiquement la \"Valeur prévisionnelle de l'affaire\" en fonction de la valeur totale des produits associés dans une affaire",
    "Dear {{ lead_name }}, \\n\\nThis is a reminder for the payment of {{ grand_total }}. \\n\\nThanks, \\nFrappé":
        "Cher(e) {{ lead_name }}, \\n\\nCeci est un rappel pour le paiement de {{ grand_total }}. \\n\\nMerci, \\nFrappé",

    # File operations
    "File \"{0}\" was skipped because of invalid file type": "Le fichier \"{0}\" a été ignoré en raison d'un type de fichier invalide",
    "File \"{0}\" was skipped because only {1} uploads are allowed": "Le fichier \"{0}\" a été ignoré car seuls {1} téléchargements sont autorisés",
    "File \"{0}\" was skipped because only {1} uploads are allowed for DocType \"{2}\"": "Le fichier \"{0}\" a été ignoré car seuls {1} téléchargements sont autorisés pour le DocType \"{2}\"",

    # Messages
    "Hi John, \\n\\nCan you please provide more details on this...": "Bonjour John, \\n\\nPouvez-vous fournir plus de détails à ce sujet...",
    "It will make deal's \"Expected Closure Date\" & \"Expected Deal Value\" mandatory to get accurate forecasting insights": "Cela rendra obligatoires la \"Date de clôture prévue\" et la \"Valeur prévisionnelle de l'affaire\" pour obtenir des prévisions précises",

    # Kanban
    "Kanban Fields": "Champs Kanban",
    "Kanban Settings": "Paramètres Kanban",

    # Time periods
    "Last 6 Months": "6 derniers mois",
    "Last Responded On": "Dernière réponse le",
    "Last Response Time": "Temps de dernière réponse",
    "Last Status Change Log": "Dernier journal de changement de statut",
    "Last Synced At": "Dernière synchronisation le",
    "Last modified": "Dernière modification",
    "Last name": "Nom de famille",
    "Last user assigned by this rule": "Dernier utilisateur attribué par cette règle",

    # Lead management
    "Lead Data": "Données du prospect",
    "Lead Owner cannot be same as the Lead Email Address": "Le propriétaire du prospect ne peut pas être identique à l'adresse e-mail du prospect",
    "Lead Sources": "Sources de prospects",
    "Lead Statuses": "Statuts de prospects",
    "Lead Sync Source": "Source de synchronisation de prospects",
    "Lead Sync Source created successfully": "Source de synchronisation de prospects créée avec succès",
    "Lead Sync Source deleted successfully": "Source de synchronisation de prospects supprimée avec succès",
    "Lead Syncing": "Synchronisation de prospects",
    "Lead generation channel analysis": "Analyse des canaux de génération de prospects",
    "Lead sources": "Sources de prospects",
    "Lead sync initiated.": "Synchronisation de prospects initiée.",
    "Lead to deal conversion pipeline": "Pipeline de conversion de prospect en affaire",
    "Leads by source": "Prospects par source",

    # Learn and library
    "Learn about conditions": "En savoir plus sur les conditions",
    "Library": "Bibliothèque",
    "Listen": "Écouter",

    # Loading and logging
    "Load Default Columns": "Charger les colonnes par défaut",
    "Log ID": "ID du journal",
    "Log a Call": "Enregistrer un appel",
    "Login with different account": "Se connecter avec un autre compte",
    "Logo": "Logo",

    # Lost deals
    "Lost Notes": "Notes de perte",
    "Lost deal reasons": "Raisons de perte d'affaires",
    "Lost notes": "Notes de perte",
    "Lost notes are required when lost reason is \"Other\"": "Les notes de perte sont requises lorsque la raison de perte est \"Autre\"",
    "Lost reason": "Raison de perte",

    # Make actions
    "Make Call": "Passer un appel",
    "Make Private": "Rendre privé",
    "Make Public": "Rendre public",
    "Make a Call": "Passer un appel",
    "Make a call": "Passer un appel",
    "Make attachment {0}": "Rendre la pièce jointe {0}",
    "Make call": "Passer un appel",
    "Make private": "Rendre privé",
    "Make public": "Rendre public",
    "Make {0} as default calling medium": "Définir {0} comme moyen d'appel par défaut",

    # Makes and manage
    "Makes \"Expected Closure Date\" and \"Expected Deal Value\" mandatory for deal value forecasting": "Rend obligatoires la \"Date de clôture prévue\" et la \"Valeur prévisionnelle de l'affaire\" pour les prévisions de valeur d'affaire",
    "Manage CRM users by adding or inviting them, and assign roles to control their access and permissions": "Gérer les utilisateurs CRM en les ajoutant ou en les invitant, et attribuer des rôles pour contrôler leur accès et leurs permissions",
    "Manage your email accounts to send and receive emails directly from CRM. You can add multiple accounts and set one as default for incoming and outgoing emails.": "Gérer vos comptes e-mail pour envoyer et recevoir des e-mails directement depuis le CRM. Vous pouvez ajouter plusieurs comptes et en définir un par défaut pour les e-mails entrants et sortants.",

    # Mandatory fields
    "Mandatory field error: {0}": "Erreur de champ obligatoire : {0}",
    "Mandatory field(s) {0} must be mapped": "Le(s) champ(s) obligatoire(s) {0} doi(ven)t être mappé(s)",
    "Mandatory fields required: {0}": "Champs obligatoires requis : {0}",

    # Mapped and mark
    "Mapped to CRM Field": "Mappé au champ CRM",
    "Mark all as read": "Tout marquer comme lu",

    # Date example
    "May 1, 2025": "1er mai 2025",

    # Mention and minimize
    "Mention": "Mentionner",
    "Minimize": "Minimiser",

    # Mobile
    "Mobile No should be a number": "Le n° de mobile doit être un nombre",
    "Mobile Number": "Numéro de mobile",
    "Mobile Number Missing": "Numéro de mobile manquant",
    "Mobile app installation": "Installation de l'application mobile",
    "Mobile no": "N° de mobile",

    # Days
    "Monday": "Lundi",

    # Period
    "Month": "Mois",
    "Monthly": "Mensuel",

    # More and move
    "More Options": "Plus d'options",
    "Move to next section": "Passer à la section suivante",
    "Move to next tab": "Passer à l'onglet suivant",
    "Move to previous section": "Revenir à la section précédente",
    "Move to previous tab": "Revenir à l'onglet précédent",

    # My deals
    "My Open Deals": "Mes affaires ouvertes",

    # Naming and nested
    "Naming Series": "Série de nommage",
    "Nested conditions": "Conditions imbriquées",

    # New items
    "New Address": "Nouvelle adresse",
    "New Assignment Rule": "Nouvelle règle d'attribution",
    "New Assignment Rule Name": "Nom de la nouvelle règle d'attribution",
    "New Call Log": "Nouveau journal d'appel",
    "New Comment": "Nouveau commentaire",
    "New Lead Sync Source": "Nouvelle source de synchronisation de prospects",
    "New Message": "Nouveau message",
    "New Note": "Nouvelle note",
    "New Section": "Nouvelle section",
    "New Tab": "Nouvel onglet",
    "New WhatsApp Message": "Nouveau message WhatsApp",
    "New contact will be created based on the person's details": "Un nouveau contact sera créé en fonction des détails de la personne",
    "New event": "Nouvel événement",
    "New organization will be created based on the data in details section": "Une nouvelle organisation sera créée en fonction des données de la section détails",
    "New template": "Nouveau modèle",

    # Next period
    "Next 6 Months": "6 prochains mois",
    "Next Quarter": "Prochain trimestre",
    "Next Step": "Prochaine étape",

    # No items
    "No Answer": "Pas de réponse",
    "No Events Scheduled": "Aucun événement planifié",
    "No Title": "Sans titre",
    "No changes made": "Aucun changement effectué",
    "No contacts added": "Aucun contact ajouté",
    "No details added": "Aucun détail ajouté",
    "No email set": "Aucun e-mail défini",
    "No email templates found": "Aucun modèle d'e-mail trouvé",
    "No failure logs found": "Aucun journal d'échecs trouvé",
    "No items in the list": "Aucun élément dans la liste",
    "No label": "Aucun libellé",
    "No lead sources found": "Aucune source de prospects trouvée",
    "No mobile number set": "Aucun numéro de mobile défini",
    "No new notifications": "Aucune nouvelle notification",
    "No phone number set": "Aucun numéro de téléphone défini",
    "No primary contact set": "Aucun contact principal défini",
    "No templates found": "Aucun modèle trouvé",
    "No users found": "Aucun utilisateur trouvé",
    "No website found": "Aucun site web trouvé",
    "No website set": "Aucun site web défini",
    "No {0} Available": "Aucun(e) {0} disponible",
    "No {0} Found": "Aucun(e) {0} trouvé(e)",

    # Not allowed
    "Not Allowed": "Non autorisé",
    "Not Synced": "Non synchronisé",
    "Not allowed to add contact to Deal": "Non autorisé à ajouter un contact à l'affaire",
    "Not allowed to convert Lead to Deal": "Non autorisé à convertir un prospect en affaire",
    "Not allowed to remove contact from Deal": "Non autorisé à retirer un contact de l'affaire",
    "Not allowed to set primary contact for Deal": "Non autorisé à définir un contact principal pour l'affaire",
    "Not implemented yet!": "Pas encore implémenté !",

    # Notes and notifications
    "Notes View": "Vue des notes",
    "Notification Text": "Texte de notification",
    "Notification Type Doc": "Doc de type de notification",
    "Notification Type Doctype": "DocType de type de notification",

    # Number
    "Number chart": "Graphique numérique",
    "Number of deals": "Nombre d'affaires",
    "Number of deals and total value per salesperson": "Nombre d'affaires et valeur totale par commercial",

    # Old
    "Old Condition": "Ancienne condition",
    "Old Parent": "Ancien parent",

    # On and ongoing
    "On Hold": "En attente",
    "Ongoing": "En cours",
    "Ongoing deals": "Affaires en cours",

    # Only and open
    "Only image files are allowed": "Seuls les fichiers image sont autorisés",
    "Open Deal": "Affaire ouverte",
    "Open Lead": "Prospect ouvert",
    "Open in Portal": "Ouvrir dans le portail",
    "Open in new window": "Ouvrir dans une nouvelle fenêtre",
    "Open nested conditions": "Ouvrir les conditions imbriquées",
    "Open website": "Ouvrir le site web",

    # Or and organization
    "Or create leads manually": "Ou créer des prospects manuellement",
    "Organization Logo": "Logo de l'organisation",
    "Organization logo": "Logo de l'organisation",
    "Organizer": "Organisateur",

    # Other and outbound
    "Other features": "Autres fonctionnalités",
    "Outbound Call": "Appel sortant",
    "Owner: {0}": "Propriétaire : {0}",

    # Parent and password
    "Parent CRM Territory": "Territoire CRM parent",
    "Password cannot be reset by Demo User {}": "Le mot de passe ne peut pas être réinitialisé par l'utilisateur de démonstration {}",
    "Password updated successfully": "Mot de passe mis à jour avec succès",

    # Payment
    "Payment Reminder": "Rappel de paiement",
    "Payment Reminder from Frappé - (#{{ name }})": "Rappel de paiement de Frappé - (#{{ name }})",

    # Pending and personal
    "Pending Invites": "Invitations en attente",
    "Person": "Personne",
    "Personal Settings": "Paramètres personnels",

    # Phone and pin
    "Phone Numbers": "Numéros de téléphone",
    "Pin View": "Épingler la vue",
    "Pinned": "Épinglé",
    "Pinned Views": "Vues épinglées",
    "Pinned view": "Vue épinglée",

    # Playback and please
    "Playback speed": "Vitesse de lecture",
    "Please add an email account to continue.": "Veuillez ajouter un compte e-mail pour continuer.",
    "Please check your access token": "Veuillez vérifier votre jeton d'accès",
    "Please enable twilio settings before making a call.": "Veuillez activer les paramètres Twilio avant de passer un appel.",
    "Please enter a valid URL": "Veuillez entrer une URL valide",
    "Please enter the Exchangerate Host access key.": "Veuillez entrer la clé d'accès Exchangerate Host.",
    "Please provide a reason for marking this deal as lost": "Veuillez fournir une raison pour marquer cette affaire comme perdue",
    "Please select a currency before saving.": "Veuillez sélectionner une devise avant d'enregistrer.",
    "Please select a lead gen form before syncing!": "Veuillez sélectionner un formulaire de génération de prospects avant la synchronisation !",
    "Please select an existing contact": "Veuillez sélectionner un contact existant",
    "Please select an existing organization": "Veuillez sélectionner une organisation existante",
    "Please setup Exotel intergration": "Veuillez configurer l'intégration Exotel",
    "Please specify a reason for losing the deal.": "Veuillez spécifier une raison pour la perte de l'affaire.",
    "Please specify the reason for losing the deal.": "Veuillez spécifier la raison de la perte de l'affaire.",

    # Primary
    "Primary Email": "E-mail principal",
    "Primary Mobile No": "N° de mobile principal",
    "Primary Phone": "Téléphone principal",
    "Primary contact set": "Contact principal défini",

    # Product and profile
    "Product Code": "Code produit",
    "Product Name": "Nom du produit",
    "Profile updated successfully": "Profil mis à jour avec succès",
    "Projected vs actual revenue based on deal probability": "Chiffre d'affaires projeté vs réel basé sur la probabilité de l'affaire",

    # Public and questions
    "Public Views": "Vues publiques",
    "Public view": "Vue publique",
    "Questions": "Questions",

    # Quick and reason
    "Quick Filters updated successfully": "Filtres rapides mis à jour avec succès",
    "Quick entry layout": "Disposition d'entrée rapide",
    "Reason": "Raison",

    # Record
    "Record Calls": "Enregistrer les appels",
    "Record Outgoing Calls": "Enregistrer les appels sortants",

    # Reference
    "Reference Doc": "Doc de référence",
    "Reference Document Type": "Type de document de référence",
    "Reference Name": "Nom de référence",

    # Reject and remove
    "Reject": "Rejeter",
    "Reject call": "Rejeter l'appel",
    "Remove all": "Tout supprimer",
    "Remove and move fields to previous column": "Supprimer et déplacer les champs vers la colonne précédente",
    "Remove column": "Supprimer la colonne",
    "Remove group": "Supprimer le groupe",
    "Remove image": "Supprimer l'image",
    "Remove section": "Supprimer la section",
    "Remove tab": "Supprimer l'onglet",

    # Required and reset
    "Required Fields": "Champs obligatoires",
    "Reset Changes": "Réinitialiser les modifications",
    "Reset ERPNext Form Script": "Réinitialiser le script de formulaire ERPNext",
    "Reset to Default": "Réinitialiser par défaut",
    "Reset to default": "Réinitialiser par défaut",

    # Responded and response
    "Responded On": "Répondu le",
    "Response Time": "Temps de réponse",
    "Response and Follow Up": "Réponse et suivi",
    "Restart the SLA each time the customer replies (status changes to Open) and fulfill it when marked as Replied": "Redémarrer le SLA à chaque fois que le client répond (statut passe à Ouvert) et le remplir lorsqu'il est marqué comme Répondu",

    # Restore and retake
    "Restore Defaults": "Restaurer les valeurs par défaut",
    "Retake": "Reprendre",
    "Retry Sync": "Réessayer la synchronisation",

    # Rich and ringing
    "Rich Text": "Texte enrichi",
    "Ringing...": "Sonnerie...",

    # Rolling and route
    "Rolling Response Due": "Réponse mobile due",
    "Rolling Responses": "Réponses mobiles",
    "Route": "Route",
    "Route Name": "Nom de la route",
    "Rows": "Lignes",

    # SLA
    "SLA": "SLA",
    "SLA Creation": "Création SLA",
    "SLA Name": "Nom du SLA",
    "SLA Status": "Statut SLA",
    "SUBJECT": "SUJET",

    # Sales
    "Sales Manager": "Responsable des ventes",
    "Sales User": "Utilisateur des ventes",
    "Sales trend": "Tendance des ventes",
    "Sales user": "Utilisateur des ventes",
    "Salesperson": "Commercial",

    # Saturday and save
    "Saturday": "Samedi",
    "Save Changes": "Enregistrer les modifications",
    "Saved Views": "Vues enregistrées",
    "Saved view": "Vue enregistrée",

    # Schedule and script
    "Schedule a task...": "Planifier une tâche...",
    "Schedule an Event": "Planifier un événement",
    "Schedule an event": "Planifier un événement",
    "Script": "Script",

    # Search and see
    "Search template": "Rechercher un modèle",
    "Search user": "Rechercher un utilisateur",
    "See all participants": "Voir tous les participants",

    # Select
    "Select Range": "Sélectionner une plage",
    "Select Source Type": "Sélectionner le type de source",
    "Select currency": "Sélectionner la devise",
    "Select provider": "Sélectionner le fournisseur",
    "Select the assignees for {0}.": "Sélectionner les assignés pour {0}.",

    # Send
    "Send Invites": "Envoyer les invitations",
    "Send Template": "Envoyer le modèle",
    "Send an email": "Envoyer un e-mail",
    "Send email": "Envoyer un e-mail",
    "Send invites to": "Envoyer des invitations à",

    # Service
    "Service Provider": "Fournisseur de services",
    "Service level agreement": "Accord de niveau de service",

    # Set
    "Set As Primary": "Définir comme principal",
    "Set all as private": "Tout définir comme privé",
    "Set all as public": "Tout définir comme public",
    "Set an organization": "Définir une organisation",
    "Set as Primary Contact": "Définir comme contact principal",
    "Set as default": "Définir par défaut",
    "Set currency": "Définir la devise",
    "Set first name": "Définir le prénom",

    # Setting up
    "Setting up": "Configuration",
    "Setting up Frappe Mail requires you to have an API key and API Secret of your email account. Read more ": "La configuration de Frappe Mail nécessite une clé API et un secret API de votre compte e-mail. En savoir plus ",
    "Setup Email": "Configurer l'e-mail",
    "Setup the Exchange Rate Provider as 'Exchangerate Host' in settings, as default provider does not support currency conversion for {0} to {1}.": "Configurez le fournisseur de taux de change comme 'Exchangerate Host' dans les paramètres, car le fournisseur par défaut ne prend pas en charge la conversion de devise de {0} vers {1}.",
    "Setup your password": "Configurer votre mot de passe",

    # Show
    "Show Password": "Afficher le mot de passe",
    "Show border": "Afficher la bordure",
    "Show label": "Afficher le libellé",
    "Show less": "Afficher moins",
    "Show preview": "Afficher l'aperçu",

    # Side and simple
    "Side Panel": "Panneau latéral",
    "Simple Python Expression, Example: doc.status == 'Open' and doc.lead_source == 'Ads'": "Expression Python simple, Exemple : doc.status == 'Open' and doc.lead_source == 'Ads'",

    # Since
    "Since you removed {0} from the assignee, the {0} has also been removed.": "Comme vous avez retiré {0} de l'assigné, le {0} a également été retiré.",
    "Since you removed {0} from the assignee, the {0} has been changed to the next available assignee {1}.": "Comme vous avez retiré {0} de l'assigné, le {0} a été changé pour le prochain assigné disponible {1}.",

    # Some error
    "Some error occurred while renaming assignment rule": "Une erreur s'est produite lors du renommage de la règle d'attribution",
    "Some error occurred while updating assignment rule": "Une erreur s'est produite lors de la mise à jour de la règle d'attribution",

    # Source
    "Source Name": "Nom de la source",
    "Source disabled successfully": "Source désactivée avec succès",
    "Source enabled successfully": "Source activée avec succès",

    # Spacer and standard
    "Spacer": "Espaceur",
    "Standard Form Scripts can not be modified, duplicate the Form Script instead.": "Les scripts de formulaire standards ne peuvent pas être modifiés, dupliquez plutôt le script de formulaire.",
    "Standard Views": "Vues standards",

    # Start and status
    "Start with sample 10 leads": "Commencer avec 10 prospects d'exemple",
    "Status Change Log": "Journal de changement de statut",
    "Subject: {0}": "Sujet : {0}",

    # Sunday and support
    "Sunday": "Dimanche",
    "Support / Sales": "Support / Ventes",

    # Switch and sync
    "Switch camera": "Changer de caméra",
    "Sync Now": "Synchroniser maintenant",
    "Sync Successful, CRM Lead: ${frappe.utils.get_form_link(\"CRM Lead\", message.name, true)}!": "Synchronisation réussie, Prospect CRM : ${frappe.utils.get_form_link(\"CRM Lead\", message.name, true)} !",
    "Sync successful!": "Synchronisation réussie !",
    "Sync your contacts,email and calenders": "Synchroniser vos contacts, e-mails et calendriers",
    "Syncing started in background": "Synchronisation démarrée en arrière-plan",

    # System
    "System Configuration": "Configuration système",
    "System Manager": "Gestionnaire système",

    # Take and telegram
    "TO": "À",
    "Take a note...": "Prendre une note...",
    "Telegram Channel": "Canal Telegram",

    # Telephony
    "Telephony": "Téléphonie",
    "Telephony Medium": "Moyen de téléphonie",
    "Telephony settings": "Paramètres de téléphonie",

    # Template
    "Template created successfully": "Modèle créé avec succès",
    "Template deleted successfully": "Modèle supprimé avec succès",
    "Template disabled successfully": "Modèle désactivé avec succès",
    "Template enabled successfully": "Modèle activé avec succès",
    "Template name": "Nom du modèle",
    "Template renamed successfully": "Modèle renommé avec succès",
    "Template updated successfully": "Modèle mis à jour avec succès",

    # Territories and thanks
    "Territories": "Territoires",
    "Thanks": "Merci",

    # The condition
    "The Condition '{0}' is invalid: {1}": "La condition '{0}' est invalide : {1}",
    "The rate used to convert the deal's currency to your crm's base currency (set in CRM Settings). It is set once when the currency is first added and doesn't change automatically.": "Le taux utilisé pour convertir la devise de l'affaire vers la devise de base de votre CRM (défini dans les paramètres CRM). Il est défini une fois lorsque la devise est ajoutée pour la première fois et ne change pas automatiquement.",
    "The rate used to convert the organization's currency to your crm's base currency (set in CRM Settings). It is set once when the currency is first added and doesn't change automatically.": "Le taux utilisé pour convertir la devise de l'organisation vers la devise de base de votre CRM (défini dans les paramètres CRM). Il est défini une fois lorsque la devise est ajoutée pour la première fois et ne change pas automatiquement.",

    # There can
    "There can only be one default priority in Priorities table": "Il ne peut y avoir qu'une seule priorité par défaut dans la table des priorités",
    "These fields are required: {0}": "Ces champs sont obligatoires : {0}",

    # This
    "This Quarter": "Ce trimestre",
    "This section is not editable": "Cette section n'est pas modifiable",
    "This will delete selected items and items linked to it, are you sure?": "Cela supprimera les éléments sélectionnés et les éléments qui leur sont liés, êtes-vous sûr ?",
    "This will delete selected items and unlink linked items to it, are you sure?": "Cela supprimera les éléments sélectionnés et déliera les éléments qui leur sont liés, êtes-vous sûr ?",
    "This will restore (if not exist) all the default statuses, custom fields and layouts. Delete & Restore will delete default layouts and then restore them.": "Cela restaurera (s'ils n'existent pas) tous les statuts par défaut, champs personnalisés et mises en page. Supprimer et restaurer supprimera les mises en page par défaut puis les restaurera.",

    # Thursday and to
    "Thursday": "Jeudi",
    "To Date": "Date de fin",
    "To Type": "Type de",
    "To know more about setting up email accounts, click": "Pour en savoir plus sur la configuration des comptes e-mail, cliquez",
    "Todo": "À faire",

    # Toggle and took
    "Toggle on for preview": "Activer pour l'aperçu",
    "Took a call with John Doe and discussed the new project.": "A passé un appel avec Jean Dupont et discuté du nouveau projet.",

    # Total
    "Total after discount": "Total après remise",
    "Total leads": "Total des prospects",
    "Total number of leads": "Nombre total de prospects",
    "Total number of non won/lost deals": "Nombre total d'affaires non gagnées/perdues",
    "Total number of won deals based on its closure date": "Nombre total d'affaires gagnées selon leur date de clôture",

    # Tuesday and turn
    "Tuesday": "Mardi",
    "Turn into a group": "Transformer en groupe",

    # Twilio
    "TwiML SID": "SID TwiML",
    "Twilio": "Twilio",
    "Twilio API credential creation error.": "Erreur de création des identifiants API Twilio.",
    "Twilio Number": "Numéro Twilio",
    "Twilio is not enabled": "Twilio n'est pas activé",
    "Twilio settings updated successfully": "Paramètres Twilio mis à jour avec succès",

    # Type
    "Type an email address to add attendee": "Tapez une adresse e-mail pour ajouter un participant",
    "Type your message here...": "Tapez votre message ici...",

    # Unassign and unauthorized
    "Unassign conditions are invalid": "Les conditions de désattribution sont invalides",
    "Unassignment condition": "Condition de désattribution",
    "Unauthorized request": "Requête non autorisée",

    # Uncollapsible and ungroup
    "Uncollapsible": "Non réductible",
    "Ungroup conditions": "Dégrouper les conditions",

    # Unlink
    "Unlink": "Délier",
    "Unlink all": "Tout délier",
    "Unlink and delete": "Délier et supprimer",
    "Unlink and delete {0} items": "Délier et supprimer {0} éléments",
    "Unlink linked item": "Délier l'élément lié",
    "Unlink {0} item(s)": "Délier {0} élément(s)",

    # Unpin and unsaved
    "Unpin View": "Désépingler la vue",
    "Unsaved": "Non enregistré",
    "Unsaved changes": "Modifications non enregistrées",
    "Untitled": "Sans titre",

    # Update and upload
    "Update Account": "Mettre à jour le compte",
    "Update {0} Records": "Mettre à jour {0} enregistrements",
    "Upload Attachment": "Télécharger une pièce jointe",
    "Upload Document": "Télécharger un document",
    "Upload Image": "Télécharger une image",
    "Upload Video": "Télécharger une vidéo",
    "Upload image": "Télécharger une image",

    # User
    "User Management": "Gestion des utilisateurs",
    "User {0} has been removed": "L'utilisateur {0} a été retiré",
    "Users added successfully": "Utilisateurs ajoutés avec succès",

    # View
    "View Name": "Nom de la vue",
    "View contact": "Voir le contact",
    "Views": "Vues",

    # Web and webhook
    "Web form": "Formulaire web",
    "Webhook Verify Token": "Jeton de vérification du webhook",

    # Wednesday and welcome
    "Wednesday": "Mercredi",
    "Welcome Message": "Message de bienvenue",
    "Welcome to Helpdesk": "Bienvenue sur le service d'assistance",
    "Welcome {0}, lets add your first lead": "Bienvenue {0}, ajoutons votre premier prospect",

    # WhatsApp and where
    "WhatsApp": "WhatsApp",
    "WhatsApp Templates": "Modèles WhatsApp",
    "Where": "Où",

    # Width and won
    "Width can be in number, pixel or rem (eg. 3, 30px, 10rem)": "La largeur peut être en nombre, pixel ou rem (ex. 3, 30px, 10rem)",
    "Won deals": "Affaires gagnées",

    # You permissions
    "You are not permitted to access this resource.": "Vous n'êtes pas autorisé à accéder à cette ressource.",
    "You can also copy-paste following link in your browser": "Vous pouvez également copier-coller le lien suivant dans votre navigateur",
    "You can change the default calling medium from the settings": "Vous pouvez changer le moyen d'appel par défaut depuis les paramètres",
    "You can get your access key from ": "Vous pouvez obtenir votre clé d'accès depuis ",
    "You can invite multiple users by comma separating their email addresses": "Vous pouvez inviter plusieurs utilisateurs en séparant leurs adresses e-mail par des virgules",
    "You do not have Exotel Number set in your Telephony Agent": "Vous n'avez pas de numéro Exotel défini dans votre agent de téléphonie",
    "You do not have enough permissions to access Frappe CRM. Please contact your administrator if you believe this is an error.": "Vous n'avez pas les permissions suffisantes pour accéder à Frappe CRM. Veuillez contacter votre administrateur si vous pensez qu'il s'agit d'une erreur.",
    "You do not have mobile number set in your Telephony Agent": "Vous n'avez pas de numéro de mobile défini dans votre agent de téléphonie",
    "You do not have permission to access this document": "Vous n'avez pas la permission d'accéder à ce document",
    "You need to be in developer mode to edit a Standard Form Script": "Vous devez être en mode développeur pour modifier un script de formulaire standard",
    "You will be redirected to invite user page, unsaved changes will be lost.": "Vous serez redirigé vers la page d'invitation d'utilisateur, les modifications non enregistrées seront perdues.",
    "You will need a Meta developer account and an access token to sync leads from Facebook. Read more ": "Vous aurez besoin d'un compte développeur Meta et d'un jeton d'accès pour synchroniser les prospects depuis Facebook. En savoir plus ",
    "Your assignment on task {0} has been removed by {1}": "Votre attribution sur la tâche {0} a été retirée par {1}",
    "Your old condition will be overwritten. Are you sure you want to save?": "Votre ancienne condition sera écrasée. Êtes-vous sûr de vouloir enregistrer ?",

    # Actions
    "added a": "a ajouté un(e)",
    "amber": "ambre",
    "assigned a new task {0} to you": "vous a attribué une nouvelle tâche {0}",
    "assigned a {0} {1} to you": "vous a attribué un(e) {0} {1}",
    "changes from": "changements de",
    "email already exists": "l'e-mail existe déjà",

    # Exchange rate providers
    "exchangerate.host": "exchangerate.host",
    "frankfurter.app": "frankfurter.app",

    # Colors
    "gray": "gris",
    "group_by": "grouper_par",

    # Actions continued
    "has made a call": "a passé un appel",
    "has reached out": "a pris contact",
    "here": "ici",

    # Time expressions
    "in 1 hour": "dans 1 heure",
    "in 1 minute": "dans 1 minute",
    "in 1 year": "dans 1 an",
    "in {0} M": "dans {0} M",
    "in {0} d": "dans {0} j",
    "in {0} days": "dans {0} jours",
    "in {0} h": "dans {0} h",
    "in {0} hours": "dans {0} heures",
    "in {0} m": "dans {0} m",
    "in {0} minutes": "dans {0} minutes",
    "in {0} months": "dans {0} mois",
    "in {0} w": "dans {0} s",
    "in {0} weeks": "dans {0} semaines",
    "in {0} y": "dans {0} a",
    "in {0} years": "dans {0} ans",

    # Examples
    "john@doe.com": "jean@dupont.com",
    "label": "libellé",

    # Actions continued
    "mentioned you in {0}": "vous a mentionné dans {0}",
    "public": "public",
    "received a whatsapp message in {0}": "a reçu un message WhatsApp dans {0}",

    # Colors continued
    "teal": "sarcelle",
    "violet": "violet",

    # Warnings
    "which are not compatible with this UI, you will need to recreate the conditions here if you want to manage and add new conditions from this UI.": "qui ne sont pas compatibles avec cette interface, vous devrez recréer les conditions ici si vous souhaitez gérer et ajouter de nouvelles conditions depuis cette interface.",

    # Format strings
    "{0} Attendees": "{0} participants",
    "{0} M": "{0} M",
    "{0} assigned a {1} {2} to you": "{0} vous a attribué un(e) {1} {2}",
    "{0} h": "{0} h",
    "{0} has been granted {1} access": "{0} a obtenu l'accès {1}",
    "{0} hrs": "{0} heures",
    "{0} is an invalid email address": "{0} est une adresse e-mail invalide",
    "{0} m": "{0} m",
    "{0} mins": "{0} minutes",
    "{0} w": "{0} s",
    "{0} y": "{0} a",

    # Developer warnings
    "⚠️ Avoid using \"trigger\" as a field name — it conflicts with the built-in trigger() method.": "⚠️ Évitez d'utiliser \"trigger\" comme nom de champ — cela entre en conflit avec la méthode trigger() intégrée.",
    "⚠️ Method \"{0}\" not found in class.": "⚠️ Méthode \"{0}\" introuvable dans la classe.",
    "⚠️ No class found for doctype: {0}, it is mandatory to have a class for the parent doctype. it can be empty, but it should be present.": "⚠️ Aucune classe trouvée pour le doctype : {0}, il est obligatoire d'avoir une classe pour le doctype parent. Elle peut être vide, mais elle doit être présente.",
    "⚠️ No data found for parent field: {0}": "⚠️ Aucune donnée trouvée pour le champ parent : {0}",
    "⚠️ No row found for idx: {0} in parent field: {1}": "⚠️ Aucune ligne trouvée pour idx : {0} dans le champ parent : {1}",
}

def apply_final_translations(filepath):
    """Apply final translations to PO file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    output_lines = []
    i = 0
    translated_count = 0

    while i < len(lines):
        line = lines[i].rstrip('\n')

        if line.startswith('msgid "') and line != 'msgid ""':
            msgid_match = re.match(r'msgid "(.*)"', line)
            if msgid_match:
                msgid_text = msgid_match.group(1)

                output_lines.append(line)
                i += 1

                if i < len(lines) and lines[i].startswith('msgstr'):
                    msgstr_line = lines[i].rstrip('\n')

                    if msgstr_line == 'msgstr ""' and msgid_text in FINAL_TRANSLATIONS:
                        translation = FINAL_TRANSLATIONS[msgid_text]
                        # Properly escape the translation
                        translation_escaped = translation.replace('\\', '\\\\').replace('"', '\\"')
                        output_lines.append(f'msgstr "{translation_escaped}"')
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
    print("Applying final translations...")
    count = apply_final_translations(po_file)
    print(f"\nTranslated {count} strings")

    # Check remaining
    import subprocess
    result = subprocess.run(['grep', '-c', 'msgstr ""', po_file], capture_output=True, text=True)
    remaining = result.stdout.strip()
    print(f"Remaining untranslated: {remaining}")

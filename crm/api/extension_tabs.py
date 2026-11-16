# //// Neoffice — added file (no upstream equivalent)
# //// The tabs that an app adds to the page of a CRM document: the app declares them in its hooks (`crm_extension_tabs`, by
# //// doctype), and the page of the CRM asks which ones this account may see. The hub's representatives work their prospects in
# //// the CRM; their questions, offer, visits and presentation are the hub app's, shown in a tab of the prospect's page, so that no
# //// code of that app lives in this public fork. Empty on a site where no app declares one.

import frappe
from frappe import _


def _allowed(tab: dict, roles: set) -> bool:
	wanted = tab.get("roles")
	return not wanted or not roles.isdisjoint(wanted)


def _is_path_of_this_site(url) -> bool:
	return isinstance(url, str) and url.startswith("/") and not url.startswith("//")


@frappe.whitelist()
def get_tabs(doctype: str) -> list:
	"""The tabs apps add to the page of `doctype`, in the order they gave them, that the account may see.

	A tab is {name, label, url, roles?}: `url` is a path of this site (`{docname}` is replaced by the document's name),
	`roles` the roles that see it (everybody who may read the document when it is absent). A declaration that is not
	well formed, or that points at another site, is left out.
	"""
	if not frappe.has_permission(doctype, "read"):
		return []
	declared = (frappe.get_hooks("crm_extension_tabs") or {}).get(doctype) or []
	roles = set(frappe.get_roles())
	tabs = []
	for tab in declared:
		if not isinstance(tab, dict) or not tab.get("name") or not tab.get("label"):
			continue
		if not _is_path_of_this_site(tab.get("url")) or not _allowed(tab, roles):
			continue
		tabs.append({"name": tab["name"], "label": _(tab["label"]), "url": tab["url"]})
	return tabs


# //// The pages that an app adds to the CRM's menu, beside the lists: the hub's managers read the funnel of their representatives' visits and
# //// issue the cards there (`crm_extension_pages` in the app's hooks). The page is the app's, shown in a frame like a tab; the menu
# //// asks here which ones this account may see. Empty on a site where no app declares one.
@frappe.whitelist()
def get_pages() -> list:  # permission-check: ok filtered by the roles each page names
	"""The pages apps add to the CRM's menu, in the order they gave them, that the account may see.

	A page is {name, label, url, icon?, roles?}: `url` is a path of this site, `roles` the roles that see it (everybody who
	works the CRM when it is absent). A declaration that is not well formed, or that points at another site, is left out.
	"""
	declared = frappe.get_hooks("crm_extension_pages") or []
	roles = set(frappe.get_roles())
	pages = []
	for page in declared:
		if not isinstance(page, dict) or not page.get("name") or not page.get("label"):
			continue
		if not _is_path_of_this_site(page.get("url")) or not _allowed(page, roles):
			continue
		pages.append(
			{
				"name": page["name"],
				"label": _(page["label"]),
				"url": page["url"],
				"icon": page.get("icon") or "",
			}
		)
	return pages

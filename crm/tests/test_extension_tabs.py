# //// Neoffice — added file (no upstream equivalent)
# //// Proves `crm.api.extension_tabs`: the tabs an app adds to a document's page, by hook, filtered by role and by where they point.

import unittest
from unittest import mock

import frappe

from crm.api import extension_tabs

TABS = {
	"CRM Lead": [
		{
			"name": "Questions",
			"label": "Questions",
			"url": "/representants?embed=questions#/lead/{docname}",
			"roles": ["Sales Representative"],
		},
		{"name": "Everyone", "label": "Everyone", "url": "/page"},
		{"name": "Elsewhere", "label": "Elsewhere", "url": "https://example.com/x"},
		{"name": "Protocol", "label": "Protocol", "url": "//example.com/x"},
		{"name": "NoLabel", "url": "/x"},
		"not a dict",
	],
	"CRM Deal": [{"name": "Deal", "label": "Deal", "url": "/deal"}],
}


def run(roles, doctype="CRM Lead", can_read=True, hooks=TABS):
	with (
		mock.patch.object(frappe, "get_hooks", return_value=hooks),
		mock.patch.object(frappe, "get_roles", return_value=["All", "Guest", *roles]),
		mock.patch.object(frappe, "has_permission", return_value=can_read),
		mock.patch.object(extension_tabs, "_", side_effect=lambda text: text),
	):
		# the function under the type check of `frappe.whitelist`, which asks the request for its flags: nothing here is a request
		return getattr(extension_tabs.get_tabs, "__wrapped__", extension_tabs.get_tabs)(doctype)


class TestExtensionTabs(unittest.TestCase):
	def test_a_role_sees_the_tabs_for_its_roles_and_those_for_everybody_in_the_order_given(self):
		self.assertEqual([t["name"] for t in run(["Sales Representative"])], ["Questions", "Everyone"])

	def test_the_others_do_not_see_a_tab_kept_for_a_role(self):
		self.assertEqual([t["name"] for t in run(["Sales Manager"])], ["Everyone"])

	def test_a_tab_that_points_at_another_site_or_is_not_well_formed_is_left_out(self):
		names = [t["name"] for t in run(["Sales Representative"])]
		for left_out in ("Elsewhere", "Protocol", "NoLabel"):
			self.assertNotIn(left_out, names)

	def test_the_tabs_of_another_doctype_are_not_mixed_in(self):
		self.assertEqual([t["name"] for t in run(["Sales Manager"], doctype="CRM Deal")], ["Deal"])

	def test_an_account_that_may_not_read_the_document_gets_nothing(self):
		self.assertEqual(run(["Sales Representative"], can_read=False), [])

	def test_a_site_where_no_app_adds_a_tab_gets_none(self):
		self.assertEqual(run(["Sales Representative"], hooks={}), [])
		self.assertEqual(run(["Sales Representative"], hooks=None), [])

	def test_the_answer_holds_the_name_the_label_and_the_path_and_nothing_else(self):
		(first, *_rest) = run(["Sales Representative"])
		self.assertEqual(set(first), {"name", "label", "url"})
		self.assertEqual(first["url"], "/representants?embed=questions#/lead/{docname}")


PAGES = [
	{
		"name": "funnel",
		"label": "Funnel",
		"url": "/representants?embed=team#/funnel",
		"icon": "lucide-filter",
		"roles": ["Sales Manager"],
	},
	{"name": "everyone", "label": "Everyone", "url": "/page"},
	{"name": "elsewhere", "label": "Elsewhere", "url": "https://example.com/x", "roles": ["Sales Manager"]},
	{"name": "protocol", "label": "Protocol", "url": "//example.com/x"},
	{"label": "NoName", "url": "/x"},
	"not a dict",
]


def run_pages(roles, hooks=PAGES):
	with (
		mock.patch.object(frappe, "get_hooks", return_value=hooks),
		mock.patch.object(frappe, "get_roles", return_value=["All", "Guest", *roles]),
		mock.patch.object(extension_tabs, "_", side_effect=lambda text: text),
	):
		return getattr(extension_tabs.get_pages, "__wrapped__", extension_tabs.get_pages)()


class TestExtensionPages(unittest.TestCase):
	def test_a_manager_sees_the_pages_for_its_role_and_those_for_everybody_in_the_order_given(self):
		self.assertEqual([p["name"] for p in run_pages(["Sales Manager"])], ["funnel", "everyone"])

	def test_the_others_do_not_see_a_page_kept_for_a_role(self):
		self.assertEqual([p["name"] for p in run_pages(["Sales User"])], ["everyone"])

	def test_a_page_that_points_at_another_site_or_is_not_well_formed_is_left_out(self):
		names = [p["name"] for p in run_pages(["Sales Manager"])]
		for left_out in ("elsewhere", "protocol"):
			self.assertNotIn(left_out, names)
		self.assertEqual(len(names), 2)

	def test_a_site_where_no_app_adds_a_page_gets_none(self):
		self.assertEqual(run_pages(["Sales Manager"], hooks=[]), [])
		self.assertEqual(run_pages(["Sales Manager"], hooks=None), [])

	def test_the_answer_holds_the_name_the_label_the_path_and_the_icon_and_nothing_else(self):
		(first, *_rest) = run_pages(["Sales Manager"])
		self.assertEqual(set(first), {"name", "label", "url", "icon"})
		self.assertEqual(first["icon"], "lucide-filter")
		self.assertEqual(run_pages(["Sales Manager"])[1]["icon"], "")


if __name__ == "__main__":
	unittest.main()

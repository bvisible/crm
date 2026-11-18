# //// Neoffice — added file (no upstream equivalent)
# //// Proves `crm.api.session.search_crm_users`: the search behind « Attribuer à » and the owner fields lists the CRM's users (a
# //// manager could pick nobody but themselves while it asked Frappe's own user search), narrowed by the text and by the screen's list.

import unittest
from unittest import mock

import frappe

from crm.api import session

USERS = [
	frappe._dict(name="manager@example.com", full_name="Marie Manager"),
	frappe._dict(name="rep@example.com", full_name="Camille Rey"),
	frappe._dict(name="other@example.com", full_name=""),
]


def search(txt="", filters=None, page_length=20, users=USERS, allowed=True):
	flags = mock.Mock(side_effect=None if allowed else frappe.PermissionError)
	with (
		mock.patch.object(session, "get_session_role_flags", flags),
		mock.patch.object(session, "get_users", return_value=(users, users)),
	):
		# the function under the type check of `frappe.whitelist`, which asks the request for its flags: nothing here is a request
		return getattr(session.search_crm_users, "__wrapped__", session.search_crm_users)(txt, filters, page_length)


class TestSearchCrmUsers(unittest.TestCase):
	def test_every_user_of_the_crm_is_listed_in_the_shape_of_the_link_search(self):
		found = search()
		self.assertEqual([u["value"] for u in found], ["manager@example.com", "rep@example.com", "other@example.com"])
		self.assertEqual(found[1], {"value": "rep@example.com", "description": "Camille Rey"})

	def test_an_account_with_no_full_name_is_described_by_its_name(self):
		self.assertEqual(search()[2]["description"], "other@example.com")

	def test_the_text_matches_the_name_or_the_full_name_whatever_its_case(self):
		self.assertEqual([u["value"] for u in search("camille")], ["rep@example.com"])
		self.assertEqual([u["value"] for u in search("MANAGER@")], ["manager@example.com"])

	def test_the_list_of_the_screen_only_narrows_the_answer(self):
		filters = {"name": ["in", ["rep@example.com", "nobody@example.com"]], "ignore_user_type": 1}
		self.assertEqual([u["value"] for u in search(filters=filters)], ["rep@example.com"])

	def test_the_filters_may_come_as_text(self):
		found = search(filters='{"name": ["in", ["manager@example.com"]]}')
		self.assertEqual([u["value"] for u in found], ["manager@example.com"])

	def test_a_page_length_caps_the_answer(self):
		self.assertEqual(len(search(page_length=2)), 2)

	def test_an_account_outside_the_crm_gets_nothing_at_all(self):
		with self.assertRaises(frappe.PermissionError):
			search(allowed=False)

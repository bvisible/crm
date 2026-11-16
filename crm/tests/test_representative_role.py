# //// Neoffice — added file (no upstream equivalent)
# //// Proves the lines marked in `crm.utils`, `crm.api` and `crm.api.session`: the hub's commercial representatives hold a role of
# //// their own, `Sales Representative`, and the CRM reads it as a sales user (a sales agent limited to the leads they own or are
# //// assigned) without giving it the ERPNext `Sales User` role. Pure: the engine's roles are simulated.

import unittest
from unittest import mock

import frappe

from crm.utils import REPRESENTATIVE_ROLE, crm_roles, is_sales_user


def roles(*names):
	return mock.patch.object(frappe, "get_roles", return_value=["All", "Guest", *names])


def not_the_administrator():
	# `is_sales_user` first asks whether the session's user is the Administrator, which needs a session this pure test has not got
	return mock.patch("crm.utils.is_admin", return_value=False)


class TestRepresentativeRole(unittest.TestCase):
	def test_a_sales_representative_counts_as_a_sales_user(self):
		with roles(REPRESENTATIVE_ROLE), not_the_administrator():
			self.assertIn("Sales User", crm_roles("rep@example.com"))
			self.assertTrue(is_sales_user("rep@example.com"))

	def test_the_role_makes_neither_a_manager_nor_a_system_manager(self):
		with roles(REPRESENTATIVE_ROLE):
			found = crm_roles("rep@example.com")
		self.assertNotIn("Sales Manager", found)
		self.assertNotIn("System Manager", found)

	def test_the_roles_of_everyone_else_are_unchanged(self):
		for held in ((), ("Sales User",), ("Sales Manager",), ("System Manager",), ("Customer",)):
			with self.subTest(held), roles(*held):
				self.assertEqual(crm_roles("someone@example.com"), {"All", "Guest", *held})

	def test_an_account_with_no_sales_role_is_not_an_agent(self):
		with roles("Desk User"), not_the_administrator():
			self.assertFalse(is_sales_user("someone@example.com"))


if __name__ == "__main__":
	unittest.main()

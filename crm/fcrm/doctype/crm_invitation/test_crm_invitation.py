# Copyright (c) 2024, Frappe Technologies Pvt. Ltd. and Contributors
# See license.txt

from contextlib import contextmanager  # //// Neoffice — for the faked site name of the invitation tests (16.10)
from unittest.mock import patch

import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import add_days, now


class TestCRMInvitation(FrappeTestCase):
	def make_invitation(self, email="invitee@example.com", role="Sales User"):
		"""Create a Pending invitation without actually sending an email."""
		with patch.object(frappe, "sendmail"):
			return frappe.get_doc(
				doctype="CRM Invitation",
				email=email,
				role=role,
			).insert(ignore_permissions=True)

	def test_new_invitation_is_pending_with_key(self):
		invitation = self.make_invitation()
		self.assertEqual(invitation.status, "Pending")
		self.assertTrue(invitation.key)
		self.assertEqual(invitation.invited_by, frappe.session.user)

	def test_accept_pending_invitation(self):
		invitation = self.make_invitation()

		invitation.accept()

		self.assertEqual(invitation.status, "Accepted")
		self.assertTrue(invitation.accepted_at)
		self.assertTrue(frappe.db.exists("User", invitation.email))

	def test_accept_clears_key(self):
		"""The key is wiped after acceptance so the invite link cannot be reused."""
		invitation = self.make_invitation()

		invitation.accept()

		self.assertIsNone(invitation.key)
		self.assertFalse(frappe.db.get_value("CRM Invitation", invitation.name, "key"))

	def test_accept_already_accepted_raises(self):
		"""An already-accepted invitation cannot be accepted again."""
		invitation = self.make_invitation()
		invitation.accept()

		invitation.reload()
		with self.assertRaises(frappe.ValidationError):
			invitation.accept()

	def test_accept_expired_invitation_raises(self):
		invitation = self.make_invitation()
		invitation.status = "Expired"
		invitation.save(ignore_permissions=True)

		with self.assertRaises(frappe.ValidationError):
			invitation.accept()

	def test_accept_reports_newly_created_user(self):
		invitation = self.make_invitation(email="brand-new@example.com")

		self.assertTrue(invitation.accept())
		self.assertEqual(frappe.db.get_value("User", invitation.email, "default_app"), "crm")

	def test_accept_reports_existing_user(self):
		frappe.get_doc(
			doctype="User",
			user_type="System User",
			email="already-there@example.com",
			send_welcome_email=0,
			first_name="Already There",
		).insert(ignore_permissions=True)
		invitation = self.make_invitation(email="already-there@example.com")

		self.assertFalse(invitation.accept())

	def test_accept_invitation_sends_new_user_to_set_password(self):
		"""A new user must set a password instead of being logged in directly."""
		from crm.api import accept_invitation

		invitation = self.make_invitation(email="new-invitee@example.com")

		accept_invitation(key=invitation.key)

		self.assertEqual(frappe.local.response["type"], "redirect")
		self.assertIn("/update-password?key=", frappe.local.response["location"])

	def test_accept_invitation_logs_in_existing_user(self):
		"""An existing user already has a password, so log them straight in."""
		from crm.api import accept_invitation

		frappe.get_doc(
			doctype="User",
			user_type="System User",
			email="existing-invitee@example.com",
			send_welcome_email=0,
			first_name="Existing Invitee",
		).insert(ignore_permissions=True)
		invitation = self.make_invitation(email="existing-invitee@example.com")

		with patch.object(frappe.local, "login_manager", create=True) as login_manager:
			accept_invitation(key=invitation.key)

		login_manager.login_as.assert_called_once_with("existing-invitee@example.com")
		self.assertEqual(frappe.local.response["location"], "/crm")

	def test_desk_accept_mails_new_user_a_set_password_link(self):
		invitation = self.make_invitation(email="desk-invitee@example.com")

		with patch("frappe.core.doctype.user.user.User.send_welcome_mail_to_user") as welcome_mail:
			invitation.accept_invitation()

		welcome_mail.assert_called_once()

	def test_desk_accept_does_not_mail_existing_user(self):
		frappe.get_doc(
			doctype="User",
			user_type="System User",
			email="desk-existing@example.com",
			send_welcome_email=0,
			first_name="Desk Existing",
		).insert(ignore_permissions=True)
		invitation = self.make_invitation(email="desk-existing@example.com")

		with patch("frappe.core.doctype.user.user.User.send_welcome_mail_to_user") as welcome_mail:
			invitation.accept_invitation()

		welcome_mail.assert_not_called()

	def test_expire_invitations_expires_old_pending_invites(self):
		from crm.fcrm.doctype.crm_invitation.crm_invitation import expire_invitations

		invitation = self.make_invitation(email="stale@example.com")
		frappe.db.set_value(
			"CRM Invitation", invitation.name, "creation", add_days(now(), -4), update_modified=False
		)

		expire_invitations()

		self.assertEqual(frappe.db.get_value("CRM Invitation", invitation.name, "status"), "Expired")

	def test_accept_grants_role_to_user(self):
		invitation = self.make_invitation(email="manager@example.com", role="Sales Manager")

		invitation.accept()

		user = frappe.get_doc("User", invitation.email)
		user_roles = {r.role for r in user.roles}
		self.assertIn("Sales Manager", user_roles)
		self.assertIn("Sales User", user_roles)

	# //// Neoffice — the invitation e-mail names the product the site calls itself, not "Frappe CRM" (15.10).
	@contextmanager
	def _site_named(self, app_name):
		"""System Settings.app_name reads `app_name`, and ONLY that key does.

		The framework asks the same function for the time zone and for more: a constant answer for every key made the
		frappe v16 job of the Server workflow fail on a time zone called "Atelier" (`No module named 'tzdata'`, 16.10).
		"""
		real_get_system_settings = frappe.get_system_settings

		def get_system_settings(key):
			return app_name if key == "app_name" else real_get_system_settings(key)

		with patch("frappe.get_system_settings", side_effect=get_system_settings):
			yield

	def _sent_invitation(self, app_name):
		# //// Neoffice — the name is faked through `_site_named`, which leaves every other setting alone (16.10).
		with patch.object(frappe, "sendmail") as sendmail, self._site_named(app_name):
			frappe.get_doc(doctype="CRM Invitation", email="brand@example.com", role="Sales User").insert(
				ignore_permissions=True
			)
		return sendmail.call_args.kwargs

	# //// Neoffice — pins the fake: while the name is faked, the time zone stays the real one (16.10).
	def test_a_faked_site_name_does_not_leak_into_the_other_system_settings(self):
		with self._site_named("Atelier"):
			self.assertEqual(frappe.get_system_settings("app_name"), "Atelier")
			self.assertNotEqual(frappe.get_system_settings("time_zone"), "Atelier")

	def test_invitation_names_neoffice_when_the_site_still_has_a_framework_name(self):
		for framework_name in ("Frappe", "ERPNext", "", None):
			with self.subTest(app_name=framework_name):
				sent = self._sent_invitation(framework_name)
				self.assertEqual(sent["subject"], "You have been invited to join Neoffice CRM")
				self.assertEqual(sent["args"]["title"], "Neoffice CRM")
				# //// Neoffice — no row to delete between the rounds: the class is rolled back at its end (16.10).

	def test_invitation_names_the_name_the_site_chose(self):
		sent = self._sent_invitation("Atelier")
		self.assertEqual(sent["subject"], "You have been invited to join Atelier CRM")

	def test_invitation_body_says_the_title_and_never_frappe(self):
		html = frappe.get_template("templates/emails/crm_invitation.html").render(
			{"title": "Neoffice CRM", "invite_link": "https://example.com/accept"}
		)
		self.assertIn("You have been invited to join Neoffice CRM", html)
		self.assertNotIn("Frappe", html)

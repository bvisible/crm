# Copyright (c) 2026, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
# //// Neoffice — added file (no upstream equivalent): the tests of two changes of our fork (maintenance#3399), offline.

"""A record saved by someone else during its enrichment, and an image fetched through the crawler's guard.

Pinned here:
  * ``run_enrichment`` reads, maps and saves the record again when it moved between the read and the save (a lead the
    representative keeps typing in): the run is Completed, the mapping decides on what the record holds now, and after
    ``SAVE_TRIES`` the run fails as before;
  * ``http.fetch_image`` returns the bytes of an image through the same SSRF guard as ``fetch``: a private address,
    first or after a redirect, is refused before any connection; a body that is not an image, or bigger than its
    limit, is refused rather than cut.

Fully offline: no site, no network (the guard's resolution and the pinned connection are replaced).
"""

from __future__ import annotations

import unittest
from types import SimpleNamespace
from unittest import mock

import frappe

from crm.domain_enrichment import http, tasks
from crm.domain_enrichment.mapper import FieldChange


def change(value="https://example.com/logo.png"):
	return FieldChange("organization_logo", None, value, "Logo")


class Record:
	"""A record whose save meets someone else's save `mismatches` times, then passes."""

	saved = 0

	def __init__(self, mismatches):
		self.mismatches = mismatches
		self.check_permission = mock.Mock()

	def save(self):
		if self.mismatches:
			raise frappe.TimestampMismatchError("Document has been modified after you have opened it")
		Record.saved += 1


class TheRecordMovedMeanwhile(unittest.TestCase):
	def run_it(self, mismatches):
		"""`mismatches` saves meet someone else's; each read returns a record that knows how many are left."""
		reads = []

		def get_doc(doctype, name):
			record = Record(1 if len(reads) < mismatches else 0)
			reads.append(record)
			return record

		Record.saved = 0
		written = mock.Mock(return_value="RUN-1")
		db = mock.MagicMock()
		rollback = db.rollback
		with (
			mock.patch.object(tasks, "get_config", return_value=SimpleNamespace()),
			mock.patch.object(tasks, "run_pipeline", return_value=SimpleNamespace(notes=[], flat=lambda: {})),
			mock.patch.object(tasks.frappe, "get_doc", side_effect=get_doc),
			mock.patch.object(tasks.frappe, "db", db),
			mock.patch.object(tasks.frappe.utils, "now_datetime", return_value="2026-11-25 20:00:00"),
			mock.patch.object(tasks.frappe, "log_error"),
			mock.patch.object(tasks.frappe, "get_traceback", return_value="trace"),
			mock.patch.object(tasks.frappe, "_", side_effect=lambda text: text),
			mock.patch.object(
				tasks, "apply_to_document", side_effect=lambda doc, result, cfg: [change()]
			) as mapped,
			mock.patch.object(tasks, "write_run", written),
			mock.patch.object(tasks, "_publish"),
			mock.patch.object(tasks, "capture"),
		):
			tasks.run_enrichment("CRM Lead", "CRM-LEAD-1", "https://example.com", user="rep@example.com")
		return reads, written.call_args.kwargs["status"], rollback, mapped

	def test_a_save_that_met_someone_elses_reads_the_record_again_and_completes(self):
		reads, status, rollback, mapped = self.run_it(mismatches=1)
		self.assertEqual(status, "Completed")
		self.assertEqual(len(reads), 2)
		self.assertEqual(Record.saved, 1)
		rollback.assert_called_once_with()
		# The mapping decides on the record as it stands now, not on the one first read
		self.assertIs(mapped.call_args_list[-1].args[0], reads[-1])

	def test_a_record_that_keeps_moving_fails_the_run_as_before(self):
		reads, status, _rollback, _mapped = self.run_it(mismatches=tasks.SAVE_TRIES)
		self.assertEqual(status, "Failed")
		self.assertEqual(len(reads), tasks.SAVE_TRIES)
		self.assertEqual(Record.saved, 0)

	def test_a_record_that_did_not_move_is_read_once(self):
		reads, status, rollback, _mapped = self.run_it(mismatches=0)
		self.assertEqual(status, "Completed")
		self.assertEqual(len(reads), 1)
		rollback.assert_not_called()


class Response:
	def __init__(
		self, status=200, content_type="image/png", body=b"\x89PNG\r\n\x1a\n" + b"0" * 100, location=None
	):
		self.status_code = status
		self.headers = {"Content-Type": content_type}
		if location:
			self.headers["Location"] = location
		self.is_redirect = location is not None
		self.is_permanent_redirect = False
		self.body = body
		self.closed = False

	def iter_content(self, chunk_size=16_384):
		for start in range(0, len(self.body), chunk_size):
			yield self.body[start : start + chunk_size]

	def close(self):
		self.closed = True


class TheImageFetched(unittest.TestCase):
	def fetch(self, responses, addresses=None, max_bytes=1000):
		"""`addresses`: host -> the address its name resolves to (public unless said)."""
		addresses = addresses or {}

		def resolve(host):
			return [addresses.get(host, "93.184.216.34")]

		pinned = mock.Mock(side_effect=list(responses))
		with (
			mock.patch.object(http, "_resolve_ips", side_effect=resolve),
			mock.patch.object(http, "_pinned_get", pinned),
		):
			content, error = http.fetch_image("https://prospect.example/logo.png", max_bytes=max_bytes)
		return content, error, pinned

	def test_an_image_comes_back_as_its_bytes(self):
		image = Response()
		content, error, _pinned = self.fetch([image])
		self.assertEqual(error, "")
		self.assertEqual(content, image.body)
		self.assertTrue(image.closed)

	def test_a_private_address_is_refused_before_any_connection(self):
		content, error, pinned = self.fetch([], addresses={"prospect.example": "169.254.169.254"})
		self.assertEqual(content, b"")
		self.assertIn("SSRF", error)
		pinned.assert_not_called()

	def test_a_redirect_to_a_private_address_is_refused_at_its_hop(self):
		hop = Response(status=302, location="http://inside.example/secret")
		content, error, pinned = self.fetch([hop], addresses={"inside.example": "10.0.0.5"})
		self.assertEqual(content, b"")
		self.assertIn("SSRF", error)
		self.assertEqual(pinned.call_count, 1)

	def test_a_page_that_is_no_image_is_refused(self):
		content, error, _pinned = self.fetch(
			[Response(content_type="text/html; charset=utf-8", body=b"<html>")]
		)
		self.assertEqual(content, b"")
		self.assertIn("not an image", error)

	def test_an_image_bigger_than_its_limit_is_refused_not_cut(self):
		content, error, _pinned = self.fetch([Response(body=b"0" * 5000)], max_bytes=1000)
		self.assertEqual(content, b"")
		self.assertIn("bigger than 1000", error)

	def test_an_answer_that_is_no_success_is_refused(self):
		content, error, _pinned = self.fetch([Response(status=404, content_type="text/html")])
		self.assertEqual((content, error), (b"", "status 404"))


if __name__ == "__main__":
	unittest.main()

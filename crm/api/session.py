import frappe
from frappe import _

# //// Neoffice — the hub's sales representative is a CRM user and a sales agent, see `crm.utils.crm_roles`
from crm.utils import REPRESENTATIVE_ROLE, crm_roles

CRM_ALLOWED_ROLES = ["System Manager", "Sales Manager", "Sales User"]
# //// Neoffice — the accounts that hold one of these roles are the CRM's users (a sales representative is one, see `crm.utils.crm_roles`)
CRM_USER_ROLES = [*CRM_ALLOWED_ROLES, REPRESENTATIVE_ROLE]


def get_session_role_flags():
	# //// Neoffice — a sales representative is read as a sales user (see `crm.utils.crm_roles`)
	roles = crm_roles()

	if not roles.intersection(set(CRM_ALLOWED_ROLES)):
		frappe.throw(_("You are not permitted to access CRM resources."), frappe.PermissionError)

	return {
		"is_system_manager": "System Manager" in roles,
		"is_sales_manager": "Sales Manager" in roles and "System Manager" not in roles,
		"is_sales_user": "Sales User" in roles
		and "Sales Manager" not in roles
		and "System Manager" not in roles,
	}


USER_FIELDS = [
	"name",
	"email",
	"enabled",
	"user_image",
	"first_name",
	"last_name",
	"full_name",
	"user_type",
	"language",
	"crm_availability",
	"crm_availability_changed_on",
]


@frappe.whitelist()
def get_users(include_all: bool = False):
	"""Return (users, crm_users) for the CRM frontend.

	By default (`include_all=False`) the User query is filtered at SQL level
	to just users with CRM roles — typically a handful of rows. This unblocks
	the UI on initial load even on sites with hundreds of thousands of users.

	When `include_all=True` and the session has System Manager, the full
	enabled user list is returned. The frontend uses this path for a
	non-blocking background fetch that populates name/avatar info for
	non-CRM users referenced in CRM activity. Non-System-Manager sessions
	cannot escalate by passing this param.
	"""
	session_roles = get_session_role_flags()

	# Param arrives as a string from the HTTP layer; coerce.
	if isinstance(include_all, str):
		include_all = include_all.lower() in ("1", "true", "yes")
	if not session_roles["is_system_manager"]:
		include_all = False

	# Always need the CRM user name set — used both as the filter for the
	# fast path and as the membership check on the full path.
	crm_user_names = set(
		frappe.get_all(
			"Has Role",
			# //// Neoffice — the CRM's users include the sales representatives (CRM_USER_ROLES)
			filters={"parenttype": "User", "role": ["in", CRM_USER_ROLES]},
			pluck="parent",
			distinct=True,
		)
	)
	crm_user_names.add("Administrator")

	user_filters = {"enabled": 1}
	if not include_all:
		user_filters["name"] = ["in", list(crm_user_names)]

	users = frappe.qb.get_query(
		"User",
		fields=USER_FIELDS,
		order_by="full_name asc",
		filters=user_filters,
	).run(as_dict=1)

	if not users:
		return [], []

	system_language = frappe.db.get_single_value("System Settings", "language")
	session_user = frappe.session.user

	# Has Role lookup — restrict by parent on the fast path (tiny IN list);
	# unfiltered scan on the full path because the IN list would otherwise
	# carry every enabled user name (see commit dropping IN-list filters).
	if include_all:
		role_filters = {"parenttype": "User"}
	else:
		role_filters = {"parenttype": "User", "parent": ["in", list(crm_user_names)]}
	role_rows = frappe.get_all("Has Role", filters=role_filters, fields=["parent", "role"])
	roles_by_user = {}
	for row in role_rows:
		roles_by_user.setdefault(row.parent, []).append(row.role)

	# Telephony agent table is tiny on any real site; full pluck is cheaper
	# than serializing an IN list and gives identical results.
	telephony_agents = set(frappe.get_all("CRM Telephony Agent", pluck="user"))

	role_priority = ("System Manager", "Sales Manager", "Sales User", "Guest")
	crm_users = []

	for user in users:
		if session_user == user.name:
			user.session_user = True

		# Administrator has every role implicitly via frappe.get_roles() but
		# its Has Role child table is not guaranteed to contain System Manager
		# on every install — special-case it to avoid locking the admin out.
		if user.name == "Administrator":
			user.roles = ["System Manager", "All"]
			user.role = "System Manager"
		else:
			# Mirror frappe.get_roles() which appends implicit "All" and "Guest"
			user.roles = [*roles_by_user.get(user.name, []), "All", "Guest"]
			user.role = ""
			for role in role_priority:
				if role in user.roles:
					user.role = role
					break
			# //// Neoffice — a sales representative is a sales user for the screen (it reads `user.role`), nothing above. `Guest`
			# //// is the last of `role_priority`, so every account ends with it: it is the absence of a CRM role, not a role.
			if user.role in ("", "Guest") and REPRESENTATIVE_ROLE in user.roles:
				user.role = "Sales User"

		user.is_telephony_agent = user.name in telephony_agents
		user.language = user.language or system_language

		if user.role in CRM_ALLOWED_ROLES:
			crm_users.append(user)

	if not include_all:
		# Fast path — both positions are the CRM users.
		return crm_users, crm_users

	return users, crm_users


# //// Neoffice — added: the user search of the CRM's assignment box and owner fields. They asked `frappe.desk.search.search_link` for
# //// the CRM's users, and Frappe answers a desk user who may not read the User doctype with the account itself and nobody else: a
# //// manager could assign a prospect to no representative (« Attribuer à » listed only the manager, 18.11). The CRM's users are what
# //// `get_users` already hands every CRM account, so the same list is searched here, in the shape of `search_link`.
@frappe.whitelist()
def search_crm_users(  # permission-check: ok the CRM's own role check, `get_session_role_flags`, comes first
	txt: str = "", filters=None, page_length: int = 20
) -> list:
	"""The CRM's users whose name or full name contains `txt`: [{value, description}], as `search_link` answers.

	Only an account of the CRM may ask (`get_users` refuses the others), and `filters` can only narrow the list: a `name in [...]`
	given by the screen keeps the users named there.
	"""
	get_session_role_flags()
	_users, crm_users = get_users()
	filters = frappe.parse_json(filters) if filters else {}
	names = filters.get("name") if isinstance(filters, dict) else None
	allowed = set(names[1]) if isinstance(names, (list, tuple)) and len(names) == 2 and names[0] == "in" else None
	query = (txt or "").strip().lower()
	found = []
	for user in crm_users:
		if allowed is not None and user.name not in allowed:
			continue
		if query and query not in user.name.lower() and query not in (user.full_name or "").lower():
			continue
		found.append({"value": user.name, "description": user.full_name or user.name})
	return found[: int(page_length or 20)]


@frappe.whitelist()
def get_user_info(users: str | list):
	"""Resolve display info for a batch of User names.

	Used by the frontend to fill in name/avatar info for non-CRM users
	referenced in CRM activity (comment authors, doc owners, etc.) when
	the background full-list fetch has not yet landed. Gated behind a
	CRM role; capped at 200 names per call to limit enumeration cost.
	"""
	get_session_role_flags()

	if isinstance(users, str):
		users = frappe.parse_json(users)
	if not users:
		return []

	return frappe.get_all(
		"User",
		filters={"name": ["in", list(users)[:200]]},
		fields=["name", "email", "full_name", "user_image", "user_type"],
	)


@frappe.whitelist()
def get_organizations():
	get_session_role_flags()

	organizations = frappe.qb.get_query(
		"CRM Organization",
		fields=["*"],
		order_by="name asc",
		distinct=True,
	).run(as_dict=1)

	return organizations

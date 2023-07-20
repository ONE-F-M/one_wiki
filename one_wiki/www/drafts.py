import frappe
from frappe import _
from frappe.utils.data import cint

from wiki.wiki.doctype.wiki_page.wiki_page import get_open_contributions


def get_context(context):
	context.pilled_title = "My Drafts"
	context.no_cache = 1
	value =  frappe.cache().get_value(f'wiki_language_{frappe.session.user}')
	value = 'en' if not value else value
	context.wiki_language = value
	context.no_sidebar = 1
	context.contributions = get_user_drafts(0, 10)
	context = context.update(
		{
			"post_login": [
				{"label": _("My Account"), "url": "/me"},
				{"label": _("Logout"), "url": "/?cmd=web_logout"},
				{
					"label": _("My Contributions ") + get_open_contributions(),
					"url": "/contributions",
				},
			]
		}
	)

	return context

@frappe.whitelist()
def get_drafts(start, limit):
	return {"contributions": get_user_drafts(start, limit)}


def get_user_drafts(start, limit):
	"""
		Check if the user has the wiki manager role then show all draft wiki pages, if the user
		 does not have the role then show only pages created by the user or where the user is set as 
		approver.
	"""
	drafts = []
	if "Wiki Manager" not in frappe.get_roles(frappe.session.user):
		wiki_page_patches = frappe.get_list(
			"Wiki Page Patch",
			["message", "status", "name", "wiki_page", "modified", "new", "new_sidebar_group"],
			order_by="modified desc",
			start=cint(start),
			limit=cint(limit),
			filters=[["status", "=", "Draft"], ["owner", "=", frappe.session.user]],
		)
		wiki_page_patches += frappe.get_list(
			"Wiki Page Patch",
			["message", "status", "name", "wiki_page", "modified", "new", "new_sidebar_group"],
			order_by="modified desc",
			start=cint(start),
			limit=cint(limit),
			filters=[["status", "=", "Draft"], ["approved_by", "=", frappe.session.user]],
		)
	else:
		wiki_page_patches = frappe.get_list(
			"Wiki Page Patch",
			["message", "status", "name", "wiki_page", "modified", "new", "new_sidebar_group"],
			order_by="modified desc",
			start=cint(start),
			limit=cint(limit),
			filters=[["status", "=", "Draft"]],
		)
	for wiki_page_patch in wiki_page_patches:
		route = frappe.db.get_value("Wiki Page", wiki_page_patch.wiki_page, "route")
		if wiki_page_patch.new:
			wiki_page_patch.edit_link = (
				f"/{route}?newWiki={wiki_page_patch.new_sidebar_group}&wikiPagePatch={wiki_page_patch.name}"
			)
		else:
			wiki_page_patch.edit_link = f"/{route}?editWiki=1&wikiPagePatch={wiki_page_patch.name}"
		wiki_page_patch.color = "orange"
		wiki_page_patch.modified = frappe.utils.pretty_date(wiki_page_patch.modified)
		drafts.extend([wiki_page_patch])

	return drafts




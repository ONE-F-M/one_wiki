import re
import frappe
from frappe.desk.form.load import get_comments
from wiki.wiki.doctype.wiki_page.wiki_page import get_open_contributions
from wiki.wiki.doctype.wiki_page.wiki_page import get_open_drafts
from frappe import _
from frappe.utils.jinja_globals import is_rtl
from one_wiki.overrides.wiki_page import is_permitted

def get_context(context):
	context.no_cache = 1
	context.show_approval = False
	frappe.form_dict.edit = True
	
	wiki_page_name = frappe.db.get_value("Wiki Page",
		filters={'route':frappe.form_dict.wiki_page},
		fieldname='name')
	context.doc = frappe.get_doc("Wiki Page", wiki_page_name)

	context.doc.verify_permission("read")

	try:
		boot = frappe.sessions.get()
	except Exception as e:
		boot = frappe._dict(status="failed", error=str(e))
		print(frappe.get_traceback())

	boot_json = frappe.as_json(boot)

	# remove script tags from boot
	boot_json = re.sub(r"\<script[^<]*\</script\>", "", boot_json)

	# TODO: Find better fix
	boot_json = re.sub(r"</script\>", "", boot_json)

	context.boot = boot_json
	context.frappe_version = frappe.__version__
	wiki_settings = frappe.get_single("Wiki Settings")
	context.banner_image = wiki_settings.logo
	context.script = wiki_settings.javascript
	context.docs_search_scope = ""
	can_edit = frappe.session.user != "Guest"
	context.can_edit = can_edit
	context.show_my_account = False
	context.doc.set_breadcrumbs(context)
	context.lang = frappe.local.lang
	context.layout_direction = "rtl" if is_rtl() else "ltr"
	if not can_edit:
		context.doc.redirect_to_login("edit")

	if  "ar" in context.lang :
		context.title =  context.doc.title + " التحرير "
	else:
		context.title = "Editing " + context.doc.title

	if frappe.form_dict.wiki_page_patch:
		context.wiki_page_patch = frappe.form_dict.wiki_page_patch
		if frappe.get_value("Wiki Page Patch",frappe.form_dict.wiki_page_patch,'approved_by') == frappe.session.user:
			context.show_approval = True
		context.doc.content = frappe.db.get_value(
			"Wiki Page Patch", context.wiki_page_patch, "new_code"
		)
		context.comments = get_comments(
			"Wiki Page Patch", frappe.form_dict.wiki_page_patch, "Comment"
		)
		context.sidebar_edited = frappe.db.get_value(
			"Wiki Page Patch", context.wiki_page_patch, "sidebar_edited"
		)
		context.new_sidebar_items = frappe.db.get_value(
			"Wiki Page Patch", context.wiki_page_patch, "new_sidebar_items"
		)
	context.lang_ = 'عربي' if context.lang == 'ar' else 'en'
	context.content_md = context.doc.content
	context.content_html = frappe.utils.md_to_html(context.doc.content)
	context.sidebar_items, context.docs_search_scope = context.doc.get_sidebar_items(
		context
	)

	context = context.update(
		{
			"post_login": [
				{"label": _("My Account"), "url": "/me"},
				{"label": _("Logout"), "url": "/?cmd=web_logout"},
				{
					"label": _("Contributions ") + get_open_contributions(),
					"url": "/contributions",
				},
				{
					"label": _("My Drafts ") + get_open_drafts(),
					"url": "/drafts",
				},
			]
		}
	)
	context.is_permitted = is_permitted(frappe.session.user)
	return context

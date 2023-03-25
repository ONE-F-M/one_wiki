import frappe
import re
from frappe.utils.jinja_globals import is_rtl

@frappe.whitelist()
def change_language(lang,user=None):
	# change the language of a user
	try:
		if not user:
			user = frappe.session.user
		frappe.set_value('User',user,'language',lang)
		return True
	except:
		frappe.log_error(frappe.get_traceback(),"Error while changing language")
		return False


def md_to_html(markdown_text: str):
	from markdown2 import MarkdownError
	from markdown2 import markdown as _markdown
	name = re.findall(r'[\u0600-\u06FF]+',markdown_text)

	if name:
		markdown_text = '<p style="text-align: right;">'+markdown_text+'</p>'
	extras = {
		"fenced-code-blocks": None,
		"tables": None,
		"header-ids": None,
		"toc": None,
		"highlightjs-lang": None,
		"html-classes": {"table": "table table-bordered", "img": "screenshot",},
	}

	try:
		return _markdown(markdown_text or "", extras=extras)
	except MarkdownError:
		pass

def update_context_(me):
	me.context.doc = me.doc
	me.context.update(me.context.doc.as_dict())
	me.context.update(me.context.doc.get_page_info())
	me.template_path = me.context.template or me.template_path
	me.context.lang = frappe.local.lang
	me.context.lang_ = 'عربي' if me.context.lang == 'ar' else 'en'
	if hasattr(me.doc, "get_context"):
		ret = me.doc.get_context(me.context)
		if ret:
			me.context.update(ret)
	for prop in ("no_cache", "sitemap"):
		if prop not in me.context:
			me.context[prop] = getattr(me.doc, prop, False)
	# if not me.template_path:
	if me.doctype == 'Wiki Page':
		me.template_path = 'one_wiki/templates/wiki_page/templates/wiki_page.html'
	else:
		me.template_path = me.context.doc.meta.get_web_template()
	if not me.template_path:
			me.template_path = me.context.doc.meta.get_web_template()
	






@frappe.whitelist()
def get_context(doc, context):
	context.no_cache = 1
	doc.verify_permission("read")
	doc.set_breadcrumbs(context)
	wiki_settings = frappe.get_single("Wiki Settings")
	context.navbar_search = wiki_settings.add_search_bar
	context.banner_image = wiki_settings.logo
	context.script = wiki_settings.javascript
	context.docs_search_scope = doc.get_docs_search_scope()
	
	context.metatags = {
		"title": doc.title, 
		"description": doc.meta_description,
		"keywords": doc.meta_keywords,
		"image": doc.meta_image,
		"og:image:width": "1200",
		"og:image:height": "630",
		}
	context.last_revision = doc.get_last_revision()
	context.number_of_revisions = frappe.db.count(
		"Wiki Page Revision Item", {"wiki_page": doc.name}
	)
	html = md_to_html(doc.content)
	context.content = html
	context.page_toc_html = html.toc_html
	context.show_sidebar = True
	context.hide_login = True
	context.lang = frappe.local.lang
	context.lang_ = 'عربي' if context.lang == 'ar' else 'en'
	context.no_cache = 1
	context.can_edit_page = 0
	if is_permitted(frappe.session.user):
		context.can_edit_page = 1
	

	context = context.update(
		{
			"post_login": [
				{"label": ("My Account"), "url": "/me"},
				{"label": ("Logout"), "url": "/?cmd=web_logout"},
				{
					"label": ("Contributions ") + get_open_contributions(),
					"url": "/contributions",
				},
				{
					"label": ("My Drafts ") + get_open_drafts(),
					"url": "/drafts",
				},
			]
		}
	)
	return context

def get_open_contributions():
	count = len(
		frappe.get_list("Wiki Page Patch", filters=[["status", "=", "Under Review"]],)
	)
	return f'<span class="count">{count}</span>'

def get_open_drafts():
	count = len(
		frappe.get_list("Wiki Page Patch", filters=[["status", "=", "Draft"], ["owner", '=', frappe.session.user]],)
	)
	return f'<span class="count">{count}</span>'

@frappe.whitelist()
def preview(content, name, new, type, diff_css=False):
	html = md_to_html(content)
	if new:
		return {"html": html}
	from ghdiff import diff

	old_content = frappe.db.get_value("Wiki Page", name, "content")
	diff = diff(old_content, content, css=diff_css)
	return {
		"html": html,
		"diff": diff,
		"orignal_preview": md_to_html(old_content),
	}
 
 
 
def is_permitted(user):
	"""
		Checks the Wiki Page Access table in ONEFM General settings page to confirm if the user has edit and creation access on the webform

		Args:
			user (str): Email address of user.
			Returns Boolean
 
	"""
	accepted_roles = frappe.get_doc("ONEFM General Setting",None).wiki_page_access
	if accepted_roles:
		roles_list = [i.role for i in accepted_roles]
		roles_intersection = [value for value in roles_list if value in frappe.get_roles(user)]
		if roles_intersection:
			return 1
		else:
			return 0



			
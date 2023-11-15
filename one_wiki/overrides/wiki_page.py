import re, frappe
from frappe import _
from frappe.utils.jinja_globals import is_rtl
from frappe.website.doctype.website_settings.website_settings import modify_header_footer_items
from frappe.utils.data import sbool
from wiki.wiki.doctype.wiki_page.wiki_page import *


class WikiPageOverride(WikiPage):
	
	@frappe.whitelist()
	def get_context(self, context):
		self.verify_permission("read")
		self.set_breadcrumbs(context)
		wiki_settings = frappe.get_single("Wiki Settings")
		context.navbar_search = wiki_settings.add_search_bar
		context.add_dark_mode = wiki_settings.add_dark_mode
		context.light_mode_logo = wiki_settings.logo
		context.dark_mode_logo = wiki_settings.dark_mode_logo
		context.script = wiki_settings.javascript
		context.wiki_search_scope = self.get_space_route()
		context.is_wiki_manager = has_wiki_manager_role()
		context.metatags = {
			"title": self.title,
			"description": self.meta_description,
			"keywords": self.meta_keywords,
			"image": self.meta_image,
			"og:image:width": "1200",
			"og:image:height": "630",
		}
		context.edit_wiki_page = frappe.form_dict.get("editWiki")
		context.new_wiki_page = frappe.form_dict.get("newWiki")
		context.last_revision = self.get_last_revision()
		patch_data = has_draft_patch(context.docname)
		if patch_data:
			context.existing_page_patch_title = patch_data.get('title')
			context.existing_page_patch_owner = patch_data.get('approved_by')
			context.existing_page_patch_url = patch_data.get('url')
		context.number_of_revisions = frappe.db.count(
			"Wiki Page Revision Item", {"wiki_page": self.name}
		)
		html = frappe.utils.md_to_html(self.content)
		context.content = html
		context.page_toc_html = (
			self.calculate_toc_html(html) if wiki_settings.enable_table_of_contents else None
		)

		revisions = frappe.db.get_all(
			"Wiki Page Revision",
			filters=[["wiki_page", "=", self.name]],
			fields=["content", "creation", "owner", "name", "raised_by", "raised_by_username"],
		)
		context.current_revision = revisions[0]
		if len(revisions) > 1:
			context.previous_revision = revisions[1]
		else:
			context.previous_revision = {"content": "<h3>No Revisions</h3>", "name": ""}
		context.lang = 'en' if self.language in ['English',None,''] else 'عربي' #defaults to english language
		wiki_lang = f'wiki_language_{frappe.session.user}'
		frappe.cache().set_value(wiki_lang,'en' if context.lang=='en' else 'ar')
		context.layout_direction = "rtl" if context.lang == 'ar'  else "ltr"
		context.show_sidebar = True
		context.hide_login = True
		context.name = self.name
		if (frappe.form_dict.editWiki or frappe.form_dict.newWiki) and frappe.form_dict.wikiPagePatch:
			context.can_approve = is_approver(frappe.form_dict.wikiPagePatch)
			(
				context.patch_new_code,
				context.patch_new_title,
				context.new_sidebar_group,
			) = frappe.db.get_value(
				"Wiki Page Patch",
				frappe.form_dict.wikiPagePatch,
				["new_code", "new_title", "new_sidebar_group"],
			)
		context = context.update(
			{
				"navbar_items": modify_header_footer_items(wiki_settings.navbar),
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
				],
			}
		)

	def get_sidebar_items(self):
		wiki_sidebar = frappe.get_doc("Wiki Space", {"route": self.get_space_route()}).wiki_sidebars
		sidebar = {}

		for sidebar_item in wiki_sidebar:
			wiki_page = frappe.get_doc("Wiki Page", sidebar_item.wiki_page)
			wiki_language = self.language or 'English'	
			if wiki_page.language == wiki_language:
				if sidebar_item.parent_label not in sidebar:
					sidebar[sidebar_item.parent_label] = [
						{
							"name": wiki_page.name,
							"type": "Wiki Page",
							"title": wiki_page.title,
							"route": wiki_page.route,
							"group_name": sidebar_item.parent_label,
						}
					]
				else:
					sidebar[sidebar_item.parent_label] += [
						{
							"name": wiki_page.name,
							"type": "Wiki Page",
							"title": wiki_page.title,
							"route": wiki_page.route,
							"group_name": sidebar_item.parent_label,
						}
					]

		return self.get_items(sidebar)



@frappe.whitelist()
def update(
	name,
	content,
	title,
	attachments="{}",
	message="",
	wiki_page_patch=None,
	new=False,
	new_sidebar="",
	new_sidebar_items="",
	draft=False,
	rejected = False,
	new_sidebar_group="",
):

	context = {"route": name}
	context = frappe._dict(context)
	content, file_ids = extract_images_from_html(content)

	new = sbool(new)
	draft = sbool(draft)

	status = "Draft" if draft else "Under Review"
	if wiki_page_patch:
		patch = frappe.get_doc("Wiki Page Patch", wiki_page_patch)
		patch.new_title = title
		patch.new_code = content
		patch.status = status
		patch.message = message
		patch.new = new
		patch.new_sidebar = new_sidebar
		patch.new_sidebar_items = new_sidebar_items
		patch.new_sidebar_group = new_sidebar_group
		patch.save()

	else:
		patch = frappe.new_doc("Wiki Page Patch")

		patch_dict = {
			"wiki_page": name,
			"status": status,
			"raised_by": frappe.session.user,
			"new_code": content,
			"message": message,
			"new": new,
			"new_title": title,
			"new_sidebar_items": new_sidebar_items,
			"new_sidebar_group": new_sidebar_group,
		}

		patch.update(patch_dict)

		patch.save()

		if file_ids:
			update_file_links(file_ids, patch.name)

	out = frappe._dict()

	if frappe.has_permission(doctype="Wiki Page Patch", ptype="submit", throw=False) and not draft:
		patch.approved_by = frappe.session.user
		patch.status = "Approved" if rejected in ['false',False] else "Rejected"
		patch.submit()
		out.approved = True

	frappe.db.commit()
	if draft:
		out.route = "drafts"
	elif not frappe.has_permission(doctype="Wiki Page Patch", ptype="submit", throw=False):
		out.route = "contributions"
	elif hasattr(patch, "new_wiki_page"):
		out.route = patch.new_wiki_page.route
	else:
		if patch.get('wiki_page_doc'):
			out.route = patch.wiki_page_doc.route
		else:
			out.route = frappe.get_value("Wiki Page",patch.wiki_page,'route')

	return out




@frappe.whitelist()
def fetch_cached_language():
	#fetch the cached wiki language for the user, defauklt to english if none is set
	value =  frappe.cache().get_value(f'wiki_language_{frappe.session.user}')
	return 'en' if not value else value

@frappe.whitelist()
def fetch_language(wiki):
	try:
		if wiki:
			patch_data = has_draft_patch(wiki)
			lang = frappe.get_value("Wiki Page",wiki,'language')
			lang = 'English' if lang in ['',None,'English'] else "Arabic"
			return {
				'language':lang,
				'url':patch_data.get('url'),
				'owner':patch_data.get('approved_by'),
				'title':patch_data.get('title'),
				
			}
	except:
		frappe.log_error(title="Fetching Wiki Page",message=frappe.get_traceback())


def has_wiki_manager_role():
	return 1 if "Wiki Manager" in frappe.get_roles(frappe.session.user) else 0


def is_approver(patch_name):
	#Returns a boolean if the current user is allowed to approve the wiki_page_patch.
	approver = frappe.get_value("Wiki Page Patch",patch_name,'approved_by')
	wiki_manager = "Wiki Manager" in frappe.get_roles(frappe.session.user)
	return True if approver == frappe.session.user or wiki_manager else  False

@frappe.whitelist()
def change_language(lang,user=None):
	# change the language of a user
	try:
		lang_ = 'en' if lang == 'English' else 'ar'
		if not user:
			user = frappe.session.user
		wiki_lang = f'wiki_language_{user}'
		frappe.cache().set_value(wiki_lang,lang_)
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
	
	
def update_context_(self):
	self.context.doc = self.doc
	self.context.update(self.context.doc.as_dict())
	self.context.update(self.context.doc.get_page_info())

	self.template_path = self.context.template or self.template_path

	if not self.template_path:
		if self.context.doc.doctype == 'Wiki Page':
			self.template_path = "one_wiki/templates/wiki_page/templates/wiki_page.html"
		else:
			self.template_path = self.context.doc.meta.get_web_template()

	if hasattr(self.doc, "get_context"):
		ret = self.doc.get_context(self.context)

		if ret:
			self.context.update(ret)

	for prop in ("no_cache", "sitemap"):
		if prop not in self.context:
			self.context[prop] = getattr(self.doc, prop, False)


	
	

@frappe.whitelist()
def update_patch(decision,wiki_patch):
	"""Update Wiki page patch based on the decision of the approver

	Args:
		decision (_type_): Approved or Rejected
		wiki_patch:Id of Wiki patch document
	"""
	try:
		if frappe.db.exists("Wiki Page Patch",wiki_patch):
			patch_doc = frappe.get_doc("Wiki Page Patch",wiki_patch)
			patch_doc.status = decision
			patch_doc.approved_by = frappe.session.user
			patch_doc.save()
			patch_doc.submit()
			route = frappe.get_value('Wiki Page',patch_doc.wiki_page,'route')
			if route:
				return route
	except:
		frappe.log_error(frappe.get_traceback(),"Error Submitting Patch")
		return ""

def has_draft_patch(wiki):
	#Checks if the wiki document has a draft wiki page patch
	route = frappe.db.get_value("Wiki Page", wiki, "route")
	wiki_page_patch = frappe.get_all("Wiki Page Patch",{'wiki_page':wiki,'docstatus':0,'new':0,'status':'Draft'},['new_title','name','approved_by'])
	if wiki_page_patch:
		edit_link = f"/{route}?editWiki=1&wikiPagePatch={wiki_page_patch[0].name}"
		return {
			'url':edit_link,
			'approved_by':wiki_page_patch[0].approved_by,
			'title':wiki_page_patch[0].new_title,
			
		}
	else:
		return {
			'url':'',
			'approved_by':'',
			'title':'',
		}



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
 

@frappe.whitelist()
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
		elif "Wiki Manager" in frappe.get_roles(user):
			return 1
		else:
			return 0
	else:
		return 0



			
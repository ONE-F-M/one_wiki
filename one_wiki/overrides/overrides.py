import frappe,random
import re
import os
from frappe.website.utils  import is_binary_file
from frappe.desk.form.assign_to import add
from wiki.wiki.doctype.wiki_page.wiki_page import extract_images_from_html,update_file_links
from frappe.website.utils import cleanup_page_name
# from frappe.website.website_generator import WebsiteGenerator





@frappe.whitelist(allow_guest=True)
def get_sidebar_for_page_(wiki_page):
	sidebar = []
	context = frappe._dict({})
	wiki_language = frappe.get_all("Wiki Page Patch",{'wiki_page':wiki_page},['wiki_language'])
	if wiki_language:
		context.wiki_language = wiki_language[0].get('wiki_language')
	if not context.wiki_language:
		#Get context from wiki page patch
		context.wiki_language = frappe.db.get_value("Wiki Page",wiki_page,'wiki_language')
	matching_pages = frappe.get_all("Wiki Page", {"name": wiki_page})
	if matching_pages:
		sidebar, _ = frappe.get_doc("Wiki Page", matching_pages[0].get("name")).get_sidebar_items(
			context
		)
	return sidebar

def get_sidebar_items_(self, context):
	sidebar = frappe.get_all(
		doctype="Wiki Sidebar Item",
		fields=["name", "parent"],
		filters=[["item", "=", self.name]],
	)
	sidebar_html = ""
	topmost = "/"
	if sidebar:
		sidebar_html, topmost = frappe.get_doc("Wiki Sidebar", sidebar[0].parent).get_items(lang=context.wiki_language)
	else:
		sidebar = frappe.db.get_single_value("Wiki Settings", "sidebar")
		if sidebar:

			sidebar_html, topmost = frappe.get_doc("Wiki Sidebar", sidebar).get_items(lang=context.wiki_language)

		else:
			sidebar_html = ""

	return sidebar_html, topmost



def get_items_(self,lang=None):

	topmost = self.find_topmost(self.name)

	sidebar_html = frappe.cache().hget("wiki_sidebar", topmost)
	if not sidebar_html or frappe.conf.disable_website_cache or frappe.conf.developer_mode:
		sidebar_items = frappe.get_doc("Wiki Sidebar", topmost).get_children()
		new_sidebar = []

		if not lang:
			cached_wiki = frappe.cache().get_value('clicked_wiki')
			if not cached_wiki:
				lang = "English" if  frappe.boot.frappe.lang == 'en' else "عربي"
			else:
				lang = frappe.db.get_value("Wiki Page",cached_wiki,'wiki_language')
		for each in sidebar_items:
			if each.get('type') == "Wiki Page":
				wiki_id = frappe.get_doc("Wiki Sidebar Item",each.name).item
				if frappe.db.get_value("Wiki Page",wiki_id,'wiki_language') == lang:
					new_sidebar.append(each)
				else:
					pass
			elif each.get('type') == 'Wiki Sidebar':
				if frappe.db.get_value("Wiki Sidebar",each.get('group_name'),'wiki_language') == lang:
					new_sidebar.append(each)
		context = frappe._dict({})
		context.sidebar_items = new_sidebar
		context.docs_search_scope = topmost
		
		sidebar_html = frappe.render_template(
			"one_wiki/templates/wiki_page/templates/web_sidebar.html", context
		)
		frappe.cache().hset("wiki_sidebar", topmost, sidebar_html)

	return sidebar_html, topmost




def update_old_page_(self):
	self.wiki_page_doc.update_page(self.new_title, self.new_code, self.message, self.raised_by)
	updated_page = frappe.get_all(
		"Wiki Sidebar Item", {"item": self.wiki_page, "type": "Wiki Page"}, pluck="name"
	)
	for page in updated_page:
		frappe.db.set_value("Wiki Sidebar Item", page, "title", self.new_title)
	frappe.set_value("Wiki Page",self.wiki_page,'wiki_language',self.wiki_language)
	return




@frappe.whitelist()
def update_create_patch(
	name,
	content,
	title,
	type,
	attachments="{}",
	message="",
	wiki_page_patch=None,
	new=False,
	new_sidebar="",
	new_sidebar_items="",
	sidebar_edited=False,
	language = None,
	draft=False,
):

	context = {"route": name}
	context = frappe._dict(context)
	if type == "Rich Text":
		content = extract_images_from_html(content)

	if new:
		new = True

	status = "Draft" if draft else "Under Review"
	if wiki_page_patch:
		patch = frappe.get_doc("Wiki Page Patch", wiki_page_patch)
		patch.new_title = title
		patch.wiki_language = language
		patch.new_code = content
		patch.status = status
		patch.message = message
		patch.new = new
		patch.new_sidebar = new_sidebar
		patch.new_sidebar_items = new_sidebar_items
		patch.sidebar_edited = sidebar_edited
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
			"wiki_language":language,
			"new_title": title,
			"sidebar_edited": sidebar_edited,
			"new_sidebar_items": new_sidebar_items,
		}

		patch.update(patch_dict)

		patch.save()

		update_file_links(attachments, patch.name)

	out = frappe._dict()

	if frappe.has_permission(doctype="Wiki Page Patch", ptype="submit", throw=False) and not draft:
		patch.approved_by = frappe.session.user
		patch.status = "Approved"
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
		out.route = patch.wiki_page_doc.route

	return out




def update_page_(doc, title, content, edit_message, raised_by=None):
	"""
	Update Wiki Page and create a Wiki Page Revision
	"""
	doc.title = title
	
	if content != doc.content:
		doc.content = content
		revision = frappe.new_doc("Wiki Page Revision")
		revision.append("wiki_pages", {"wiki_page": doc.name})
		revision.content = content
		revision.message = edit_message
		revision.raised_by = raised_by
		revision.insert()

	doc.save()






def wiki_patch_submit(doc,ev):
	"""Close the existing todo when the document is about to be approved.

	Args:
		doc Wiki Page Patch
		ev event
	"""
	todos = frappe.get_all("ToDo",{"reference_type":doc.doctype,'reference_name':doc.name})
	if todos:
		for each in todos:
			frappe.db.set_value("ToDo",each.name,'status','Closed')
		frappe.db.commit()
	

def wiki_patch_insert(doc,ev):
	"""Create  an approval Todo for the current user's line manager when a wiki page patch is created

	Args:
		doc Wiki Page Patch
		ev event
	"""
	
	reports_to = frappe.get_all("Employee",{'user_id':frappe.session.user},['employee_name','reports_to'])
	#Set Approver as the user
	if not reports_to:
		reports_to = frappe.session.user
	if reports_to:
		if reports_to[0].get('employee_name') and reports_to[0].get('reports_to'):
			reports_user = frappe.get_value("Employee",reports_to[0].reports_to,'user_id')
			drafts_url = frappe.utils.get_url()+"/drafts"
			if reports_user:
				args = {
						'assign_to':[reports_user],
						'doctype':doc.doctype,
						'name':doc.name,
						'description':f"Please note that {reports_to[0].employee_name} just modified the Wiki page titled <b>\
          								{doc.new_title}</b><br>.You can approve this on the drafts page <a href='{drafts_url}'>\
                      						here</a> <br/> \
							Kindly review the changes made.",
					}
				add(args)
				doc.approved_by = reports_user
				doc.save()
				frappe.db.commit()
    
			


def get_start_folders():
	return frappe.local.flags.web_pages_folders or ("www", "templates/pages")


def set_template_path(selfs):
	"""
	Searches for file matching the path in the /www
	and /templates/pages folders and sets path if match is found
	"""
	folders = get_start_folders()
	for app in frappe.get_installed_apps(frappe_last=True,sort=True):
		app_path = frappe.get_app_path(app)

		for dirname in folders:
			search_path = os.path.join(app_path, dirname, selfs.path)
			for file_path in selfs.get_index_path_options(search_path):
				if os.path.isfile(file_path) and not is_binary_file(file_path):
					selfs.app = app
					selfs.app_path = app_path
					selfs.file_dir = dirname
					selfs.basename = os.path.splitext(file_path)[0]
					selfs.template_path = os.path.relpath(file_path, selfs.app_path)
					selfs.basepath = os.path.dirname(file_path)
					selfs.filename = os.path.basename(file_path)
					selfs.name = os.path.splitext(selfs.filename)[0]
					return


@frappe.whitelist()
def get_context(doc, context):
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

def wiki_patch_validate(doc, method):
	status_filter = ("Rejected", "Approved")
	check = frappe.db.get_list("Wiki Page Patch", filters={"wiki_page": doc.wiki_page, "status": ["not in", status_filter]}, fields=["name", "raised_by"])
	if check:
		the_raiser = frappe.db.get_value("Employee", {"user_id": check[0]["raised_by"]}, ["reports_to", "employee_name" ], as_dict=1)
		if the_raiser:
			approver_name = frappe.db.get_value("Employee", the_raiser.reports_to, "employee_name")
		else:
			approver_name = the_raiser.employee_name
		if not doc.name in [obj["name"] for obj in check]:
			error = "There is a pending Page Patch for this Wiki Page, kindly wait till the patch is reviewed "
			if approver_name:
				error += f"by {approver_name}"
			frappe.throw(error + ' !')
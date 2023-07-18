import frappe
from frappe import _
import re
from frappe.utils.jinja_globals import is_rtl
from frappe.website.doctype.website_settings.website_settings import modify_header_footer_items

def get_sidebar_items_(self):
    wiki_sidebar = frappe.get_doc("Wiki Space", {"route": self.get_space_route()}).wiki_sidebars
    sidebar = {}

    for sidebar_item in wiki_sidebar:
        wiki_page = frappe.get_doc("Wiki Page", sidebar_item.wiki_page)
        wiki_language = frappe.cache().get_value(f'wiki_language_{frappe.session.user}')
        if wiki_language in ['en','ar']:
            wiki_language_dict = {'en':'English','ar':'عربي'}
            if wiki_page.language == wiki_language_dict[wiki_language]:
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
def fetch_cached_language():
    return frappe.cache().get_value(f'wiki_language_{frappe.session.user}')


@frappe.whitelist()
def fetch_language(wiki):
    try:
        if wiki:
            lang = frappe.get_value("Wiki Page",wiki,'language')
            lang = 'English' if lang in ['',None,'English'] else "Arabic"
            return lang
    except:
        frappe.log_error(title="Fetching Wiki Page",message=frappe.get_traceback())


def fetch_approver(page_patch):
    if "Wiki Manager" in frappe.get_roles(frappe.session.user):
        return 1
    approver = frappe.session.user
    if frappe.db.exists('Wiki Page Patch',page_patch):
        approver = frappe.get_doc('Wiki Page Patch',page_patch).approved_by
        if not approver:
            # get line manager of employee
            employee = frappe.get_all("Employee",{'user_id':frappe.get_doc('Wiki Page Patch',page_patch).raised_by},['name'])
            if employee:
                line_manager = frappe.get_value("Employee",employee[0]['name'],'reports_to')
                if not line_manager:
                    approver = frappe.session.user
                else:
                    approver = frappe.get_value("Employee",line_manager,'user_id')
            return 1 if approver == frappe.session.user else 0
        else:
            return 1 if approver == frappe.session.user else 0
    else:
        frappe.throw("Wiki Page Patch Document not Found")


@frappe.whitelist()
def fetch_details(page_patch=None):
    try:
        can_edit = is_permitted(frappe.session.user)
        if not page_patch:
            return [can_edit,0]
        else:
            approver=fetch_approver(page_patch)
            return [can_edit,approver]
            
            
            
    except:
        frappe.log_error(frappe.get_traceback(),"Error fetching permissions for wiki",)
        
    



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



            
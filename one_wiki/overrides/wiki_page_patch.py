import frappe,random, re, os
from frappe.website.utils  import is_binary_file
from frappe.desk.form.assign_to import add
from frappe.website.utils import cleanup_page_name
from wiki.wiki.doctype.wiki_page_patch.wiki_page_patch import *

class WikiPagePatchOverride(WikiPagePatch):
    def create_new_wiki_page(self):
        self.new_wiki_page = frappe.new_doc("Wiki Page")
        #Check for existing routes and update the route value with _ with one
        route ="/".join(self.wiki_page_doc.route.split("/")[:-1] + [cleanup_page_name(self.new_title)])
        existing_routes = frappe.get_all("Wiki Page",{'route':route})
        if existing_routes:
            str_index = random.choice(range(len(route)-1))
            route = route.replace(route[str_index],"_")
        
        wiki_page_dict = {
            "title": self.new_title,
            "content": self.new_code,
            "route": route,
            "published": 1,
            "language":'عربي' if frappe.cache().get_value(f'wiki_language_{frappe.session.user}') =='ar' else 'English',
            "allow_guest": self.wiki_page_doc.allow_guest,
        }

        self.new_wiki_page.update(wiki_page_dict)
        self.new_wiki_page.save()


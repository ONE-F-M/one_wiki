import re
from frappe import _
from frappe.utils.jinja_globals import is_rtl
from frappe.website.doctype.website_settings.website_settings import modify_header_footer_items
from frappe.utils.data import sbool
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


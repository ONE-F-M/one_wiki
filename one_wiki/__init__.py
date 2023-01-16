
__version__ = '0.0.1'
from one_wiki.overrides.wiki_page import get_context,update_context_
from one_wiki.overrides.overrides import set_template_path
from wiki.wiki.doctype.wiki_page.wiki_page import WikiPage
from frappe.website.page_renderers.document_page import DocumentPage 
from frappe.website.page_renderers.template_page import TemplatePage

WikiPage.get_context = get_context
DocumentPage.update_context = update_context_
TemplatePage.set_template_path=set_template_path



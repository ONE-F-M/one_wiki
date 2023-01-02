
__version__ = '0.0.1'
from one_wiki.overrides.wiki_page import get_context,update_context_
from wiki.wiki.doctype.wiki_page.wiki_page import WikiPage
from frappe.website.page_renderers.document_page import DocumentPage


DocumentPage.update_context = update_context_

WikiPage.get_context = get_context
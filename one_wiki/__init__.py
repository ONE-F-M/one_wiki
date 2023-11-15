

from one_wiki.overrides.wiki_page import update_context_

from frappe.website.page_renderers.document_page import DocumentPage

from wiki.www import drafts

from one_wiki.www.drafts import get_context as get_draft_context

__version__ = '0.0.1'


drafts.get_context = get_draft_context

DocumentPage.update_context = update_context_





__version__ = '0.0.1'
from one_wiki.overrides.wiki_page import get_context,update_context_,get_sidebar_items_
from one_wiki.overrides.overrides import create_new_wiki_page_

from wiki.wiki.doctype.wiki_page.wiki_page import WikiPage

from wiki.wiki.doctype.wiki_page_patch.wiki_page_patch import WikiPagePatch
from frappe.website.page_renderers.document_page import DocumentPage

from wiki.www import drafts

from one_wiki.www.drafts import get_context as get_draft_context





WikiPagePatch.create_new_wiki_page = create_new_wiki_page_

WikiPage.get_context = get_context
WikiPage.get_sidebar_items = get_sidebar_items_
drafts.get_context = get_draft_context

DocumentPage.update_context = update_context_




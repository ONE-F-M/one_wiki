from . import __version__ as app_version

app_name = "one_wiki"
app_title = "One Wiki"
app_publisher = "One_FM"
app_description = "Custom Application to override Frappe Wiki"
app_email = "support@one-fm.com"
app_license = "MIT"

# Includes in <head>
# ------------------

# page_renderer = "one_wiki.overrides.page_renderer.WikiPageRenderer"

# include js, css files in header of desk.html
# app_include_css = "/assets/one_wiki/css/one_wiki.css"
# app_include_js = "/assets/one_wiki/js/one_wiki.js"

# include js, css files in header of web template
# web_include_css = "/assets/one_wiki/css/one_wiki.css"
# web_include_js = "/assets/one_wiki/js/one_wiki.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "one_wiki/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype": "public/js/doctype.js",
#               "Wiki Page": "public/js/doctype_js/wiki_page.js",
#               }
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "one_wiki.utils.jinja_methods",
#	"filters": "one_wiki.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "one_wiki.install.before_install"
# after_install = "one_wiki.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "one_wiki.uninstall.before_uninstall"
# after_uninstall = "one_wiki.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "one_wiki.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# 

# Document Events
# ---------------
# Hook on document methods and events
# website_route_rules = [
#     {"from_route": "/<path:wiki_page>/edit-wiki", "to_route": "wiki/edit"},
#     {"from_route": "/<path:wiki_page>/new-wiki", "to_route": "wiki/new"},
#     {"from_route": "/drafts", "to_route": "wiki/drafts"},
# ]
doc_events = {
	# "*": {
	# 	"on_update": "method",
	# 	"on_cancel": "method",
	# 	"on_trash": "method"
	# }
 
	"Wiki Page Patch":{
		'after_insert':"one_wiki.overrides.overrides.wiki_patch_insert",
		
		'on_submit':"one_wiki.overrides.overrides.wiki_patch_submit",
	}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"one_wiki.tasks.all"
#	],
#	"daily": [
#		"one_wiki.tasks.daily"
#	],
#	"hourly": [
#		"one_wiki.tasks.hourly"
#	],
#	"weekly": [
#		"one_wiki.tasks.weekly"
#	],
#	"monthly": [
#		"one_wiki.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "one_wiki.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "one_wiki.event.get_events"
# }
override_whitelisted_methods = {
    "wiki.wiki.doctype.wiki_page.wiki_page.update": "one_wiki.overrides.wiki_page.update",
#     "wiki.wiki.doctype.wiki_page.wiki_page.get_sidebar_for_page":"one_wiki.overrides.overrides.get_sidebar_for_page_",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "one_wiki.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------


# auth_hooks = [
#	"one_wiki.auth.validate"
# ]

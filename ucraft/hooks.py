app_name = "ucraft"
app_title = "Ucraft"
app_publisher = "Webisoft"
app_description = "This app is an ERPNext integration manager for UCraft"
app_email = "utkarsh@webisoft.com"
app_license = "mit"
app_logo_url = '/assets/whitelabel/images/whitelabel_logo.svg'
# required_apps = ["frappe/hrms"]


# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/ucraft/css/ucraft.css"
# app_include_js = "/assets/ucraft/js/ucraft.js"

# include js, css files in header of web template
# web_include_css = "/assets/ucraft/css/ucraft.css"
# web_include_js = "/assets/ucraft/js/ucraft.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ucraft/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ucraft/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ucraft.utils.jinja_methods",
# 	"filters": "ucraft.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ucraft.install.before_install"
after_install = "ucraft.install.after_install"
after_uninstall = "ucraft.install.after_uninstall"

# Uninstallation
# ------------

# before_uninstall = "ucraft.uninstall.before_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ucraft.utils.before_app_install"
# after_app_install = "ucraft.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ucraft.utils.before_app_uninstall"
# after_app_uninstall = "ucraft.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ucraft.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events
doc_events = {
    "*": {
        "on_update": "ucraft.kafka.send_to_kafka_async",
        "on_cancel": "ucraft.kafka.send_to_kafka_async",
        "on_trash": "ucraft.kafka.send_to_kafka_async",
        "on_submit": "ucraft.kafka.send_to_kafka_async",
        "before_insert": "ucraft.kafka.send_to_kafka_async",
        "after_insert": "ucraft.kafka.send_to_kafka_async",
        "before_save": "ucraft.kafka.send_to_kafka_async",
        "after_save": "ucraft.kafka.send_to_kafka_async",
        "before_rename": "ucraft.kafka.send_to_kafka_async",
        "after_rename": "ucraft.kafka.send_to_kafka_async",
        "before_cancel": "ucraft.kafka.send_to_kafka_async",
        "after_cancel": "ucraft.kafka.send_to_kafka_async",
        "before_trash": "ucraft.kafka.send_to_kafka_async",
        "after_trash": "ucraft.kafka.send_to_kafka_async",
        "before_restore": "ucraft.kafka.send_to_kafka_async",
        "after_restore": "ucraft.kafka.send_to_kafka_async",
        "before_delete": "ucraft.kafka.send_to_kafka_async",
        "after_delete": "ucraft.kafka.send_to_kafka_async"
    }
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ucraft.tasks.all"
# 	],
# 	"daily": [
# 		"ucraft.tasks.daily"
# 	],
# 	"hourly": [
# 		"ucraft.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ucraft.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ucraft.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ucraft.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ucraft.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ucraft.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ucraft.utils.before_request"]
# after_request = ["ucraft.utils.after_request"]

# Job Events
# ----------
# before_job = ["ucraft.utils.before_job"]
# after_job = ["ucraft.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------
# authenticate_login = "ucraft.sso.auth.authenticate_login"

# auth_hooks = [
# 	"ucraft.auth.validate"
# ]
rest_api = {
    'create_company_for_ucraft_project': 'ucraft.api.create_company_for_ucraft_project',
    'handle_callback': 'ucraft.api.handle_callback',
}

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }
website_redirects = [
    {"source": "/#login", "target": "/ucraft"},
    {"source": "/login", "target": "/ucraft"},
    {"source": "/", "target": "/ucraft"},
]

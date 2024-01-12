from pprint import pprint

import frappe
import frappe.utils
from frappe import _
from frappe.auth import LoginManager
from frappe.rate_limiter import rate_limit
from frappe.utils import cint, get_url
from frappe.utils.data import escape_html
from frappe.utils.html_utils import get_icon_html
from frappe.utils.jinja import guess_is_path
from frappe.utils.oauth import get_oauth2_authorize_url, get_oauth_keys, redirect_post_login
from frappe.utils.password import get_decrypted_password
from frappe.website.utils import get_home_page
from ucraft.constants import MAIN_URL_UCRAFT
from ucraft.sso.auth import UcraftAuth
import urllib.parse

no_cache = True


def construct_sso_auth_url(return_url, target='blank'):
    base_url = f"{MAIN_URL_UCRAFT}/callback"
    params = {
        'target': target,
        'returnUrl': return_url
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    return url


def get_context(context):
    redirect_to = frappe.local.request.args.get("redirect-to")

    if frappe.session.user != "Guest":
        if not redirect_to:
            if frappe.session.data.user_type == "Website User":
                redirect_to = get_home_page()
            else:
                redirect_to = "/app"

        if redirect_to != "login":
            frappe.local.flags.redirect_location = redirect_to
            raise frappe.Redirect

    site_url = frappe.utils.get_url()

    context.no_header = True
    context.for_test = "login.html"
    context["title"] = "Login"
    context["hide_login"] = True  # dont show login link on login page again.
    context["login_name_placeholder"] = "gev@ucraft.ai"  # dont show login link on login page again.
    context["provider_logins"] = []
    context["disable_signup"] = cint(frappe.get_website_settings("disable_signup"))
    context["disable_user_pass_login"] = cint(frappe.get_system_settings("disable_user_pass_login"))
    context["logo"] = frappe.get_website_settings("app_logo") or frappe.get_hooks("app_logo_url")[-1]
    context["sso_url"] = construct_sso_auth_url(f"{site_url}/api/method/ucraft.api.handle_callback")
    context["app_name"] = (
        _("Ucraft ERPNext")
    )

    signup_form_template = frappe.get_hooks("signup_form_template")
    if signup_form_template and len(signup_form_template):
        path = signup_form_template[-1]
        if not guess_is_path(path):
            path = frappe.get_attr(signup_form_template[-1])()
    else:
        path = "frappe/templates/signup.html"

    if path:
        context["signup_form_template"] = frappe.get_template(path).render()

    providers = frappe.get_all(
        "Social Login Key",
        filters={"enable_social_login": 1},
        fields=["name", "client_id", "base_url", "provider_name", "icon"],
        order_by="name",
    )

    for provider in providers:
        client_secret = get_decrypted_password("Social Login Key", provider.name, "client_secret")
        if not client_secret:
            continue

        icon = None
        if provider.icon:
            if provider.provider_name == "Custom":
                icon = get_icon_html(provider.icon, small=True)
            else:
                icon = f"<img src={escape_html(provider.icon)!r} alt={escape_html(provider.provider_name)!r}>"

        if provider.client_id and provider.base_url and get_oauth_keys(provider.name):
            context.provider_logins.append(
                {
                    "name": provider.name,
                    "provider_name": provider.provider_name,
                    "auth_url": get_oauth2_authorize_url(provider.name, redirect_to),
                    "icon": icon,
                }
            )
            context["social_login"] = True

    if cint(frappe.db.get_value("LDAP Settings", "LDAP Settings", "enabled")):
        from frappe.integrations.doctype.ldap_settings.ldap_settings import LDAPSettings

        context["ldap_settings"] = LDAPSettings.get_ldap_client_settings()

    login_label = [_("Email")]

    if frappe.utils.cint(frappe.get_system_settings("allow_login_using_mobile_number")):
        login_label.append(_("Mobile"))

    if frappe.utils.cint(frappe.get_system_settings("allow_login_using_user_name")):
        login_label.append(_("Username"))

    context["login_label"] = f" {_('or')} ".join(login_label)

    context["login_with_email_link"] = False

    return context


@frappe.whitelist(allow_guest=True)
def login_via_token(login_token: str):
    sid = frappe.cache.get_value(f"login_token:{login_token}", expires=True)
    if not sid:
        frappe.respond_as_web_page(_("Invalid Request"), _("Invalid Login Token"), http_status_code=417)
        return

    frappe.local.form_dict.sid = sid
    frappe.local.login_manager = LoginManager()

    redirect_post_login(
        desk_user=frappe.db.get_value("User", frappe.session.user, "user_type") == "System User"
    )


@frappe.whitelist(allow_guest=True)
@rate_limit(limit=5, seconds=60 * 60)
def send_login_link(email: str):
    if not frappe.get_system_settings("login_with_email_link"):
        return

    expiry = frappe.get_system_settings("login_with_email_link_expiry") or 10
    link = _generate_temporary_login_link(email, expiry)

    app_name = (
            frappe.get_website_settings("app_name") or frappe.get_system_settings("app_name") or _("Frappe")
    )

    subject = _("Login To {0}").format(app_name)

    frappe.sendmail(
        subject=subject,
        recipients=email,
        template="login_with_email_link",
        args={"link": link, "minutes": expiry, "app_name": app_name},
        now=True,
    )


def _generate_temporary_login_link(email: str, expiry: int):
    assert isinstance(email, str)

    if not frappe.db.exists("User", email):
        frappe.throw(
            _("User with email address {0} does not exist").format(email), frappe.DoesNotExistError
        )
    key = frappe.generate_hash()
    frappe.cache.set_value(f"one_time_login_key:{key}", email, expires_in_sec=expiry * 60)

    return get_url(f"/api/method/frappe.www.login.login_via_key?key={key}")


@frappe.whitelist(allow_guest=True, methods=["GET"])
@rate_limit(limit=5, seconds=60 * 60)
def login_via_key(key: str):
    cache_key = f"one_time_login_key:{key}"
    email = frappe.cache.get_value(cache_key)

    if email:
        frappe.cache.delete_value(cache_key)

        frappe.local.login_manager.login_as(email)

        redirect_post_login(
            desk_user=frappe.db.get_value("User", frappe.session.user, "user_type") == "System User"
        )
    else:
        frappe.respond_as_web_page(
            _("Not Permitted"),
            _("The link you trying to login is invalid or expired."),
            http_status_code=403,
            indicator_color="red",
        )


@frappe.whitelist(allow_guest=True, methods=["POST"])
@rate_limit(limit=5, seconds=60 * 60)
def login(usr, pwd):
    client = UcraftAuth()
    response, info, status_code, access_token = client.login(usr, pwd)
    if response:
        frappe.local.login_manager = LoginManager()
        first_name = info.get("firstName", "")
        last_name = info.get("lastName", "")
        user = frappe.get_all("User", filters={
            "email": usr,
            "first_name": first_name,
            "last_name": last_name
        })
        if len(user) == 0:
            user = frappe.new_doc("User")
            user.email = usr
            user.first_name = first_name
            user.last_name = last_name
            print("first_name", first_name)
            print("last_name", last_name)
            user.insert(ignore_permissions=True)
        else:
            user = frappe.get_doc("User", user[0].name)
        user.auth_token = access_token
        user.is_ucraft_user = True
        # Assign permissions

        user.save(ignore_permissions=True)
        frappe.local.login_manager.login_as(user.name)
        redirect_post_login(
            desk_user=frappe.db.get_value("User", frappe.session.user, "user_type") == "System User"
        )
    else:
        return False


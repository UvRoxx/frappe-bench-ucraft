from pprint import pprint

import requests

import frappe
from frappe import _
from frappe.utils.oauth import redirect_post_login
from ucraft.constants import MAIN_URL_UCRAFT


@frappe.whitelist(allow_guest=True)
def create_company_for_ucraft_project(project_id, company_name):
    # Check if a company with the given project ID already exists
    existing_company = frappe.db.get_value('Company', {'ucraft_project_id': project_id}, 'name')
    if existing_company:
        return {'message': 'Company already exists for this project ID', 'status': 409}

    # Create a new company
    new_company = frappe.get_doc({
        'doctype': 'Company',
        'company_name': company_name,
        'ucraft_project_id': project_id,
        "default_currency": "USD",
    })
    new_company.insert(ignore_permissions=True)

    return {'message': f'Company {company_name} created successfully', 'status': 200}


@frappe.whitelist(allow_guest=True)
def handle_callback():
    print("handle_callback_called")
    data = frappe.form_dict
    nonce_token = data.get('nonce')
    if not nonce_token:
        frappe.throw('Nonce token not provided', frappe.PermissionError)

    # The URL should include the nonce token as a query parameter correctly.
    print(nonce_token)
    url_for_auth = f"https://sso.stage.ucraft.ai/api/access-token?nonce={nonce_token}"
    print(url_for_auth)
    response = requests.get(
        url_for_auth,
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        }
    )
    if response.status_code != 200:
        # Handle the error appropriately, maybe log it or throw a different exception.
        frappe.log(f"Ucraft Login Error Status Code {response.status_code}\nResponse Text: {response.text}")
    access_token_data = response.json()
    user_info = requests.get(
        "https://sso.stage.ucraft.ai/api/user?",
        headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f"Bearer {access_token_data['accessToken']}"
        }
    )
    pprint(user_info.json())
    data = user_info.json()['data']
    first_name = data.get('firstName', '')
    last_name = data.get('lastName', '')
    email = data.get('email', '')
    user = frappe.get_all("User", filters={
        "email": email,
        "first_name": first_name,
        "last_name": last_name
    })
    if len(user) == 0:
        user = frappe.new_doc("User")
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.insert(ignore_permissions=True)
    else:
        user = frappe.get_doc("User", user[0].name)
    user.auth_token = access_token_data['accessToken']
    user.is_ucraft_user = True
    # Assign the given user all permissions
    user.save(ignore_permissions=True)
    frappe.local.login_manager.login_as(user.name)
    redirect_post_login(
        desk_user=frappe.db.get_value("User", frappe.session.user, "user_type") == "System User"
    )




from pprint import pprint

import frappe
from frappe import _


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
        'ucraft_project_id': project_id,  # Ensure this custom field exists in the Company doctype
        "default_currency": "USD"",
    })
    new_company.insert()

    return {'message': f'Company {company_name} created successfully', 'status': 200}


@frappe.whitelist(allow_guest=True)
def handle_callback():
    print("handle_callback_called")
    data = frappe.form_dict
    pprint(data)
    auth_token = data.get('auth_token')
    if not auth_token:
        frappe.throw('Auth token not provided', frappe.PermissionError)
    user = frappe.get_all(
        "User",
        filters={
            "auth_token": auth_token
        }
    )

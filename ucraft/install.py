import os

import frappe
from frappe.custom.doctype.custom_field.custom_field import CustomField


# Install
def after_install():
    create_ucraft_project_id_field()
    create_ucraft_authtoken_and_is_ucraft_user_field_on_user()
    frappe.db.set_value("Website Settings", "Website Settings", "app_name", "Ucraft ERPNext")
    os.system("pip install confluent_kafka==2.3.0")


def create_ucraft_authtoken_and_is_ucraft_user_field_on_user():
    """
    This method will create a field Auth Token which is text and is_ucraft_user which is a bool on install
    """
    # Define the new custom fields properties
    auth_token_field = {
        'fieldname': 'auth_token',
        'label': 'Auth Token',
        'fieldtype': 'Data',
        'insert_after': 'username',  # Adjust this based on your User doctype layout
    }

    is_ucraft_user_field = {
        'fieldname': 'is_ucraft_user',
        'label': 'Is Ucraft User',
        'fieldtype': 'Check',
        'insert_after': 'auth_token',  # Adjust this based on your User doctype layout
    }

    # Add the custom fields to the User doctype
    frappe.get_doc({
        'doctype': 'Custom Field',
        'dt': 'User',
        **auth_token_field
    }).insert(ignore_permissions=True)

    frappe.get_doc({
        'doctype': 'Custom Field',
        'dt': 'User',
        **is_ucraft_user_field
    }).insert(ignore_permissions=True)


def create_ucraft_project_id_field():
    # Define the new custom field properties
    custom_field = {
        'fieldname': 'ucraft_project_id',
        'label': 'Ucraft Project ID',
        'fieldtype': 'Data',
        'insert_after': 'country',  # Adjust this based on your Company doctype layout
        # 'hidden': 1
    }

    # Add the custom field to the Company doctype
    frappe.get_doc({
        'doctype': 'Custom Field',
        'dt': 'Company',
        **custom_field
    }).insert(ignore_permissions=True)


# Uninstall
def after_uninstall():
    frappe.flags.ignore_permissions = True  # Bypass permissions
    delete_ucraft_project_id_field()
    delete_auth_token_field()
    delete_is_ucraft_user_field()
    frappe.db.commit()  # Commit the changes


def delete_ucraft_project_id_field():
    # Fetch the custom field
    custom_field = frappe.get_all('Custom Field', filters={
        'fieldname': 'ucraft_project_id',
        'dt': 'Company'
    })

    # Delete the custom field from the Company doctype
    if custom_field:
        try:
            frappe.delete_doc('Custom Field', custom_field[0].name)
        except frappe.DoesNotExistError:
            pass  # If the custom field does not exist, do nothing


def delete_auth_token_field():
    # Fetch the custom field
    custom_field = frappe.get_all('Custom Field', filters={
        'fieldname': 'auth_token',
        'dt': 'User'
    })

    # Delete the custom field from the User doctype
    if custom_field:
        try:
            frappe.delete_doc('Custom Field', custom_field[0].name)
        except frappe.DoesNotExistError:
            pass  # If the custom field does not exist, do nothing


def delete_is_ucraft_user_field():
    # Fetch the custom field
    custom_field = frappe.get_all('Custom Field', filters={
        'fieldname': 'is_ucraft_user',
        'dt': 'User'
    })

    # Delete the custom field from the User doctype
    if custom_field:
        try:
            frappe.delete_doc('Custom Field', custom_field[0].name)
        except frappe.DoesNotExistError:
            pass  # If the custom field does not exist, do nothing

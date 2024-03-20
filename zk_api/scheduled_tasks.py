import frappe
from . import api
from datetime import datetime
from datetime import timedelta


# @frappe.whitelist(allow_guest=True)
# def test():
#     device_name = frappe.get_value("Zk Settings", None, "name_1")
#     if device_name:
#
#         api.get_log(device_name)
#     else:
#         return "Device not found"


@frappe.whitelist(allow_guest=True)
def get_start_date():
    now = datetime.now()
    start_date = now - timedelta(days=2)
    return start_date.strftime("%Y-%m-%d")


@frappe.whitelist(allow_guest=True)
def get_end_date():
    now = datetime.now()
    start_date = now - timedelta(days=1)
    return start_date.strftime("%Y-%m-%d")


@frappe.whitelist(allow_guest=True)
def scheduled_dev1():
    ip_address = frappe.get_value("Zk Settings", None, "ip_address_1")
    start_date = get_start_date()
    end_date = get_end_date()
    device_name = frappe.get_value("Zk Settings", None, "name_1")
    #
    if ip_address and device_name:
        api.get_logs(ip_address, start_date, end_date, device_name)

    else:
        frappe.throw("You must provide an IP address and a device name")

    return f'{device_name} successfully scheduled'

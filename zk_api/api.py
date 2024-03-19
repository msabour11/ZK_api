import json
from datetime import datetime
from datetime import timedelta
import requests
import json
import os
import frappe
import uuid


def custom_naming_function(doc, method):
    name = f"DEVLOG-{doc.date.strftime('%Y-%m-%d')}-{doc.enroll_no}"
    return name


@frappe.whitelist(allow_guest=True)
def get_log():
    # Get the current directory of the script

    current_dir = os.path.dirname(__file__)

    # Construct the relative path to the file
    relative_path = os.path.join(current_dir, 'res.txt')

    with open(relative_path, 'r') as f:
        json_data = f.read()

    try:
        data = json.loads(json_data)
        for record in data:
            date_time_str = record['dateTime']
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
            date = date_time_obj.date()
            time = date_time_obj.time()
            in_out_mode = record['inOutMode']
            type_map = {0: "IN", 1: "OUT"}
            type1 = type_map.get(in_out_mode, "Unknown")
            existing_records = frappe.db.exists("Device Log", {"enroll_no": record['enrollNumber'], "date": date,
                                                               "time": record['dateTime']})
            if not existing_records:
                doc = frappe.get_doc({
                    "doctype": "Device Log",
                    'enroll_no': record['enrollNumber'],
                    'time': record['dateTime'],
                    'date': date,
                    "type": type1

                })

                # doc.name = str(uuid.uuid4())
                doc.name = custom_naming_function(doc, 'after_insert')
                doc.insert()

        frappe.db.commit()
        return "Success: Device logs inserted successfully"


    except json.JSONDecodeError as e:
        return e

    except Exception as e:
        return f"An error occurred: {e}"

    return data


@frappe.whitelist(allow_guest=True)
def filter_device_logs(start_d, end_d):
    # Get start_date and end_date from ZK Settings
    zk_settings = frappe.get_doc("Zk Settings")
    if start_d is None or end_d is None:
        frappe.msgprint('Error')

    start_date = datetime.strptime(start_d, '%Y-%m-%d').date()
    end_date = datetime.strptime(end_d, '%Y-%m-%d').date()

    # Get Device Log records within the date range
    device_logs = frappe.get_all('Device Log', filters={'date': ['between', [start_date, end_date]]},
                                 fields=['name', 'enroll_no', 'date', 'time', 'type'])

    return device_logs


@frappe.whitelist(allow_guest=True)
def get_url():
    zk_settings = frappe.get_doc('Zk Settings')
    url_list = []

    # Iterate over the IP address and name fields
    for i in range(1, 4):
        ip_address_field = f'ip_address_{i}'
        name_field = f'name_{i}'

        # Skip if the field does not exist or is empty
        if not hasattr(zk_settings, ip_address_field) or not getattr(zk_settings, ip_address_field):
            continue

        # Construct the API endpoint URL
        url = f"http://10.0.0.117/api/GetAttendance?ipAddress={getattr(zk_settings, ip_address_field)}&startDate=2024-03-05&endDate=2024-03-06"

        url_list.append(url)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for record in data:
                date_time_str = record['dateTime']
                date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
                date = date_time_obj.date()
                time = date_time_obj.time()
                in_out_mode = record['inOutMode']
                type_map = {0: "IN", 1: "OUT"}
                type1 = type_map.get(in_out_mode, "Unknown")
                existing_records = frappe.db.exists("Device Log", {"enroll_no": record['enrollNumber'], "date": date,
                                                                   "time": record['dateTime']})
                if not existing_records:
                    doc = frappe.get_doc({
                        "doctype": "Device Log",
                        'enroll_no': record['enrollNumber'],
                        'time': record['dateTime'],
                        'date': date,
                        "type": type1

                    })

                    # doc.name = str(uuid.uuid4())
                    doc.name = custom_naming_function(doc, 'after_insert')
                    doc.insert()

            frappe.db.commit()
            return "Success: Device logs inserted successfully"

        else:
            return f"error"

    # return url_list


@frappe.whitelist(allow_guest=True)
def get_log_dev1():
    ip_address_1 = frappe.db.get_value("Zk Settings", None, 'ip_address_1')
    if ip_address_1:
        url = f"http://10.0.0.117/api/GetAttendance?ipAddress={ip_address_1}&startDate=2024-03-05&endDate=2024-03-06"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            for record in data:
                date_time_str = record['dateTime']
                date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
                date = date_time_obj.date()
                time = date_time_obj.time()
                in_out_mode = record['inOutMode']
                type_map = {0: "IN", 1: "OUT"}
                type1 = type_map.get(in_out_mode, "Unknown")
                existing_records = frappe.db.exists("Device Log", {"enroll_no": record['enrollNumber'], "date": date,
                                                                   "time": record['dateTime']})
                if not existing_records:
                    doc = frappe.get_doc({
                        "doctype": "Device Log",
                        'enroll_no': record['enrollNumber'],
                        'time': record['dateTime'],
                        'date': date,
                        "type": type1
                    })

                    # doc.name = custom_naming_function(doc, 'after_insert')
                    doc.name = str(uuid.uuid4())
                    doc.insert()

            frappe.db.commit()
            return "data inserted successfully"


def is_valid_ip(ip_address):
    try:
        parts = ip_address.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if 0 <= int(part) <= 255:
                return False
        return True
    except ValueError:
        return False


@frappe.whitelist(allow_guest=True)
def get_logs(ip_address,start_date,end_date):
    # if not is_valid_ip(ip_address):
    #     return "Invalid IP Address"
    past_day = datetime.now() - timedelta(days=1)
    # start_date = past_day.strftime('%Y-%m-%d')
    try:
        url = f"http://10.0.0.117/api/GetAttendance?ipAddress={ip_address}&startDate={start_date}&endDate{end_date}"
        response = requests.get(url)

        if response.status_code != 200:
            return "Failed to retrieve data from the device."

        data = response.json()

        for record in data:
            date_time_str = record['dateTime']
            date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S')
            date = date_time_obj.date()
            time = date_time_obj.time()
            in_out_mode = record['inOutMode']
            type_map = {0: "IN", 1: "OUT"}
            type1 = type_map.get(in_out_mode, "Unknown")

            if not frappe.db.exists("Device Log",
                                    {"enroll_no": record['enrollNumber'], "date": date, "time": record['dateTime']}):
                doc = frappe.get_doc({
                    "doctype": "Device Log",
                    'enroll_no': record['enrollNumber'],
                    'time': record['dateTime'],
                    'date': date,
                    "type": type1
                })
                # doc.name = custom_naming_function(doc, 'after_insert')
                doc.name = str(uuid.uuid4())
                doc.insert()

        frappe.db.commit()
        return "Data inserted successfully"
    except requests.exceptions.RequestException as e:
        frappe.msgprint("Request Error: {0}".format(e))

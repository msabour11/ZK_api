import json
from datetime import datetime
import requests
import json

import frappe
import uuid


@frappe.whitelist(allow_guest=True)
def get_log():
    with open('/home/msabour/frappe-bench-dev/apps/zk_api/zk_api/res.txt', 'r') as f:
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
            type1 = type_map.get(in_out_mode,"Unknown")
            existing_records=frappe.db.exists("Device Log",{"enroll_no":record['enrollNumber'],"date":date,"time":record['dateTime']})
            if not existing_records:
                doc = frappe.get_doc({
                    "doctype": "Device Log",
                    'enroll_no': record['enrollNumber'],
                    'time': record['dateTime'],
                    'date': date,
                    "type": type1

                })
                
                doc.name = str(uuid.uuid4())
                doc.insert()

        frappe.db.commit()
        return "Success: Device logs inserted successfully"


    except json.JSONDecodeError as e:
        return e

    except Exception as e:
        return f"An error occurred: {e}"

    return data


@frappe.whitelist(allow_guest=True)
def filter_device_logs(start_d,end_d):
    # Get start_date and end_date from ZK Settings
    zk_settings = frappe.get_doc("Zk Settings")
    # if zk_settings.start_date is None or zk_settings.end_date is None:
    #     frappe.msgprint('error')
    # start_date = datetime.strptime(zk_settings.start_date, '%Y-%m-%d').date()
    # end_date = datetime.strptime(zk_settings.end_date, '%Y-%m-%d').date()
    if start_d is None or end_d is None:
        frappe.msgprint('Error')

    start_date=datetime.strptime(start_d,'%Y-%m-%d').date()
    end_date=datetime.strptime(end_d,'%Y-%m-%d').date()


    # Get Device Log records within the date range
    device_logs = frappe.get_all('Device Log', filters={'date': ['between', [start_date, end_date]]}, fields=['name', 'enroll_no', 'date', 'time', 'type'])

    return device_logs

@frappe.whitelist(allow_guest=True)
def test():
    url="https://dummyjson.com/posts"
    ids=[]
    response=requests.get(url)
    data=response.json()
    for record in data['posts']:
        ids.append(record['title'])
       # return record
        

    return ids
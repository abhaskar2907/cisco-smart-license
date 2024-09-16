from __future__ import print_function
from mailmerge import MailMerge
import sys, json, pprint
from datetime import date

template_1 = "doc_template/cloud-template-cisco-smart-license-details.docx"
infra = 'cloud'

with open(sys.argv[1]) as json_file2:
    json_data2 = json.load(json_file2)

with open(sys.argv[2]) as json_file3:
    json_data3 = json.load(json_file3)

with open(sys.argv[3]) as json_file4:
    json_data4 = json.load(json_file4)

def get_account_list(account_details):
    account_list = []
    for account_values in account_details['accounts']:
        # account_values.update(dict(roles=str(account_values['roles'])))
        account_list.append(account_values)
    return account_list

def get_roles(role_details):
    roles_list = []
    for account_value in role_details['accounts']:
        account_name = account_value['accountDomain']
        for roles in account_value['roles']:
            roles.update(dict(domain_name=str(account_name)))
            roles_list.append(roles)
    return roles_list

def get_device_list(device_details):
    device_list = []
    for va in device_details:
        va['virtual_account'] = va['virtual_account']['name']
        va['total_devices'] = str(va['total_devices'])
        for device in va['device_details']:
            va['instanceName'] = device['instanceName']
            va['productTagName'] = device['productTagName']
            va['device_details'] = str(device['sudi'])
            device_list.append(va)
    return device_list

account_list = get_account_list(json_data2)
roles_list = get_roles(json_data2)
device_list = get_device_list(json_data4)
# pprint.pprint(device_list)


document_1 = MailMerge(template_1)
print("Fields included in {}: {}".format(template_1,
                                         document_1.get_merge_fields()))

# document_1.merge_rows('name', va_devices)
document_1.merge_rows('accountStatus', account_list)
document_1.merge_rows('domain_name', roles_list)
document_1.merge_rows('name', json_data3)
document_1.merge_rows('virtual_account', device_list)
document_1.merge(
    date='{:%d-%b-%Y}'.format(date.today()),)
document_1.write('exports/auto-generated-cisco-smart-license-' + infra + '.docx')
print('Successfully generated on-prem docx file in exports directory ')

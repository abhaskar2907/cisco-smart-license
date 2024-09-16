from __future__ import print_function
from mailmerge import MailMerge
import sys, json, pprint
from datetime import date

template_1 = "doc_template/cloud-template-cisco-smart-license-details.docx"
infra = 'cloud'

with open(sys.argv[1]) as json_file:
    json_data = json.load(json_file)


def get_account_list(account_details):
    account_list = []
    for account_value in account_details:
        account_list.append(account_value)
    return account_list


def get_cloud_licenses(license_details):
    license_list = [{'accountDomain': account_value['accountDomain'], 'virtualAccount': licenses['virtual_account'],
                     'licenseName': license['license'], 'status': license['status']}
                    for account_value in license_details
                    for licenses in account_value['licenses']
                    for license in licenses['licenses']]
    return license_list


def get_cloud_devices(device_details, ):
    device_list = []
    for account_value in device_details:
        for devices in account_value['devices']:
            for device in devices['devices'] if devices['devices'] else []:
                device_dict = {'accountDomain': account_value['accountDomain'],
                               'virtualAccount': devices['virtual_account'],
                               'instanceName': device['instanceName'], 'productTagName': device['productTagName'],
                               'udiSerialNumber': device['sudi']['udiSerialNumber']}
                device_list.append(device_dict)
    return device_list


def get_on_prem(account_details):
    on_prem_list = [{'accountDomain': on_prem_acc['domain'], 'name': on_prem_acc['name'],
                     'cssm_smart_account_name': on_prem_acc['cssm_smart_account_name'],
                     'cssm_va': on_prem_acc['cssm_virtual_account_name']}
                    for account_value in account_details
                    for on_prem_acc in account_value['onPremAccounts']]
    return on_prem_list


def get_on_prem_va(on_prem_va_details):
    on_prem_va_list = []
    for account_value in on_prem_va_details:
        for on_prem_account in account_value['onPremAccounts']:
            for on_prem_va in on_prem_account['virtualAccounts']:
                on_prem_va_dict = {'accountDomain': account_value['accountDomain'],
                                   'cssm_va': on_prem_account['cssm_virtual_account_name'],
                                   'on_prem_va': on_prem_va['name']}
                on_prem_va_list.append(on_prem_va_dict)
    return on_prem_va_list


def get_on_prem_license(on_prem_license_details):
    on_prem_licenses = []
    for account_value in on_prem_license_details:
        for on_prem_account in account_value['onPremAccounts']:
            for on_prem_va in on_prem_account['licenses']:
                for on_prem_lic in on_prem_va['licenses']:
                    on_prem_va_dict = {'accountDomain': account_value['accountDomain'],
                                       'cssm_va': on_prem_account['cssm_virtual_account_name'],
                                       'on_prem_va': on_prem_va['virtual_account'],
                                       'licenseName': on_prem_lic['license'],
                                       'status': on_prem_lic['status']}
                    on_prem_licenses.append(on_prem_va_dict)
    return on_prem_licenses


def get_on_prem_devices(on_prem_device_details):
    on_prem_devices2 = []
    for account_value in on_prem_device_details:
        for on_prem_account in account_value['onPremAccounts']:
            for on_prem_devices in on_prem_account['devices']:
                for on_prem_device_details in on_prem_devices['devices']:
                    on_prem_dev_dict = {'accountDomain': account_value['accountDomain'],
                                        'cssm_va': on_prem_account['cssm_virtual_account_name'],
                                        'on_prem_va': on_prem_devices['virtual_account'],
                                        'instanceName': on_prem_device_details['instanceName'],
                                        'productTagName': on_prem_device_details['productTagName']}
                    on_prem_devices2.append(on_prem_dev_dict)
    return on_prem_devices2


account_list = get_account_list(json_data)
license_list2 = get_cloud_licenses(json_data)
device_list2 = get_cloud_devices(json_data)
on_prem_list = get_on_prem(json_data)
on_prem_va_list = get_on_prem_va(json_data)
on_prem_lic_list = get_on_prem_license(json_data)
on_prem_dev_list = get_on_prem_devices(json_data)
# pprint.pprint(on_prem_dev_list)

document_1 = MailMerge(template_1)
print("Fields included in {}: {}".format(template_1,
                                         document_1.get_merge_fields()))

document_1.merge_rows('accountStatus', account_list)
document_1.merge_rows('accountDomain', license_list2)
document_1.merge_rows('accountDomain', device_list2)
document_1.merge_rows('accountDomain', on_prem_list)
document_1.merge_rows('accountDomain', on_prem_va_list)
document_1.merge_rows('accountDomain', on_prem_lic_list)
document_1.merge_rows('accountDomain', on_prem_dev_list)

document_1.merge(
    date='{:%d-%b-%Y}'.format(date.today()), )
document_1.write('exports/auto-generated-cisco-smart-license-' + infra + '.docx')
print('Successfully generated docx file in exports directory ')

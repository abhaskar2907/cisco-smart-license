from __future__ import print_function
from mailmerge import MailMerge
import sys, json, pprint
from datetime import date

template_1 = "doc_template/on-prem-template-cisco-smart-license-details.docx"
infra = 'on_prem'
on_prem_ip = sys.argv[2]

with open(sys.argv[1]) as json_file2:
    json_data2 = json.load(json_file2)

def get_va_list(va_details):
    va_list = []
    for account_values in json_data2:
        on_prem_accounts = account_values['on_prem_account']['name']
        # json_data3 = json.load(open("exports/on_prem_" + on_prem_ip + on_prem_accounts + "_devices.json", "r"))
        json_data3 = json.load(open(f'exports/{infra}_{on_prem_ip}_{on_prem_accounts}_devices.json', "r"))
        for va_values in json_data3:
            va_filter = va_values['va_name']
            # va_filter.update(dict(device_details=str(va_values['device_details'])))
            va_filter.update(dict(device_details=str(va_values['device_details']), on_prem_account_name=str(on_prem_accounts)))
            va_list.append(va_filter)
    return va_list

def get_account_list(account_details):
    account_list = []
    for account_values in json_data2:
        filter_keys = ['account_id', 'domain', 'name', 'cslu_tenant_url', 'cssm_smart_account_id', 'cssm_smart_account_name']
        filter_dict = {key: str(account_values['on_prem_account'][key]) for key in filter_keys}
        filter_dict['on_prem_name'] = filter_dict['name']
        del filter_dict['name']
        account_list.append(filter_dict)
    return account_list

account_list = get_account_list(json_data2)
va_devices = get_va_list(json_data2)

document_1 = MailMerge(template_1)
print("Fields included in {}: {}".format(template_1,
                                         document_1.get_merge_fields()))

document_1.merge_rows('name', va_devices)
document_1.merge_rows('account_id', account_list)
document_1.merge(
    date='{:%d-%b-%Y}'.format(date.today()),)
document_1.write('exports/auto-generated-cisco-smart-license-' + infra + '.docx')
print('Successfully generated on-prem docx file in exports directory ')

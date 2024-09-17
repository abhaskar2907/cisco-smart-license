# Steps to generate on prem and cloud smart license templates and operations:
1. Clone Repo.
2. Run container:
#### docker build -t smart_license:latest .
#### docker run --rm -it -v ${PWD}:/home smart_license:latest /bin/bash

3. Generate smart account json files:
#### ansible-playbook playbook.yml -t smart_accounts -e infra=cloud
#### ansible-playbook playbook.yml -t smart_accounts -e infra=on_prem

4. Merge smart account json files:
#### ansible-playbook playbook.yml -t merge_json -e infra=on_prem
#### ansible-playbook playbook.yml -t merge_json -e infra=cloud

5. Device transfer across virtual accounts
#### ansible-playbook playbook.yml -t transfer -e infra=on_prem
#### ansible-playbook playbook.yml -t transfer -e infra=cloud

6. Process csv files and generate json:
#### ansible-playbook playbook.yml -t pak -e infra=cloud

7. License transfer of a device from on prem to cloud and vice versa
Add device IP address to ./hosts file in desired group:
For example:

To transfer a device from on_prem to cloud, add the device ip to cloud group:
cloud_device1 ansible_host=10.50.217.53 ansible_ssh_common_args="-o KexAlgorithms=diffie-hellman-group-exchange-sha1"

To transfer a device from cloud to on prem, add the device ip to on_prem group:
on_prem_device1 ansible_host=10.50.217.53 ansible_ssh_common_args="-o KexAlgorithms=diffie-hellman-group-exchange-sha1"

Add device ssh connection details in group_vars/on_prem.yml and group_vars/cloud.yml.
Add call-home profile name and destination addresses.

Playbooks to move device from on prem to cloud:
####  ansible-playbook playbook.yml -t sl_transfer -e infra=cloud --limit="cloud_device1" -e mode=check
####  ansible-playbook playbook.yml -t sl_transfer -e infra=cloud --limit="cloud_device1" -e mode=deregister
####  Manually Synchronise cloud and on prem from GUI
####  ansible-playbook playbook.yml -t sl_transfer -e infra=cloud --limit="cloud_device1" -e mode=register

Playbooks to move device from cloud to on on prem:
####  ansible-playbook playbook.yml -t sl_transfer -e infra=on_prem --limit="on_prem_device1" -e mode=check
####  ansible-playbook playbook.yml -t sl_transfer -e infra=on_prem --limit="on_prem_device1" -e mode=deregister
####  Manually Synchronise cloud and on prem from GUI
####  ansible-playbook playbook.yml -t sl_transfer -e infra=on_prem --limit="on_prem_device1" -e mode=register
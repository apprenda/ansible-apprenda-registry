#!/usr/bin/python

from ansible.module_utils.basic import AnsibleModule
from email.header import Header
import requests

def authenticate(url, user, password, tenant):
    auth_url = "{0}/authentication/api/v1/sessions/developer".format(url)
    auth_data = {
        'username': user,
        'password': password,
        'tenant': tenant
    }
    resp = requests.post(auth_url, verify=False, json=auth_data)
    resp_json = resp.json()
    return resp_json['apprendaSessionToken']

def get_all_registry_settings(auth_token, url):
    apps_url = "{0}/soc/api/v1/registry".format(url)
    resp = requests.get(apps_url, verify=False, headers=auth_token)
    return resp.json(), 0

def create_registry_setting(auth_token, url, registry_name, registry_value, is_encrypted, is_readonly):
    apps_url = "{0}/soc/api/v1/registry".format(url)
    apps_data = {
        'name': registry_name,
        'value': registry_value,
        'isEncrypted': is_encrypted,
        'isReadOnly': is_readonly
    }
    resp = requests.post(apps_url, json=apps_data, verify=False, headers=auth_token)
    if resp.status_code != 201:
        return "Failed with status code: {0} with detail: {1}".format(resp.status_code, resp.text), 1
    return resp.status_code, 0

def delete_registry_setting(auth_token, url, registry_name):
    apps_url = "{0}/soc/api/v1/registry/{1}".format(url, registry_name)
    resp = requests.delete(apps_url, verify=False, headers=auth_token)
    if resp.status_code != 204:
        return resp.status_code, 1
    return resp.status_code, 0

def get_single_registry_settings(auth_token, url, registry_name):
    apps_url = "{0}/soc/api/v1/registry/{1}".format(url, registry_name)
    resp = requests.get(apps_url, verify=False, headers=auth_token)
    return resp.json(), 0

def update_registry_setting(auth_token, url, registry_name, registry_value, is_encrypted, is_readonly):
    apps_url = "{0}/soc/api/v1/registry/{1}".format(url, registry_name)
    apps_data = {
        'name': registry_name,
        'value': registry_value,
        'isEncrypted': is_encrypted,
        'isReadOnly': is_readonly
    }
    resp = requests.put(apps_url, json=apps_data, verify=False, headers=auth_token)
    if resp.status_code != 200:
        return resp.status_code, 1
    return resp.status_code, 0

def main():
    module = AnsibleModule(
        argument_spec=dict(
            action=dict(required=True, choices=['get_all_registry_settings', 'get_single_registry_settings', 'create_registry_setting', 'update_registry_setting', 'delete_registry_setting']),
            apprenda_url=dict(type='str', required=True),
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            tenant=dict(type='str', required=True),
            registry_name=dict(type='str', required=False),
            registry_value=dict(type='str', required=False),
            is_encrypted=dict(type='bool', required=False),
            is_readonly=dict(type='bool', required=False),
        )
    )

    action = module.params['action']
    apprenda_url = module.params['apprenda_url']
    username = module.params['username']
    password = module.params['password']
    tenant = module.params['tenant']
    registry_name = module.params['registry_name']
    registry_value = module.params['registry_value']
    is_encrypted = module.params['is_encrypted']
    is_readonly = module.params['is_readonly']

    auth_token_string = authenticate(apprenda_url, username, password, tenant)
    auth_token = { "ApprendaSessionToken": str(Header(auth_token_string, 'utf-8')) }

    if action == "get_all_registry_settings":
        (out, rc) = get_all_registry_settings(auth_token, apprenda_url)
    if action == "get_single_registry_settings":
        (out, rc) = get_single_registry_settings(auth_token, apprenda_url, registry_name)
    if action == "create_registry_setting":
        (out, rc) = create_registry_setting(auth_token, apprenda_url, registry_name, registry_value, is_encrypted, is_readonly)
    if action == "update_registry_setting":
        (out, rc) = update_registry_setting(auth_token, apprenda_url, registry_name, registry_value, is_encrypted, is_readonly)
    if action == "delete_registry_setting":
        (out, rc) = delete_registry_setting(auth_token, apprenda_url, registry_name)

    if (rc != 0):
        module.fail_json(msg="failure", result=out)
    else:
        module.exit_json(msg="success", result=out)

if __name__ == '__main__':
    main()

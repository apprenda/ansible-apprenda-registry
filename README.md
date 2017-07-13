Apprenda Registry
=========

This role enables management of Apprenda Registry Settings through the System Operations Center.

Requirements
------------

* Apprenda Cloud Platform v7.1 or higher
* Python requests library (`pip install requests`)
* Python apprendaapipythonclient Library (`pip install apprendaapipythonclient`)

Role Variables
--------------

`apprenda_url` - FQDN of your ACP instance (i.e, `https://apps.apprenda.com`) **Required**

`username` - Platform user to execute role actions under. **Required**

`password` - Password of the platform user. **Required**

`tenant` - Tenant Alias of the platform user. **Required**

`action` - The action to perform. This can be one of the following. Required parameters for each action are below the action. **Required**
- `get_all_registry_settings`: Gets all available platform registry settings.
- `get_single_registry_settings`: Gets a single platform registry setting.
  - `registry_name`: The key to retrieve.
- `create_registry_setting` or `update_registry_setting`: Create or update a platform registry setting.
  - `registry_name`: The key to create.
  - `registry_value`: The value to set.
  - `is_encrypted`: If `true`, the value of this setting will be encrypted.
  - `is_readonly`: If `true`, the value is set to readonly status.
- `delete_registry_setting`: Delete a platform registry setting.
  - `registry_name`: The key to delete.

Dependencies
------------


Example Playbook
----------------

This demonstrates how to get, create, update, and delete registry settings.

```
---
- hosts: localhost
  vars:
    apprenda_url: "https://apps.apprenda.bxcr"
    username: "bxcr@apprenda.com"
    password: "password"
    tenant: "developer"
  roles:
  - role: "apprenda_registry"
    action: "get_all_registry_settings"

  - role: "apprenda_registry"
    action: "create_registry_setting"
    registry_name: "MyNewRegistrySetting"
    registry_value: "MyNewRegistryValue"
    is_encrypted: false
    is_readonly: false

  - role: "apprenda_registry"
    action: "get_single_registry_settings"
    registry_name: "MyNewRegistrySetting"

  - role: "apprenda_registry"
    action: "update_registry_setting"
    registry_name: "MyNewRegistrySetting"
    registry_value: "MyNewRegistryValueUpdated"
    is_encrypted: false
    is_readonly: false

  - role: "apprenda_registry"
    action: "get_single_registry_settings"
    registry_name: "MyNewRegistrySetting"
    name: "Verify Updated Registry Setting"

  - role: "apprenda_registry"
    action: "delete_registry_setting"
    registry_name: "MyNewRegistrySetting"
```

License
-------

MIT

Author Information
------------------

Please see http://www.apprenda.com for more information about the Apprenda Cloud Platform.
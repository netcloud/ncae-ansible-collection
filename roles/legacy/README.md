# NCAE Legacy Role

This role can be used for interacting with the Netcloud Automation Engine (NCAE).
It was previously available as a role on Ansible Galaxy, and has now been moved into this collection.

As of today, this is still the correct solution for interacting with NCAE, even though it is called legacy.
In the near future this collection will be expanded with custom modules, so that including tasks is no longer necessary.
To migrate from the previous rule, change all role references from `netcloud.ncae` to `netcloud.ncae.legacy`.

During the release of 1.0.0 of this collection, version 2.0.1 from the previous role has been imported.
Further updates to this role are versioned along with the collection as a whole.

## Role Variables

The following NCAE variables are required for this role.  

- NCAE_USERNAME: YOUR NCAE BACKEND USERNAME
- NCAE_PASSWORD: YOUR NCAE BACKEND PASSWORD
- NCAE_URL: FQDN of the NCAE

## Example: Service deployment
This role provides a way to deploy a full service to the ncae. These tasks
are idempotent based on the `name`.

```yml
- hosts: localhost
  vars:
    NCAE_USERNAME: YOUR NCAE BACKEND USERNAME
    NCAE_PASSWORD: YOUR NCAE BACKEND PASSWORD
    NCAE_URL: FQDN of the NCAE
    AUTH:
      name: tower01 token
      type: Bearer
      auth_username: admin
      auth_value: TOWER TOKEN
    EXT_SERVICE:
      name: tower-01.example.com
      description: ''
      base_url: https://tower-01.example.com/api/v2/
    SERVICE:
      name: NCAE Test
      template:
        values:
          - name: vlan_id
            type: text
            label: VLAN ID
            required: true
      devices: # Optional
        - name: device_name
      fire_and_forget: false # Optional
    PHASES:
      - name: Stage 1
        order: 1
        text: First stage of the deployment
        auto_deploy: true
        idempotency: false
        uri: 10/launch/
        send_credentials: false # Optional
      - name: Stage 2
        order: 2
        text: Second stage of the deployment
        auto_deploy: false
        idempotency: true
        uri: 11/launch/
  tasks:
    - include_role:
        name: netcloud.ncae.legacy
        tasks_from: login # Needs to be called first inorder to get AUTH Cookie
        
    - include_role:
        name: netcloud.ncae.legacy
        tasks_from: auth

    - include_role:
        name: netcloud.ncae.legacy
        tasks_from: ext_api_service

    - include_role:
        name: netcloud.ncae.legacy
        tasks_from: service

    - include_role:
        name: netcloud.ncae.legacy
        tasks_from: phase
      loop: '{{ PHASES }}'
      loop_control:
        loop_var: PHASE
```

Logging Example:

```yml
- hosts: localhost
  vars:
    NCAE_TOKEN: YOUR NCAE BACKEND TOKEN
    NCAE_URL: FQDN of the NCAE
  tasks:
    - include_role:
        name: netcloud.ncae.legacy
        tasks_from: login # Needs to be called first inorder to get AUTH Cookie
        
    - name: 'Log to NCAE'
      vars:
        LOG_TITLE: 'Example Title'
        LOG_HOSTNAME: '{{ hostname }}'
        LOG_TEXT: 'Successfully deployed. Changes to the XYZ done: {{ output.XYZ }}'
        LOG_STATUS: 'IN'
        service_id: '{{ service_id }}'
        service_instance_id: '{{ service_instance_id }}'
      include_role:
        name: netcloud.ncae.legacy
        tasks_from: log
```

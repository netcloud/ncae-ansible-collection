NCAE
====

This is a support role for the Netcloud Automation Engine (NCAE).
The role is also available on [Ansible Galaxy](https://galaxy.ansible.com/netcloud/ncae)


Role Variables
--------------

The following NCAE variables are required for this role.  
NCAE_TOKEN: YOUR TOKEN  
NCAE_URL: FQDN of the NCAE

Example: Service deployment
----------------
This role provides a way to deploy a full service to the ncae. These tasks
are idempotent based on the `name`.

```yml
- hosts: localhost
  vars:
    NCAE_TOKEN: YOUR NCAE BACKEND TOKEN
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
        name: netcloud.ncae
        tasks_from: auth

    - include_role:
        name: netcloud.ncae
        tasks_from: ext_api_service

    - include_role:
        name: netcloud.ncae
        tasks_from: service

    - include_role:
        name: netcloud.ncae
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
    - name: 'Log to NCAE'
      vars:
        LOG_TITLE: 'Example Title'
        LOG_HOSTNAME: '{{ hostname }}'
        LOG_TEXT: 'Successfully deployed. Changes to the XYZ done: {{ output.XYZ }}'
        LOG_STATUS: 'IN'
        service_id: '{{ service_id }}'
        service_instance_id: '{{ service_instance_id }}'
      include_role:
        name: netcloud.ncae
        tasks_from: log
```

License
-------

MIT License

Author Information
------------------

-   **Richard Strnad** - _Initial work_ - [richardstrnad](https://github.com/richardstrnad)

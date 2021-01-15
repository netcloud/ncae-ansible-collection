NCAE
====

This is a support role for the Netcloud Automation Engine (NCAE).


Role Variables
--------------

The following NCAE variables are required for this role.
NCAE_TOKEN: YOUR TOKEN
NCAE_URL: FQDN of the NCAE

Example: Service deployment
----------------
This role provides a way to deploy a full service to the ncae. These tasks
are idempotent based on the `name`.

    - hosts: localhost
      vars:
        NCAE_TOKEN: YOUR TOKEN
        NCAE_URL: FQDN of the NCAE
        EXT_SERVICE:
          name: tower-01.example.com
          description: ''
          base_url: https://tower-01.example.com/api/v2/
          auth:
            type: basic
            username: admin
            password: password
        SERVICE:
          name: NCAE Test
          template:
            values:
              - name: vlan_id
                type: text
                label: VLAN ID
                required: true
        PHASES:
          - name: Stage 1
            order: 1
            text: First stage of the deployment
            auto_deploy: true
            idempotency: false
            uri: job_templates/10/launch/
          - name: Stage 2
            order: 2
            text: Second stage of the deployment
            auto_deploy: false
            idempotency: true
            uri: job_templates/11/launch/
      tasks:
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

License
-------

MIT License

Author Information
------------------

-   **Richard Strnad** - _Initial work_ - [richardstrnad](https://github.com/richardstrnad)

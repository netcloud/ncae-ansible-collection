# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    module: core_automation_ext_api_service
    author: Netcloud AG (@netcloud)
    short_description: Manage automation.ExtApiService objects
    description:
        - This module is a CRUD wrapper for NCAE Core around C(/api/automation/v1/ext-api-service).
        - The C(automation.ExtApiService) endpoint is related to external API services.
        - The API calls are always made from the Ansible controller as part of an action plugin.
    options:
        name:
            description:
                - Name for ExtApiService object, used as unique identifier
            type: str
            required: true
        description:
            description:
                - Optional description for ExtApiService object
            type: str
        base_url:
            description:
                - Base URL for external service to interact with.
                - The correct URL path depends on the external system that is used.
            type: str
            required: true
        auth_id:
            description:
                - ID of C(automation.Auth) object to use for authentication.
                - See also M(netcloud.ncae.core_automation_auth).
            type: int
            required: true
    extends_documentation_fragment:
        - netcloud.ncae.auth
"""

EXAMPLES = r"""
# Create or update NCAE external api service
- core_automation_ext_api_service:
    name: AWX-01
    description: Ansible AWX
    base_url: https://awx.example.com/api/v2/
    auth_id: 1
"""

RETURN = r"""
id:
    description: ID of managed object
    returned: success
    type: int
data:
    description: Raw API data as returned by NCAE Core
    returned: success
    type: dict
"""

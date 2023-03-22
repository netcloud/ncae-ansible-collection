# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    module: core_automation_auth
    author: Netcloud AG (@netcloud)
    short_description: Manage automation.Auth objects
    description:
        - This module is a CRUD wrapper for NCAE Core around C(/api/automation/v1/auth).
        - The C(automation.Auth) endpoint is related to authentication against external API services.
        - The API calls are always made from the Ansible controller as part of an action plugin.
    options:
        name:
            description:
                - Name for Auth object, used as unique identifier.
            type: str
            required: true
        type:
            description:
                - Type of HTTP-based authentication to use.
            type: str
            default: Basic
            choices:
                - Basic
                - Bearer
        auth_username:
            description:
                - Username to store for external service authentication.
            type: str
            required: true
        auth_value:
            description:
                - Value to store for external service authentication.
            type: str
            required: true
    extends_documentation_fragment:
        - netcloud.ncae.auth
"""

EXAMPLES = r"""
# Create or update external service auth
- netcloud.ncae.core_automation_auth:
    name: AUTH-AWX-01
    type: Basic
    auth_username: admin
    auth_value: topsecret
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

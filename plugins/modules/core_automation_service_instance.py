# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    module: core_automation_service_instance
    author: Netcloud AG (@netcloud)
    short_description: Manage automation.ServiceInstance objects
    description:
        - This module is a CRUD wrapper for NCAE Core around C(/api/automation/v1/service-instance).
        - The C(automation.ServiceInstance) endpoint is related to service instances.
        - The API calls are always made from the Ansible controller as part of an action plugin.
    options:
        service_id:
            description:
                - ID of C(automation.Service) to which this phase belongs.
                - See also M(netcloud.ncae.core_automation_service).
            type: int
            required: true
        data:
            description:
                - CMDB data for service instance.
            type: dict
            required: true
    extends_documentation_fragment:
        - netcloud.ncae.auth
"""

EXAMPLES = r"""
# Create new service instance for service #42
- netcloud.ncae.core_automation_service_instance:
    service_id: 42
    data:
      name: New Instance
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

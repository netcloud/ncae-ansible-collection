# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    module: core_automation_phase
    author: Netcloud AG (@netcloud)
    short_description: Manage automation.Phase objects
    description:
        - This module is a CRUD wrapper for NCAE Core around C(/api/automation/v1/phase).
        - The C(automation.Phase) endpoint is related to NCAE service phases.
        - The API calls are always made from the Ansible controller as part of an action plugin.
    options:
        name:
            description:
                - Name for Phase object, used as unique identifier
            type: str
            required: true
        text:
            description:
                - Human-readable description for actions taken by phase
            type: str
            required: true
        order:
            description:
                - An integer specifying the order of this phase.
                - In NCAE, every service has one or more ordered phases.
                - The lower the number, the earlier the phase is being triggered.
                - Each order number should only be used once.
            type: int
            required: true
        service_id:
            description:
                - ID of C(automation.Service) to which this phase belongs.
                - See also M(netcloud.ncae.core_automation_service).
            type: int
            required: true
        ext_api_service_id:
            description:
                - ID of C(automation.ExtApiService) used by this phase.
                - See also M(netcloud.ncae.core_automation_phase).
            type: int
            required: true
        auto_deploy:
            description:
                - Specifies if the phase should be automatically deployed.
                - If C(true), the phase gets automatically deployed after the previous one completes.
                - If C(false), the user has to manually trigger a deployment for this phase.
            type: bool
            default: false
        idempotency:
            description:
                - Specifies if the phase should be seen as idempotent.
            type: bool
            default: false
        uri_reverse_capable:
            description:
                - Specifies if the same URI can be used for teardown as well.
                - If C(true), the URI specified in I(uri) is used for decommissioning.
                - If C(false), the URI specified in I(decom_uri) is used instead.
                - If C(false) and I(decom_uri) is missing, this phase does not support decommissioning.
            type: bool
            default: false
        uri:
            description:
                - Specifies the URI that should be used for deploying this phase.
                - Can optionally be used for decommissioning as well, see I(uri_reverse_capable).
            type: str
            required: true
        decom_uri:
            description:
                - Specifies the URI that should be used for decommissioning this phase.
                - Can not be used together with I(uri_reverse_capable) set to C(true).
            type: str
    extends_documentation_fragment:
        - netcloud.ncae.auth
"""

EXAMPLES = r"""
# Create or update NCAE phase
- netcloud.ncae.core_automation_phase:
    order: 1
    name: First Phase
    text: This is an extraordinary phase
    service_id: 4
    ext_api_service_id: 9
    auto_deploy: true
    idempotency: true
    uri_reverse_capable: true
    uri: job_templates/17/launch/
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

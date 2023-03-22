# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    module: module_phase_update
    author: Netcloud AG (@netcloud)
    short_description: Update status of NCAE phase instance
    description:
        - This module is used to update the status of a phase instance.
        - It is meant to signal the outcome of a phase operation to the user.
        - As an example, after a successful deployment the phase should be switched to "Deployed".
    options:
        url:
            description:
                - URL to use for sending the phase update request.
                - Defaults to C(/api/automation/v1/phase-instance/<id>) with the ID set to I(phase_instance_id).
                - Either I(url) or I(phase_instance_id) must be provided.
            type: str
        status:
            description:
                - New status that should be applied to phase instance.
            type: str
            required: true
            choices:
                - ordered
                - deployed
                - retired
                - error
                - ready
                - pending_update
                - updating
        phase_instance_id:
            description:
                - ID of C(automation.PhaseInstance) which should be updated.
                - Used for constructing the URL if not specified via I(url).
                - Either I(url) or I(phase_instance_id) must be provided.
            type: int
    extends_documentation_fragment:
        - netcloud.ncae.auth
"""

EXAMPLES = r"""
# Update phase instance #42 via URL to Deployed
- netcloud.ncae.module_phase_update:
    url: https://ncae.example.com/api/automation/v1/phase-instance/42
    status: deployed

# Update phase instance #42 via ID to Retired
- netcloud.ncae.module_phase_update:
    phase_instance_id: 42
    status: retired
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

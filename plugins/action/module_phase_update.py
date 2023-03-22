# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.netcloud.ncae.plugins.plugin_utils.base import NcaeActionBase
from ansible_collections.netcloud.ncae.plugins.plugin_utils.misc import NCAE_BASE_ARGUMENT_SPEC

PHASE_STATUS_MAPPING = {
    "ordered": "OR",
    "deployed": "DE",
    "retired": "RE",
    "error": "ER",
    "ready": "RA",
    "pending_update": "PU",
    "updating": "UP",
}


class ActionModule(NcaeActionBase):
    def execute(self):
        # Build URL with phase instance ID, unless specified
        url = self._task_args["url"]
        if not url:
            url = "/api/automation/v1/phase-instance/" + self._task_args["phase_instance_id"]

        # Determine internal status from user-friendly status
        status = PHASE_STATUS_MAPPING[self._task_args["status"]]

        return self.ncae_client.session.patch(
            url=url,
            data={
                "status": status,
            },
        )

    def _get_validate_spec(self):
        return {
            "argument_spec": {
                "url": {
                    "type": "str",
                },
                "status": {
                    "type": "str",
                    "required": True,
                    "choices": PHASE_STATUS_MAPPING.keys(),
                },
                "phase_instance_id": {
                    "type": "int",
                },
                **NCAE_BASE_ARGUMENT_SPEC,
            },
            "mutually_exclusive": [
                ("url", "phase_instance_id"),
            ],
            "required_one_of": [
                ("url", "phase_instance_id"),
            ],
        }

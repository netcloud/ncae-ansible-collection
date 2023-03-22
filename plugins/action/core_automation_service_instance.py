# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.netcloud.ncae.plugins.plugin_utils.base import NcaeRestActionBase
from ansible_collections.netcloud.ncae.plugins.plugin_utils.misc import NCAE_REST_ARGUMENT_SPEC


class ActionModule(NcaeRestActionBase):
    def get_endpoint(self):
        return "/api/automation/v1/service-instance"

    def _get_validate_spec(self):
        return {
            "argument_spec": {
                **NCAE_REST_ARGUMENT_SPEC,
                "service_id": {
                    "type": "int",
                    "required": True,
                },
                "data": {
                    "type": "dict",
                    "default": {},
                },
            }
        }

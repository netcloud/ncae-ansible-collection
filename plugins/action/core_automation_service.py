# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.netcloud.ncae.plugins.plugin_utils.base import NcaeRestActionBase
from ansible_collections.netcloud.ncae.plugins.plugin_utils.misc import NCAE_REST_ARGUMENT_SPEC


class ActionModule(NcaeRestActionBase):
    def get_endpoint(self):
        return "/api/automation/v1/service"

    def get_ignored_keys(self):
        return ("module_name",)

    def get_unique_keys(self):
        return ("name",)

    def _get_validate_spec(self):
        return {
            "argument_spec": {
                "name": {
                    "type": "str",
                },
                "description": {
                    "type": "str",
                },
                "fire_and_forget": {
                    "type": "bool",
                    "default": False,
                },
                "excel": {
                    "type": "bool",
                    "default": False,
                },
                "devices": {
                    "type": "list",
                    "elements": "int",
                    "default": [],
                },
                "template": {
                    "type": "dict",
                },
                "module_name": {
                    "type": "str",
                },
                **NCAE_REST_ARGUMENT_SPEC,
            },
            "required_if": [
                ("state", "present", ("name", "description", "template", "module_name")),
                ("state", "absent", ("id", "name"), True),
            ],
        }

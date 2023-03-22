# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.netcloud.ncae.plugins.plugin_utils.base import NcaeRestActionBase
from ansible_collections.netcloud.ncae.plugins.plugin_utils.misc import NCAE_REST_ARGUMENT_SPEC


class ActionModule(NcaeRestActionBase):
    def get_endpoint(self):
        return "/api/automation/v1/phase"

    def get_mappings(self):
        return {
            "uri_reverse_capable": "uriIsReverseCapable",
            "decom_uri": "decomUri",
        }

    def get_unique_keys(self):
        return ("service_id", "order")

    def build_object_attributes(self, values):
        attrs = super().build_object_attributes(values)
        attrs["service"] = attrs.pop("service_id")
        return attrs

    def _get_validate_spec(self):
        return {
            "argument_spec": {
                **NCAE_REST_ARGUMENT_SPEC,
                "id": {
                    "type": "str",
                },
                "order": {
                    "type": "int",
                },
                "name": {
                    "type": "str",
                },
                "text": {
                    "type": "str",
                },
                "service_id": {
                    "type": "int",
                },
                "ext_api_service_id": {
                    "type": "int",
                },
                "auto_deploy": {
                    "type": "bool",
                    "default": False,
                },
                "idempotency": {
                    "type": "bool",
                    "default": False,
                },
                "uri": {
                    "type": "str",
                },
                "uri_reverse_capable": {
                    "type": "bool",
                    "default": False,
                },
                "decom_uri": {
                    "type": "str",
                },
            },
            "required_if": [
                ("state", "present", ("order", "name", "text", "service_id", "ext_api_service_id", "uri")),
                ("state", "absent", ("id", "order", "service_id"), True),
            ],
        }

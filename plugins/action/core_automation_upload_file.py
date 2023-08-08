# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible_collections.netcloud.ncae.plugins.plugin_utils.base import NcaeRestActionBase
from ansible_collections.netcloud.ncae.plugins.plugin_utils.misc import NCAE_REST_ARGUMENT_SPEC


class ActionModule(NcaeRestActionBase):
    def get_endpoint(self):
        return "/api/automation/v1/upload-file"

    def get_request_options(self):
        return dict(multipart=True)

    def build_object_values(self):
        # Generate object values with default logic
        values = super().build_object_values()

        # Transform file-related properties into combined dictionary
        # This is needed by `ansible.module_utils.urls.prepare_multipart`
        values["file"] = {
            "filename": values.pop("path", None) or values["name"],
            "content": values.pop("content", None),
            "mime_type": values.pop("mime_type", None),
        }

        return values

    def _get_validate_spec(self):
        return {
            "argument_spec": {
                **NCAE_REST_ARGUMENT_SPEC,
                "name": {
                    "type": "str",
                },
                "content": {
                    "type": "str",
                    "default": None,
                },
                "path": {
                    "type": "str",
                    "default": None,
                },
                "mime_type": {
                    "type": "str",
                    "default": None,
                },
                "service_instance": {
                    "type": "int",
                },
                "delete_on": {
                    "type": "str",
                },
                "allow_anonymous_download": {
                    "type": "bool",
                    "default": False,
                },
            },
            "mutually_exclusive": [
                ("content", "path"),
            ],
            "required_if": [
                ("state", "present", ("name",)),
                ("state", "absent", ("id",)),
            ],
        }

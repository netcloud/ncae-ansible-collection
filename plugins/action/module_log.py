# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from datetime import datetime

from ansible_collections.netcloud.ncae.plugins.plugin_utils.base import NcaeActionBase
from ansible_collections.netcloud.ncae.plugins.plugin_utils.misc import NCAE_BASE_ARGUMENT_SPEC

LOG_STATUS_MAPPING = {
    "info": "IN",
    "warning": "WA",
    "error": "ER",
}


class ActionModule(NcaeActionBase):
    def execute(self):
        # Determine internal status from mapping user-friendly level
        status = LOG_STATUS_MAPPING[self._task_args["level"]]

        # Automatically set timestamp to now if not specified
        timestamp = self._task_args["timestamp"]
        if not timestamp:
            timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

        # Send log message via POST call
        self.ncae_client.session.post(
            url=self._task_args["url"],
            data={
                "status": status,
                "timestamp": timestamp,
                "log_hostname": self._task_args["hostname"],
                "log_title": self._task_args["title"],
                "log_text": self._task_args["text"],
                "publish": self._task_args["publish"],
                "service_id": self._task_args["service_id"],
                "service_instance_id": self._task_args["service_instance_id"],
            },
        )

        return {"changed": False}

    def _get_validate_spec(self):
        return {
            "argument_spec": {
                "url": {
                    "type": "str",
                    "default": "/api/logger/v1/service-instance-log",
                },
                "level": {
                    "type": "str",
                    "default": "info",
                    "choices": LOG_STATUS_MAPPING.keys(),
                },
                "timestamp": {
                    "type": "str",
                },
                "hostname": {
                    "type": "str",
                    "required": True,
                },
                "title": {
                    "type": "str",
                    "required": True,
                },
                "text": {
                    "type": "str",
                    "required": True,
                },
                "publish": {
                    "type": "bool",
                    "default": True,
                },
                "service_id": {
                    "type": "int",
                    "required": True,
                },
                "service_instance_id": {
                    "type": "int",
                    "required": True,
                },
                **NCAE_BASE_ARGUMENT_SPEC,
            }
        }

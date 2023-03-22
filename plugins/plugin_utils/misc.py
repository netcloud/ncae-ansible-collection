# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.module_utils.basic import env_fallback

NCAE_BASE_ARGUMENT_SPEC = {
    "ncae_base_url": {
        "type": "str",
        "required": True,
        "fallback": (env_fallback, ["NCAE_URL"]),
    },
    "ncae_username": {
        "type": "str",
        "required": True,
        "fallback": (env_fallback, ["NCAE_USERNAME"]),
    },
    "ncae_password": {
        "type": "str",
        "required": True,
        "no_log": True,
        "fallback": (env_fallback, ["NCAE_PASSWORD"]),
    },
    "validate_certs": {
        "type": "bool",
        "default": False,
        "fallback": (env_fallback, ["NCAE_VALIDATE_CERTS"]),
    },
}

NCAE_REST_ARGUMENT_SPEC = {
    **NCAE_BASE_ARGUMENT_SPEC,
    "state": {
        "type": "str",
        "default": "present",
        "choices": ("present", "absent"),
    },
    "id": {
        "type": "int",
    },
}

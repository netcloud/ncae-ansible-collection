# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type


class ModuleDocFragment(object):
    DOCUMENTATION = r"""
        options:
            ncae_base_url:
                description:
                    - Base URL of NCAE instance to query without trailing slash.
                    - If value not set, will try environment variables C(NCAE_BASE_URL) and C(NCAE_URL).
                type: str
                required: true
            ncae_username:
                description:
                    - Username for authenticating against NCAE.
                    - If value not set, will try environment variables C(NCAE_USERNAME).
                type: str
                required: true
            ncae_password:
                description:
                    - Password for authenticating against NCAE.
                    - If value not set, will try environment variables C(NCAE_PASSWORD).
                type: str
                required: true
            validate_certs:
                description:
                    - Whether to verify SSL certificates for API connections.
                    - If value not set, will try environment variables C(NCAE_VALIDATE_CERTS).
                type: bool
                default: false
    """

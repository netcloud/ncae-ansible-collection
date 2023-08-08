# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    module: core_automation_upload_file
    author: Netcloud AG (@netcloud)
    short_description: Manage automation.UploadFile objects
    description:
        - This module is a CRUD wrapper for NCAE Core around C(/api/automation/v1/upload-file).
        - The C(automation.UploadFile) endpoint is related to NCAE services.
        - The API calls are always made from the Ansible controller as part of an action plugin.
    options:
        name:
            description:
                - Name to be used for storing the file inside NCAE.
            type: str
            required: true
        content:
            description:
                - Optional content which should be used instead of reading from the filesystem.
                - In case of binary data, avoid this option and use I(path) instead.
                - Options I(content) and I(path) are mutually exclusive.
            type: str
        path:
            description:
                - Optional path to the file which should be uploaded.
                - If not specified, defaults to the same value as I(name).
                - Options I(content) and I(path) are mutually exclusive.
            type: str
        mime_type:
            description:
                - Optional MIME type for the file which is being uploaded.
                - If left empty, the file contents will be analysed for a heuristic detection.
                - If no MIME type can be determined, C(application/octet-stream) is used instead.
            type: str
        service_instance:
            description:
                - Optional ID of service instance to which this file belongs.
                - If left empty, the file is assumed to be at global scope.
            type: int
        delete_on:
            description:
                - Optional expiration date in C(YYYY-MM-DD) format for file.
                - If not specified, the default file expiration as defined by NCAE Core is used.
            type: str
        allow_anonymous_download:
            description:
                - Specifies whether the file can be downloaded anonymously.
                - If C(true), the file requires no authentication for downloads.
                - If C(false), the file can only be downloaded when authenticated.
            type: bool
            default: false
    extends_documentation_fragment:
        - netcloud.ncae.auth
"""

EXAMPLES = r"""
# Upload new file called netcloud.jpg based on local/company-logo.jpg
- netcloud.ncae.core_automation_upload_file:
    name: netcloud.jpg
    path: local/company-logo.jpg
    mime_type: image/jpeg
    delete_on: 2038-01-19
    service_instance: 139

# Upload new file based on string
- netcloud.ncae.core_automation_upload_file:
    name: important.txt
    content: Hello World
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

# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    module: module_log
    author: Netcloud AG (@netcloud)
    short_description: Log service-instance related message to NCAE
    description:
        - This module is used to log a message relating to a service instance viae NCAE Core.
        - All log messages are streamed in real-time to the user.
        - Different log levels can be used to signal the severity.
    options:
        url:
            description:
                - URL to call for logging a message via NCAE Core.
                - When used within a NCAE module, the variable C(callback_data.logger_url) should be used.
                - Otherwise the default endpoint is being used.
            type: str
            default: /api/logger/v1/service-instance-log
        level:
            description:
                - Specifies the desired log level / severity of the message.
            type: str
            default: info
            choices:
                - info
                - warning
                - error
        timestamp:
            description:
                - Specifies the timestamp for the message being logged.
                - Timestamp must be in ISO8061 format, e.g. C(2023-12-31T23:59:59Z).
                - The current time is being used when not specified.
            type: str
        hostname:
            description:
                - Specifies the hostname from where the message originates.
            type: str
            required: true
        title:
            description:
                - Title of the log message, should quickly summarize the contents.
                - A maximum of 100 characters is being enforced for this field.
                - Attempting to submit a longer title leads to the API call failing.
            type: str
            required: true
        text:
            description:
                - Body of the log message, should explain the reason in more detail.
                - A maximum of 500 characters is being enforced for this field.
                - Attempting to submit a longer title leads to the API call failing.
            type: str
            required: true
        publish:
            description:
                - Specifies if the log message should be published.
            type: bool
            default: true
        service_id:
            description:
                - ID of C(automation.Service) to which this phase belongs.
                - See also M(netcloud.ncae.core_automation_service).
            type: int
            required: true
        service_instance_id:
            description:
                - ID of C(automation.ServiceInstance) to which this phase belongs.
            type: int
            required: true
    extends_documentation_fragment:
        - netcloud.ncae.auth
"""

EXAMPLES = r"""
# Send warning log message for service #8 with instance #42
- netcloud.ncae.module_log:
    status: warning
    log_hostname: example-host
    log_title: Something happened
    log_text: And it should not have happened
    service_id: 8
    service_instance_id: 42
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

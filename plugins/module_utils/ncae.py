# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.module_utils.urls import Request
from ansible.module_utils.six.moves.urllib.parse import urljoin


class NcaeClient:
    def __init__(self, base_url, username, password, validate_certs=True):
        self._session = NcaeSession(
            base_url=base_url,
            validate_certs=validate_certs,
        )
        self.authenticate(username, password)

    def authenticate(self, username, password):
        self._session.post(
            url="/api/auth/v1/login/",
            data={
                "username": username,
                "password": password,
            },
        )

    def list_simple_devices(self):
        response = self._session.get("/api/dashboard/v1/simple-device")
        return response["results"]

    def list_device_groups(self):
        response = self._session.get("/api/dashboard/v1/device-group")
        return response["results"]


class NcaeSession:
    def __init__(self, *, base_url, timeout=60, validate_certs=True):
        self._base_url = base_url.strip("/")
        self._http_client = Request(
            http_agent="NCAE Ansible Client",
            timeout=timeout,
            validate_certs=validate_certs,
        )

    def get(self, url):
        return self._request(
            method="GET",
            url=url,
        )

    def post(self, url, data):
        return self._request(
            method="POST",
            url=url,
            data=json.dumps(data),
            headers={"Content-Type": "application/json"},
        )

    def _request(self, method, url, *args, **kwargs):
        response = self._http_client.open(
            method=method,
            url=urljoin(self._base_url, url),
            *args,
            **kwargs,
        )

        return json.loads(response.read())

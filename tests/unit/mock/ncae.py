# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json

from ansible_collections.netcloud.ncae.plugins.plugin_utils.ncae import NcaeClient, NcaeSession


class MockNcaeClient:
    def __init__(self, mocker, default_mocks=True):
        # Prepare state for handling mocked calls
        self._mocker = mocker
        self._client = None
        self._handlers = {}

        # Initialize with default mocks unless disabled
        if default_mocks:
            self._load_default_mocks()

    def mock_fixture(self, method, url, name):
        with open(f"tests/unit/fixtures/{name}.json", "rb") as fp:
            fixture = json.load(fp)
            handler_key = self._get_handler_key(method, url)
            self._handlers[handler_key] = lambda **_: fixture

    def __getattr__(self, attr):
        # Build mocked client on-demand instead of during class construction.
        # At least one mock for the login endpoint is required.
        if self._client is None:
            self._client = self._build_mock_client()

        # Passthrough to mocked client so all methods are supported.
        return getattr(self._client, attr)

    def _load_default_mocks(self):
        # List of URLs to map to static JSON fixtures for testing
        fixtures = [
            ["POST", "auth", "v1", "login"],
            ["GET", "dashboard", "v1", "device-group"],
            ["GET", "dashboard", "v1", "simple-device"],
        ]

        # Create new fixture-based request mock for all urls
        for url_parts in fixtures:
            method = url_parts.pop(0)
            url = "/api/" + "/".join(url_parts)
            fixture = method.lower() + "-" + "-".join(url_parts)
            self.mock_fixture(method, url, fixture)

    def _handle_mock_request(self, method, url, **kwargs):
        handler_key = self._get_handler_key(method, url)
        handler = self._handlers.get(handler_key)
        if handler is None:
            raise Exception("No request mapping for " + method + " " + url)

        return handler(method=method, url=url)

    def _get_handler_key(self, method, url):
        return (method.upper(), url.rstrip("/"))

    def _build_mock_client(self):
        # Mock _request method to catch all external API requests.
        # These will be dispatched to this class instead for per-request mocking.
        with self._mocker.patch.object(
            target=NcaeSession,
            attribute="_request",
            side_effect=self._handle_mock_request,
        ):
            return NcaeClient(
                base_url="http://localhost:8080",
                username="admin",
                password="admin",
            )

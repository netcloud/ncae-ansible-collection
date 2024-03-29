# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from urllib.parse import urlencode

import ansible.module_utils.six.moves.http_cookiejar as cookiejar
from ansible.module_utils.six import iteritems
from ansible.module_utils.six.moves.urllib.error import HTTPError
from ansible.module_utils.six.moves.urllib.parse import urljoin, urlsplit
from ansible.module_utils.urls import Request, prepare_multipart


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

    def create(self, endpoint, values, **kwargs):
        response = self._session.post(endpoint, data=values, **kwargs)

        return {
            "changed": True,
            "change_reason": "created",
            "msg": f"Created new {endpoint} instance #{response['id']}",
            "id": response["id"],
            "data": response,
        }

    def update(self, endpoint, id, values, **kwargs):
        instance_url = f"{endpoint}/{id}"
        response = self._session.patch(instance_url, data=values, **kwargs)

        return {
            "changed": True,
            "change_reason": "updated",
            "msg": f"Updated new {endpoint} instance #{response['id']}",
            "id": response["id"],
            "data": response,
        }

    def delete(self, endpoint, id, **kwargs):
        instance_url = f"{endpoint}/{id}"
        response = self._session.delete(instance_url, **kwargs)

        if response is None:
            return {"changed": False}

        return {
            "changed": True,
            "change_reason": "deleted",
            "msg": f"Deleted {endpoint} instance #{id}",
            "id": id,
        }

    def lookup(self, endpoint, attributes, request_opts=None):
        # Retrieve existing items with specified attributes
        request_opts = request_opts if request_opts is not None else {}
        items = self._session.get(
            endpoint,
            params=attributes,
            request_opts=request_opts,
        )["results"]

        # Ensure there is at most one item to determine uniqueness
        if len(items) > 1:
            raise Exception(f"more than one item for {endpoint} with: {attributes}")
        existing = items[0] if len(items) == 1 else None

        # If no item was found, return early
        if not existing:
            return None

        # Check if existing item actually matches attributes
        # This is require to cover API failures/mismatches with NCAE core
        for k, av in iteritems(attributes):
            iv = existing.get(k, existing.get(k + "_id"))

            # Transform numerical strings to actual numbers
            # This is required as sometimes strings are returned by the API
            if isinstance(av, str) and av.isdigit():
                av = int(av)
            if isinstance(iv, str) and iv.isdigit():
                iv = int(iv)

            # Ensure that item value matches attribute value, otherwise fail
            if iv != av:
                raise Exception(
                    f"found item with mismatched value [{iv}], expected [{av}] for key [{k}], "
                    f"during lookup {endpoint} with {attributes}"
                )

        return existing

    def upsert(self, endpoint, attributes, values, *, ignores=None, request_opts=None):
        # Build list of ignored keys
        ignores = [] if ignores is None else ignores

        # Lookup existing item by unique attributes
        existing = self.lookup(endpoint, attributes)

        # Create new item if currently missing
        if existing is None:
            return self.create(
                endpoint=endpoint,
                values=values,
                **request_opts,
            )

        # Otherwise compare existing item with provided values
        diff = []
        for k, v in values.items():
            # Skip if key is marked as being ignored
            if k in ignores:
                continue

            # If key does not exist or has different value, mark as modified
            if k not in existing or existing[k] != v:
                diff_header = "object key: " + k
                diff_entry = {
                    "before_header": diff_header,
                    "before": str(existing.get(k, "<missing>")) + "\n",
                    "after_header": diff_header,
                    "after": str(v) + "\n",
                }
                diff.append(diff_entry)

        # If item has not been modified, return without changes
        if not diff:
            return {
                "changed": False,
                "msg": "No changes made, all values are equal",
                "id": existing["id"],
                "data": existing,
                "diff": [],
            }

        # Otherwise trigger update and append diff values
        result = self.update(
            endpoint=endpoint,
            id=existing["id"],
            values=values,
            **request_opts,
        )
        result["diff"] = diff

        return result

    def list_simple_devices(self):
        response = self._session.get("/api/dashboard/v1/simple-device")
        return response["results"]

    def list_device_groups(self):
        response = self._session.get("/api/dashboard/v1/device-group")
        return response["results"]

    @property
    def session(self):
        return self._session


class NcaeSession:
    def __init__(self, base_url, timeout=60, validate_certs=True):
        # Store base URL without trailing slashes
        self._base_url = base_url.strip("/")

        # Use custom cookie jar to workaround issues with "Secure" cookies.
        # This is required as otherwise authentication does not work when using http://.
        is_http_scheme = str(urlsplit(base_url).scheme).lower() == "http"
        if is_http_scheme:
            self._cookies = cookiejar.CookieJar(
                policy=cookiejar.DefaultCookiePolicy(
                    secure_protocols=("http", "https", "ws", "wss"),
                )
            )
        else:
            self._cookies = cookiejar.CookieJar()

        # Initialize HTTP client for API calls towards NCAE Core
        self._http_client = Request(
            http_agent="NCAE Ansible Client",
            cookies=self._cookies,
            timeout=timeout,
            validate_certs=validate_certs,
        )

    def get(self, url, params=None, **kwargs):
        if params is not None:
            params = {key: value for key, value in params.items() if value is not None}
            url = f"{url}?{urlencode(params)}"

        return self._request(
            method="GET",
            url=url,
            **kwargs,
        )

    def post(self, url, data, **kwargs):
        return self._request(
            method="POST",
            url=url,
            data=data,
            **kwargs,
        )

    def put(self, url, data, **kwargs):
        return self._request(
            method="PUT",
            url=url,
            data=data,
            **kwargs,
        )

    def patch(self, url, data, **kwargs):
        return self._request(
            method="PATCH",
            url=url,
            data=data,
            **kwargs,
        )

    def delete(self, url, **kwargs):
        return self._request(
            method="DELETE",
            url=url,
            **kwargs,
        )

    def _request(self, *, method, url, data=None, **kwargs):
        # Sanitize request method
        method = str(method).upper()

        # Read well-known custom options
        headers = dict(kwargs.get("headers", {}))
        multipart = bool(kwargs.get("multipart", False))

        # Prepare body based on specified data
        if data and multipart:
            form_data = self._convert_to_form_data(data)
            header, data = prepare_multipart(form_data)
            headers["Content-Type"] = header
        elif data:
            headers.setdefault("Content-Type", "application/json")
            data = json.dumps(data)

        # Execute actual HTTP request and wrap any errors
        try:
            response = self._http_client.open(
                method=method,
                url=urljoin(self._base_url, url),
                headers=headers,
                data=data,
            )
        except HTTPError as e:
            # Return None for DELETE requests which result in 404
            # This is required to maintain idempotency
            if method == "DELETE" and e.code == 404:
                return None

            # Otherwise throw an exception with further details
            error_body = e.read()
            error_msg = "Calling NCAE API using [%s %s] failed with status [%d]: %s" % (
                method,
                e.url,
                e.code,
                error_body,
            )
            raise Exception(error_msg)

        # Return empty dictionary for 204 No Content
        if response.code == 204:
            return {}

        # Otherwise parse body as JSON payload
        return json.loads(response.read())

    @classmethod
    def _convert_to_form_data(cls, value):
        if not isinstance(value, dict):
            raise Exception("Unable to convert type [%s] into form-data, expected dict" % (value,))

        form_data = {}
        for key, value in iteritems(value):
            if isinstance(value, str):
                form_data[key] = value
            elif isinstance(value, bool):
                form_data[key] = "true" if value else "false"
            elif isinstance(value, int) or isinstance(value, float):
                form_data[key] = str(value)
            elif isinstance(value, dict):
                # Pass dictionaries as-is, with the assumption that those contain file properties
                # If they do not, error handling is already provided as part of prepare_multipart
                form_data[key] = value
            elif value is None:
                # Exclude the key from the formdata if not set
                pass
            else:
                raise Exception("Unable to convert key [%s] with type [%s] into form-data" % (key, type(value)))

        return form_data

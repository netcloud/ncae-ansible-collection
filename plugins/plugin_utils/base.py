# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

from abc import abstractmethod

__metaclass__ = type

from ansible.module_utils.basic import AnsibleFallbackNotFound
from ansible.module_utils.six import iteritems
from ansible.plugins.action import ActionBase as AnsibleActionBase
from ansible_collections.netcloud.ncae.plugins.plugin_utils.ncae import NcaeClient


class ActionBase(AnsibleActionBase):
    def run(self, tmp=None, task_vars=None):
        # Prepare task result dictionary
        self._result = super().run(tmp, task_vars)
        self._result["changed"] = False
        self._result["failed"] = False
        self._result["diff"] = []
        self._result["msg"] = None

        # Configure supported modes
        self._supports_async = False
        self._supports_check_mode = True

        # Store internal references
        self._task_vars = task_vars

        # Parse task arguments
        self._task_args = self._parse_task_args()

        # Run actual plugin code and merge result, if any, with our dict
        result = self.execute()
        if result:
            self._result.update(result)

        return self._result

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def _get_validate_spec(self):
        pass

    def _run_action(self, name, args):
        # Clone task and replace action and arguments
        new_task = self._task.copy()
        new_task.action = name
        new_task.args = args

        # Resolve action plugin via shared loader
        plugin = self._shared_loader_obj.action_loader.get(
            name,
            task=new_task,
            connection=self._connection,
            play_context=self._play_context,
            loader=self._loader,
            templar=self._templar,
            shared_loader_obj=self._shared_loader_obj,
        )

        # Raise exception if plugin is not found
        if not plugin:
            raise Exception("Could not find action plugin: " + name)

        # Run resolved action plugin
        return plugin.run(task_vars=self._task_vars)

    def _run_module(self, name, args):
        return self._execute_module(
            module_name=name,
            module_args=args,
            task_vars=self._task_vars,
        )

    def _parse_task_args(self):
        # Retrieve validation spec for validation
        validate_spec = self._get_validate_spec()

        # Support ansible-core releases <= 2.12 by partial legacy support
        if not hasattr(self, "validate_argument_spec"):
            return self._parse_task_args_legacy(validate_spec)

        # Validate and retrieve sanitized arguments
        validated_task_args = self.validate_argument_spec(
            argument_spec=validate_spec.get("argument_spec", {}),
            mutually_exclusive=validate_spec.get("mutually_exclusive", []),
            required_together=validate_spec.get("required_together", []),
            required_one_of=validate_spec.get("required_one_of", []),
            required_if=validate_spec.get("required_if", []),
            required_by=validate_spec.get("required_by", {}),
        )[1]

        return validated_task_args

    def _parse_task_args_legacy(self, spec):
        # Obtain argument spec and copy task arguments for processing
        argument_spec = spec.get("argument_spec", {})
        task_args = self._task.args.copy()

        # Call ansible.builtin.validate_argument_spec for validation
        # This is required as the re-implementation below has (almost) no sanity checks
        result = self._run_action(
            name="ansible.builtin.validate_argument_spec",
            args={
                "argument_spec": argument_spec,
                "provided_arguments": task_args,
            },
        )

        # Raise exception when module execution has failed
        if result.get("failed"):
            errors = result.get("argument_errors", ["<unknown>"])
            raise Exception("invalid arguments: " + ", ".join(errors))

        # Partial re-implementation of argument handling from Ansible Core >=2.13
        # This skips a lot of sanity checks, but does the most important logic stuff
        for arg_name, arg_spec in iteritems(argument_spec):
            # Skip processing if argument exists
            if arg_name in task_args:
                continue

            # Attempt resolving of argument via fallback
            try:
                fallback = arg_spec.get("fallback")
                if fallback and len(fallback) >= 2:
                    # [0] contains the fallback function
                    # [1] contains the arguments for the fallback function
                    task_args[arg_name] = fallback[0](*fallback[1])

                    # Proceed with next argument when fallback was successful
                    continue
            except AnsibleFallbackNotFound:
                pass

            # Raise exception when required without default
            if arg_spec.get("required") and "default" not in arg_spec:
                raise Exception("missing argument: " + arg_name)

            # Apply default value
            task_args[arg_name] = arg_spec.get("default", None)

        return task_args


class NcaeActionBase(ActionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._ncae_client = None

    @property
    def ncae_client(self):
        if self._ncae_client is None:
            self._ncae_client = NcaeClient(
                base_url=self._task_args["ncae_base_url"],
                username=self._task_args["ncae_username"],
                password=self._task_args["ncae_password"],
                validate_certs=self._task_args["validate_certs"],
            )

        return self._ncae_client


class NcaeRestActionBase(NcaeActionBase):
    IGNORED_KEYS = (
        "state",
        "id",
        "ncae_base_url",
        "ncae_username",
        "ncae_password",
        "validate_certs",
    )

    def execute(self):
        state = self._task_args["state"]
        if state == "present":
            return self._map_response(self._manage_present())
        elif state == "absent":
            return self._map_response(self._manage_absent())
        else:
            raise Exception("invalid state: " + state)

    @abstractmethod
    def get_endpoint(self):
        pass

    def get_request_options(self):
        return {}

    def get_ignored_keys(self):
        return set()

    def get_unique_keys(self):
        return set()

    def get_mappings(self):
        return {}

    def build_object_attributes(self, values):
        unique_keys = self.get_unique_keys()
        return {k: v for k, v in iteritems(values) if k in unique_keys}

    def build_object_values(self):
        mappings = self.get_mappings()
        data = {}
        for key, value in iteritems(self._task_args):
            # Skip ignored keys
            if key in self.IGNORED_KEYS:
                continue

            # Attempt to map key and store as object data
            mapped_key = mappings.get(key, key)
            data[mapped_key] = value

        return data

    def _map_response(self, response):
        # Build reverse mappings to translate response into our representation
        mappings = self.get_mappings()
        reverse_mappings = {v: k for k, v in iteritems(mappings)}

        # Use generated mapping for transforming response
        data = {}
        original_data = response.get("data", {})
        for key, value in iteritems(response.get("data", {})):
            mapped_key = reverse_mappings.get(key, key)
            data[mapped_key] = value

        # Override data for response and return
        response["original_data"] = original_data
        response["data"] = data
        return response

    def _manage_present(self):
        values = self.build_object_values()

        # If an ID has been specified, directly update the object
        if self._task_args["id"]:
            return self.ncae_client.update(
                endpoint=self.get_endpoint(),
                id=self._task_args["id"],
                values=values,
                **self.get_request_options(),
            )

        # Determine unique keys for upsert operation
        # If no unique keys exist, create a new one
        unique_keys = self.get_unique_keys()
        if not unique_keys:
            return self.ncae_client.create(
                endpoint=self.get_endpoint(),
                values=values,
                **self.get_request_options(),
            )

        # Execute upsert operation to create/update as needed
        attributes = self.build_object_attributes(values)
        return self.ncae_client.upsert(
            endpoint=self.get_endpoint(),
            attributes=attributes,
            values=values,
            ignores=self.get_ignored_keys(),
            request_opts=self.get_request_options(),
        )

    def _manage_absent(self):
        # If an ID has been specified, directly delete the object
        if self._task_args["id"]:
            return self.ncae_client.delete(
                endpoint=self.get_endpoint(),
                id=self._task_args["id"],
            )

        # Otherwise lookup existing item by unique keys
        values = self.build_object_values()
        attributes = self.build_object_attributes(values)
        existing = self.ncae_client.lookup(
            endpoint=self.get_endpoint(),
            attributes=attributes,
            request_opts=self.get_request_options(),
        )

        # If no item has been found, consider as successful
        if not existing:
            return {"changed": False}

        # Otherwise trigger deletion by found ID
        return self.ncae_client.delete(
            endpoint=self.get_endpoint(),
            id=existing["id"],
            **self.get_request_options(),
        )

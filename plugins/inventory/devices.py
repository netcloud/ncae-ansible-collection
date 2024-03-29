# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
    name: devices
    short_description: Uses NCAE as an inventory source for all devices.
    description:
        - This inventory plugin gathers all devices and associated groups from NCAE.
        - All devices are automatically added as Ansible hosts with their ID prefixed by I(device_prefix).
        - All groups are automatically added to the inventory with their slug prefixed by I(group_prefix).
        - Devices are automatically linked to their associated groups.
        - The IP address of the device is automatically used for 'ansible_host'.
        - Additional device facts are prefixed by I(facts_prefix).
    options:
        ncae_base_url:
            description: Base URL of NCAE instance to query without trailing slash.
            type: str
            required: true
            env:
                - name: NCAE_BASE_URL
                - name: NCAE_URL
        ncae_username:
            description: Username for authenticating against NCAE.
            type: str
            required: true
            env:
                - name: NCAE_USERNAME
        ncae_password:
            description: Password for authenticating against NCAE.
            type: str
            required: true
            env:
                - name: NCAE_PASSWORD
        validate_certs:
            description: Whether to verify SSL certificates for API connections.
            type: bool
            default: false
            env:
                - name: NCAE_VALIDATE_CERTS
        device_prefix:
            description: Prefix to be used in front of device ids.
            type: str
            default: ncae_device_
            env:
                - name: NCAE_INVENTORY_DEVICE_PREFIX
        group_prefix:
            description: Prefix to be used in front of group slugs.
            type: str
            default: ncae_group_
            env:
                - name: NCAE_INVENTORY_GROUP_PREFIX
        facts_prefix:
            description: Prefix to be used in front of device facts.
            type: str
            default: ncae_
            env:
                - name: NCAE_INVENTORY_FACTS_PREFIX
        nest_groups:
            description:
                - Specifies whether a group should contain hosts associated with child groups.
                - When enabled, the behavior matches with regular YAML/INI inventories containing nested groups.
                - When disabled, hosts are only added to groups they directly belong to.
            type: bool
            default: true
            env:
                - name: NCAE_INVENTORY_NEST_GROUPS

"""

EXAMPLES = """
# Sample configuration for NCAE devices inventory
plugin: netcloud.ncae.devices
ncae_base_url: https://ncae.example.com
ncae_username: admin
ncae_password: secret
validate_certs: true
"""

from collections import defaultdict

from ansible.module_utils.six import iteritems
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible_collections.netcloud.ncae.plugins.plugin_utils.ncae import NcaeClient


class InventoryModule(BaseInventoryPlugin):
    NAME = "netcloud.ncae.devices"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._client = None
        self._device_prefix = None
        self._group_prefix = None
        self._facts_prefix = None
        self._nest_groups = None

    def parse(self, inventory, loader, path, cache=True):
        # Initialize state and config for inventory plugin
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)

        # Read module configuration
        self._device_prefix = self.get_option("device_prefix")
        self._group_prefix = self.get_option("group_prefix")
        self._facts_prefix = self.get_option("facts_prefix")
        self._nest_groups = self.get_option("nest_groups")

        # Actually populate inventory
        self._populate()

    def _populate(self):
        # Fetch list of all devices and groups from NCAE
        devices = self._get_ncae_client().list_simple_devices()
        groups = self._get_ncae_client().list_device_groups()

        # Add device groups to Ansible inventory
        group_map = {}
        group_parents = defaultdict(list)
        for group in groups:
            # Generate group name and add to inventory
            group_name = self._group_prefix + group["tree_slug"]
            group_map[group["id"]] = group_name
            self.inventory.add_group(group_name)

            # Persist parents associated with given group
            # The last element in tree_path is the node itself and not a parent
            group_parents[group["id"]] = group["tree_path"][:-1]

        # Add devices to Ansible inventory
        for device in devices:
            # Generate device name and facts for Ansible inventory
            device_name = self._device_prefix + str(device["id"])
            facts = {
                "device_id": device["id"],
                "device_name": device["name"],
            }

            # Add device to inventory and configure IP as target host
            self.inventory.add_host(device_name)
            self.inventory.set_variable(device_name, "ansible_host", device["ip"])

            # Add facts to device with configured prefix
            for fact_key, fact_value in iteritems(facts):
                self.inventory.set_variable(device_name, self._facts_prefix + fact_key, fact_value)

            # Associate device with all its directly attached groups
            for group_id in device["groups"]:
                self.inventory.add_child(group_map[group_id], device_name)

                # Associate device with all parent groups if enabled
                if self._nest_groups:
                    for parent_id in group_parents[group_id]:
                        self.inventory.add_child(group_map[parent_id], device_name)

    def _get_ncae_client(self):
        if self._client is None:
            self._client = NcaeClient(
                base_url=self.get_option("ncae_base_url"),
                username=self.get_option("ncae_username"),
                password=self.get_option("ncae_password"),
                validate_certs=self.get_option("validate_certs"),
            )

        return self._client

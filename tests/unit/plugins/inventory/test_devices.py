# -*- coding: utf-8 -*-
# Copyright (c) 2023 Netcloud AG
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import pytest

from ansible.inventory.data import InventoryData
from ansible_collections.netcloud.ncae.plugins.inventory.devices import InventoryModule
from ansible_collections.netcloud.ncae.tests.unit.mock.ncae import MockNcaeClient


@pytest.fixture(scope="module")
def inventory():
    r = InventoryModule()
    r.inventory = InventoryData()
    return r


def load_fixture(name):
    with open(f"tests/unit/plugins/inventory/fixtures/{name}.json", "rb") as fp:
        return json.load(fp)


def mock_options(options):
    return lambda key: options.get(key, False)


def test_populate_without_group_nesting(inventory, mocker):
    # Manually specify module options
    inventory._device_prefix = "ncae_device_"
    inventory._group_prefix = "ncae_group_"
    inventory._facts_prefix = "ncae_"
    inventory._nest_groups = False

    # Mock ncae client and populate inventory
    inventory._client = MockNcaeClient(mocker)
    inventory._populate()

    # Gather different devices from inventory
    device_multi = inventory.inventory.get_host("ncae_device_1")
    device_global = inventory.inventory.get_host("ncae_device_2")
    device_basel = inventory.inventory.get_host("ncae_device_3")
    device_bern = inventory.inventory.get_host("ncae_device_4")
    device_winterthur = inventory.inventory.get_host("ncae_device_5")

    # Ensure expected groups are present
    assert "ncae_group_offices" in inventory.inventory.groups
    assert "ncae_group_offices__basel" in inventory.inventory.groups
    assert "ncae_group_offices__bern" in inventory.inventory.groups
    assert "ncae_group_offices__winterthur" in inventory.inventory.groups

    # Gather different groups from inventory
    group_global = inventory.inventory.groups["ncae_group_offices"]
    group_basel = inventory.inventory.groups["ncae_group_offices__basel"]
    group_bern = inventory.inventory.groups["ncae_group_offices__bern"]
    group_winterthur = inventory.inventory.groups["ncae_group_offices__winterthur"]

    # Ensure appropriate device memberships
    assert group_global.hosts == [device_global]
    assert group_basel.hosts == [device_multi, device_basel]
    assert group_bern.hosts == [device_multi, device_bern]
    assert group_winterthur.hosts == [device_winterthur]

    # Gather variables for one of the devices
    vars_global = device_global.get_vars()

    # Ensure device facts are present
    assert vars_global["ansible_host"] == "192.168.254.2"
    assert vars_global["ncae_device_id"] == 2
    assert vars_global["ncae_device_name"] == "device-global"


def test_populate_with_group_nesting(inventory, mocker):
    # Manually specify module options
    inventory._device_prefix = "ncae_device_"
    inventory._group_prefix = "ncae_group_"
    inventory._facts_prefix = "ncae_"
    inventory._nest_groups = True

    # Mock ncae client and populate inventory
    inventory._client = MockNcaeClient(mocker)
    inventory._populate()

    # Gather different devices from inventory
    device_multi = inventory.inventory.get_host("ncae_device_1")
    device_global = inventory.inventory.get_host("ncae_device_2")
    device_basel = inventory.inventory.get_host("ncae_device_3")
    device_bern = inventory.inventory.get_host("ncae_device_4")
    device_winterthur = inventory.inventory.get_host("ncae_device_5")

    # Ensure expected groups are present
    assert "ncae_group_offices" in inventory.inventory.groups
    assert "ncae_group_offices__basel" in inventory.inventory.groups
    assert "ncae_group_offices__bern" in inventory.inventory.groups
    assert "ncae_group_offices__winterthur" in inventory.inventory.groups

    # Gather different groups from inventory
    group_offices = inventory.inventory.groups["ncae_group_offices"]
    group_basel = inventory.inventory.groups["ncae_group_offices__basel"]
    group_bern = inventory.inventory.groups["ncae_group_offices__bern"]
    group_winterthur = inventory.inventory.groups["ncae_group_offices__winterthur"]

    # Ensure appropriate device memberships
    assert group_offices.hosts == [
        device_multi,
        device_global,
        device_basel,
        device_bern,
        device_winterthur,
    ]
    assert group_basel.hosts == [device_multi, device_basel]
    assert group_bern.hosts == [device_multi, device_bern]
    assert group_winterthur.hosts == [device_winterthur]

    # Gather variables for one of the devices
    vars_global = device_global.get_vars()

    # Ensure device facts are present
    assert vars_global["ansible_host"] == "192.168.254.2"
    assert vars_global["ncae_device_id"] == 2
    assert vars_global["ncae_device_name"] == "device-global"

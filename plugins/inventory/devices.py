from ansible.plugins.inventory import BaseInventoryPlugin

from ansible_collections.netcloud.ncae.plugins.module_utils.ncae import NcaeClient

DOCUMENTATION = r"""
    name: netcloud.ncae.devices
    short_description: Uses NCAE as an inventory source for all devices.
    description:
        - This inventory plugin gathers all devices and associated groups from NCAE.
        - All devices are automatically added as Ansible hosts, named 'device_<id>'.
        - All groups are automatically added to the inventory, named 'group_<full slug>'.
        - Devices are automatically linked to their associated groups.
        - The IP address of the device is automatically used for 'ansible_host'.
        - The ID and name of the device are stored in 'ncae_device_id' and 'ncae_device_name' respectively.
    options:
        ncae_base_url:
            description: Base URL of NCAE instance to query without trailing slash
            type: string
            required: true
            env:
                - name: NCAE_INVENTORY_BASE_URL
        ncae_username:
            description: Username for authenticating against NCAE
            type: string
            required: true
            env:
                - name: NCAE_INVENTORY_USERNAME
        ncae_password:
            description: Password for authenticating against NCAE
            type: string
            required: true
            env:
                - name: NCAE_INVENTORY_PASSWORD
        ncae_validate_certs:
            description: Whether to verify SSL certificates when connecting to NCAE
            type: bool
            default: true
            env:
                - name: NCAE_INVENTORY_VALIDATE_CERTS
"""


class InventoryModule(BaseInventoryPlugin):
    NAME = "netcloud.ncae.devices"

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._client = None

    def parse(self, inventory, loader, path, cache=True):
        # Initialize state and config for inventory plugin
        super().parse(inventory, loader, path, cache)
        self._read_config_data(path)

        # Fetch list of all devices and groups from NCAE
        devices = self._get_ncae_client().list_simple_devices()
        groups = self._get_ncae_client().list_device_groups()

        # Add device groups to Ansible inventory
        group_map = {}
        for group in groups:
            group_name = f"group_{group['tree_slug']}"
            group_map[group["id"]] = group_name
            self.inventory.add_group(group_name)

        # Add devices to Ansible inventory
        for device in devices:
            device_name = f"device_{device['id']}"
            self.inventory.add_host(device_name)
            self.inventory.set_variable(device_name, "ncae_device_id", device["id"])
            self.inventory.set_variable(device_name, "ncae_device_name", device["name"])
            self.inventory.set_variable(device_name, "ansible_host", device["ip"])

            # Add device as child to all associated device groups
            for group_id in device["groups"]:
                self.inventory.add_child(group_map[group_id], device_name)

    def _get_ncae_client(self):
        if self._client is None:
            self._client = NcaeClient(
                base_url=self.get_option("ncae_base_url"),
                username=self.get_option("ncae_username"),
                password=self.get_option("ncae_password"),
                validate_certs=self.get_option("ncae_validate_certs"),
            )

        return self._client

# Ansible Collection - netcloud.ncae

This repository contains the Ansible Collection for the Netcloud Automation Engine, also known as NCAE. It exposes several plugins and roles for interacting with NCAE Core and allows the development of custom modules.

## Usage
Documentation about all the modules and plugins provided by this Ansible collection can be found on the auto-generated documentation hosted on [GitHub Pages](https://netcloud.github.io/ncae-ansible-collection/collections/netcloud/ncae/index.html).

As of today, only the inventory plugin `devices` is being provided. All other functionality to interact with NCAE still remains within the `legacy` role, which offers various tasks that can be individually included into your playbook. To find more information about this role, check out [the README file](roles/legacy/README.md) within the directory `roles/legacy`.

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests to this project.

## Versioning
This repository uses [Semantic Versioning](https://semver.org/) as its versioning policy. You can quickly view all available versions by checking the [available tags](https://github.com/netcloud/ncae-ansible-collection/tags) on this repository.

## License
GNU General Public License v3.0 - see [COPYING](COPYING) for further details.

## Authors
- **Andreas Graber** - _Various improvements and bugfixes_ - @andreasgraber
- **Pascal Mathis** - _Creation and maintenance of collection_ - @ppmathis
- **Richard Strnad** - _Initial work on Ansible role_ - @richardstrnad

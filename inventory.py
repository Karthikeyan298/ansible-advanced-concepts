#!/usr/bin/env python

'''
custom dynamic inventory script for Ansible, in Python.
'''

import os
import sys
import argparse
import json

class CustomInventory(object):

    def __init__(self):
        self.inventory = {}
        self.read_cli_args()

        # Called with `--list`.
        if self.args.list:
            self.inventory = self.custom_inventory_groups()
        # Called with `--host [hostname]`.
        elif self.args.host:
            # Not implemented, since we return _meta info `--list`.
            self.inventory = self.custom_inventory_host(self.args.host)
        # If no groups or vars are present, return empty inventory.
        else:
            self.inventory = self.empty_inventory()
        print(json.dumps(self.inventory, sort_keys=True, indent=2))

    # custom inventory for testing.
    def custom_inventory_groups(self):
        hosts_file = open("iplist.json")
        hosts_json = json.load(hosts_file)
        try:
            custom_inventory = {
                'collector_hosts': {
                    'hosts': hosts_json['collector_hosts']
                },
                'proxy_hosts': {
                    'hosts': hosts_json['proxy_hosts']
                },
            }
        except Exception as e:
            print('Please provide valid group name: {}'.format(e))
        
        return custom_inventory

    def custom_inventory_host(self, host):

        hosts_file = open('iplist.json', 'r').read()
        hosts_json = json.loads(str(hosts_file))
        hosts = {
            'ansible_host': host,
            'ansible_ssh_user': hosts_json['ssh_user'],
            'ansible_ssh_pass': hosts_json['ssh_pass']
        }

        return hosts


    # Empty inventory for testing.
    def empty_inventory(self):
        return {'_meta': {'hostvars': {

        }}}

    def read_cli_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--list', action = 'store_true')
        parser.add_argument('--host', action = 'store')
        self.args = parser.parse_args()

# Get the inventory.
CustomInventory()
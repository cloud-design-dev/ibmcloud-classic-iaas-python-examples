#!/usr/bin/env python3
# Author: Ryan Tiffany
# Copyright (c) 2023
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = 'ryantiffany'
import argparse
import os
import ibm_vpc
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from rich import box
from rich.console import Console
from rich.table import Table

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def get_regions():
    # use us-south endpoint to look up all regions
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://us-south.iaas.cloud.ibm.com/v1')
    response = service.list_regions().get_result()
    regions = response['regions']
    region_names = [region['name'] for region in regions]
    return region_names

def get_all_vpcs():
    regions = get_regions()
    all_vpcs = []
    for region in regions:
        vpcs = get_vpcs(region)
        all_vpcs.extend(vpcs)

    console = Console()

    table = Table(show_header=True, header_style="white", box=box.ROUNDED, title="All VPCs")
    table.add_column("Name")
    table.add_column("Region")
    table.add_column("Subnets")
    table.add_column("Instances")
    table.add_column("ID")

    for vpc in all_vpcs:
        table.add_row(vpc['name'], vpc['region'], vpc['subnets'], vpc['instances'], vpc['id'])

    console.print(table)

def get_vpcs(region):
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    list_vpcs = service.list_vpcs().get_result()['vpcs']
    vpcs = []
    for vpc in list_vpcs:
        vpc_info = {'name': vpc['name'], 'id': vpc['id'], 'region': region}
        list_subnets = service.list_subnets().get_result()['subnets']
        subnets_in_vpc = [subnet for subnet in list_subnets if subnet['vpc']['id'] == vpc['id']]
        public_subnets = sum(1 for subnet in subnets_in_vpc if subnet.get('public_gateway'))
        private_subnets = len(subnets_in_vpc) - public_subnets
        vpc_info['subnets'] = f"[green]{public_subnets}[/green] / [white]{private_subnets}[/white]"

        list_instances = service.list_instances().get_result()['instances']
        instances_in_vpc = [instance for instance in list_instances if instance['vpc']['id'] == vpc['id']]
        total_instances = len(instances_in_vpc)
        running_instances = len([instance for instance in instances_in_vpc if instance['status'] == 'running'])
        stopped_instances = total_instances - running_instances
        vpc_info['instances'] = f"[yellow]{total_instances}[/yellow] / [green]{running_instances}[/green] / [red]{stopped_instances}[/red]"

        vpcs.append(vpc_info)

    return vpcs

if __name__ == '__main__':
    get_all_vpcs()

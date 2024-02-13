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
    table.add_column("VPC Name")
    table.add_column("VPC Region")
    table.add_column("VPC Subnets")
    table.add_column("VPC Compute Instances")
    table.add_column("VPC ID")

    for vpc in all_vpcs:
        total_instances = vpc['total_instances']
        running_instances = vpc['running_instances']
        stopped_instances = vpc['stopped_instances'] 
        public_subnets = vpc['public_subnets'] 
        private_subnets = vpc['private_subnets'] 

        subnet_text = f"[blue]{public_subnets} Public GW [/blue] / [white]{private_subnets} Private Only[/white]"
        instances_text = f"[yellow]{total_instances} Total[/yellow] / [green]{running_instances} Running[/green] / [red]{stopped_instances} Stopped[/red]"

        table.add_row(f"{vpc['name']}", vpc['region'], subnet_text, instances_text, vpc['id'])
    # for vpc in all_vpcs:
    #     instances_text = f"[yellow]str({vpc['instances']['total']}) Total[/yellow] / [green]str({vpc['instances']['running_instances']}) Running[/green] / [red]str({vpc['instances']['stopped_instances']}) Stopped[/red]"
    #     table.add_row(f"{vpc['name']}\n{vpc['id']}", vpc['region'], vpc['subnets'], instances_text)

    console.print(table)

def get_vpcs(region):
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    list_vpcs = service.list_vpcs().get_result()['vpcs']
    vpcs = []
    for vpc in list_vpcs:
        vpc_info = {'name': vpc['name'], 'id': vpc['id'], 'region': region}
        list_subnets = service.list_subnets().get_result()['subnets']
        total_subnets = [subnet for subnet in list_subnets if subnet['vpc']['id'] == vpc['id']]
        public_subnets = sum(1 for subnet in total_subnets if subnet.get('public_gateway'))
        private_subnets = len(total_subnets) - public_subnets
        vpc_info['public_subnets'] = public_subnets
        vpc_info['private_subnets'] = private_subnets

        list_instances = service.list_instances().get_result()['instances']
        instances_in_vpc = [instance for instance in list_instances if instance['vpc']['id'] == vpc['id']]
        total_instances = len(instances_in_vpc)
        running_instances = len([instance for instance in instances_in_vpc if instance['status'] == 'running'])
        stopped_instances = total_instances - running_instances
        vpc_info['total_instances'] = total_instances
        vpc_info['running_instances'] = running_instances
        vpc_info['stopped_instances'] = stopped_instances

        vpcs.append(vpc_info)

    return vpcs

if __name__ == '__main__':
    get_all_vpcs()

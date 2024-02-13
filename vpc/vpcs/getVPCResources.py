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


vpc_id = os.environ.get('VPC_ID')

if not vpc_id:
    raise ValueError("VPC_ID environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def set_client(region):
    # use us-south endpoint to look up all regions
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    return service

def get_vpc(region, vpc_id):
    service = set_client(region)
    response = service.get_vpc(id=vpc_id).get_result()
    return response

def get_subnets(region, vpc_id):
    service = set_client(region)
    response = service.list_subnets().get_result()
    subnets = [subnet for subnet in response['subnets'] if subnet['vpc']['id'] == vpc_id]
    return subnets


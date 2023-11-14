import argparse
import os

import ibm_vpc
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from rich import box
from rich.console import Console

from rich.tree import Tree

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def get_vpcs(region):
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')

    list_vpcs = service.list_vpcs().get_result()['vpcs']
    return list_vpcs

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List all VPCs in a region.')
    parser.add_argument('--region', type=str, required=True, help='The region to list VPCs from.')
    args = parser.parse_args()
    vpcs = get_vpcs(args.region)
    print(type(vpcs))
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='List all VPCs in a region.')
#     parser.add_argument('--region', type=str, required=True, help='The region to list VPCs from.')
#     args = parser.parse_args()

#     vpcs = get_vpcs(args.region)
#     print_vpcs(vpcs)

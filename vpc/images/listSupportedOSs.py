import argparse
import os

import ibm_vpc
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from rich import box
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def get_supported_os_list(region):
    # use us-south endpoint to look up all regions
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    response = service.list_operating_systems().get_result()
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List all VPCs in a region.')
    parser.add_argument('--region', type=str, required=True, help='The IBM Cloud VPC region to target for image search.')
    args = parser.parse_args()
    supported_operating_systems = get_supported_os_list(args.region)
    print(supported_operating_systems)




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

def get_volumes(region):
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    volumes = service.list_volumes().get_result()['volumes']
    return volumes

def get_detached_volumes(region):
  volumes = get_volumes(region)
  return [vol for vol in volumes if not vol.get('volume_attachments')]

def get_attached_volumes(region):
    volumes = get_volumes(region)
    return [vol for vol in volumes if vol.get('volume_attachments')]

def print_vols(volumes):
    console = Console()

    table = Table(show_header=True, header_style="bright_cyan", box=box.SQUARE_DOUBLE_HEAD)  # Change header style to bold purple
    table.add_column("Name")
    table.add_column("Profile")
    table.add_column("Size")
    table.add_column("Attached")
    table.add_column("Zone")
    table.add_column("Status")

    for vol in volumes:
        profile_name = vol.get('profile', {}).get('name', 'N/A')
        attached = 'Yes' if vol.get('volume_attachments') else 'No'
        zone_name = vol.get('zone', {}).get('name', 'N/A')
        table.add_row(
            vol['name'], 
            profile_name, 
            f"{vol['capacity']}GB",
            attached,
            zone_name,
            vol['status']
            )

    console.print(table)

try:
    parser = argparse.ArgumentParser(description='List all Volumes in a region.')
    parser.add_argument('--region', type=str, required=True, help='The VPC region to check for block storage volumes.')
    parser.add_argument('--show-detached', action='store_true', help='Only show detached Block volumes') 
    parser.add_argument('--show-attached', action='store_true', help='Only show attached Block volumes') 
    args = parser.parse_args()
    if args.show_detached:
        vols = get_detached_volumes(args.region)
    elif args.show_attached:
        vols = get_attached_volumes(args.region)
    else:
        vols = get_volumes(args.region)
    print_vols(vols)

except ApiException as e:
    print("Exception when calling VPC API: %s\n" % e)

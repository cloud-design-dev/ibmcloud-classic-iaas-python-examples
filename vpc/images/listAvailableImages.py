import argparse
import os

import ibm_vpc
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from rich import box
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn
import random


ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def random_color():
    return "#"+''.join([random.choice('0123456789ABCDEF') for _ in range(6)])

def get_available_images(region):
    # use us-south endpoint to look up all regions
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')
    response = service.list_images(
        status="available",
        visibility="public",
        limit=100
        ).get_result()
    get_all_images = response['images']
    return get_all_images

def display_images(region):
    available_images = sorted(get_available_images(region), key=lambda image: image['operating_system']['vendor'])
    all_images = []

    vendor_colors = {}

    # Create a table
    table = Table(show_header=True, header_style="bold magenta", box=box.ROUNDED, title="Available Images")
    table.add_column("OS Vendor")
    table.add_column("Family")
    table.add_column("Short Name")
    table.add_column("Version")
    table.add_column("Architecture")

    for image in available_images:
        family = image['operating_system']['family']
        architecture = image['operating_system']['architecture']
        vendor = image['operating_system']['vendor']
        short_name = image['operating_system']['name']
        version = image['operating_system']['version']

        # Assign a random color to each vendor
        if vendor not in vendor_colors:
            vendor_colors[vendor] = random_color()

        # Add a row to the table
        table.add_row(f"[color={vendor_colors[vendor]}]{vendor}[/color]", family, short_name, version, architecture)

    console = Console()
    console.print(table) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List all VPCs in a region.')
    parser.add_argument('--region', type=str, required=True, help='The IBM Cloud VPC region to target for image search.')
    args = parser.parse_args()
    display_images(region=args.region)
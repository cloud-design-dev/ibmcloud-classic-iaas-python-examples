import argparse
import os
import json 

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_container_registry.vulnerability_advisor_v4 import VulnerabilityAdvisorV4
from ibm_container_registry.container_registry_v1 import *
from rich import box
from rich.console import Console
from rich.table import Table

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

ibmcloud_account = os.environ.get('IBMCLOUD_ACCOUNT_ID')
if not ibmcloud_account:
    raise ValueError("IBMCLOUD_ACCOUNT_ID environment variable not found")

status_colors = {
  'OK': '[green]',
  'FAIL': '[red]',
  'INCOMPLETE': '[yellow]'
}


authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def get_all_images(region):
    client = VulnerabilityAdvisorV4(account=ibmcloud_account,authenticator=authenticator)
    client.set_service_url(f'https://{region}.icr.io/')
    response = client.account_status_query_path()
    scanreport_image_summary_list = response.get_result()['images']
    all_images = []
    for image in scanreport_image_summary_list:
        name_parts = image['name'].split('/')
        namespace = name_parts[1]
        image_name = name_parts[-1]
        status = image['status']
        issue_count = image['issue_count']
        vulnerability_count = image['vulnerability_count']
        configuration_issue_count = image['configuration_issue_count']
        all_images.append(image)
    
    return all_images
def print_all_images(images):

    console = Console()

    table = Table(show_header=True, header_style="white", box=box.ROUNDED)
    table.sort_by = 'Namespace'
    table.add_column("Namespace")
    table.add_column("Image")
    table.add_column("Scan status")
    table.add_column("Total Issues")
    table.add_column("Vulnerabilities Issues")
    table.add_column("Configuration Issues")

    for image in images:
        status_color = status_colors.get(image['status'], '')
        colored_status = f"{status_color}{image['status']}[/]"
        name_parts = image['name'].split('/')
        namespace = name_parts[1]
        image_name = name_parts[-1]
        table.add_row(namespace, image_name, colored_status, str(image['issue_count']), str(image['vulnerability_count']), str(image['configuration_issue_count']))

    console.print(table)


try:
    parser = argparse.ArgumentParser(description='List all images in a region.')
    parser.add_argument('--region', type=str, required=True, help='The region to target for listing images.')
    args = parser.parse_args()
    images = get_all_images(args.region)
    print_all_images(images)
except ApiException as e:
    print(f"Failed to list images in region {args.region}: {e}")
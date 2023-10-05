import os
import sys
import time
import json
import argparse
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException  
from rich import box
from rich.console import Console
from rich.table import Table

ibmApiKey = os.environ.get('IBMCLOUD_API_KEY')
if not ibmApiKey:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmApiKey,
    client_id='bx',
    client_secret='bx'  # pragma: allowlist secret
)

status_colors = {
  'ACTIVE': '[green]',
  'FAILED': '[red]',
  'INACTIVE': '[yellow]'
}

def get_regional_workspaces(region):
    client  = SchematicsV1(authenticator=authenticator)
    schematicsURL = 'https://' + region + '.schematics.cloud.ibm.com'
    client.set_service_url(schematicsURL)
    all_workspaces = []
    workspaces = client.list_workspaces().get_result()['workspaces']
    for workspace in workspaces:
        workspace['region'] = region
        name = workspace['name']
        status = workspace['status']
        created_by = workspace['created_by']
        all_workspaces.append(workspace)
    console = Console()

    table = Table(show_header=True, header_style="white", box=box.ROUNDED, title="All Schematics Workspaces")
    table.add_column("Name")
    table.add_column("Region")
    table.add_column("Status")
    table.add_column("Owner")
    table.add_column("ID")

    for workspace in all_workspaces:
        status_color = status_colors.get(workspace['status'], '')
        colored_status = f"{status_color}{workspace['status']}[/]"
        table.add_row(workspace['name'], workspace['region'], colored_status, workspace['created_by'], workspace['id'])

    console.print(table)

try:
    parser = argparse.ArgumentParser(description='List all Schematics workspaces in a region.')
    parser.add_argument('--region', type=str, required=True, help='The region to target for listing workspaces.')
    args = parser.parse_args()
    workspaces = get_regional_workspaces(args.region)
except ApiException as e:
    print("ERROR: " + str(e.code) + " " + e.message)

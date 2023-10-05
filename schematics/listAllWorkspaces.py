import os
import sys
import time
import json
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException  
from ibm_platform_services import ResourceControllerV2
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

def get_schematics_regions():
    client  = SchematicsV1(authenticator=authenticator)
    schematicsURL = 'https://us-south.schematics.cloud.ibm.com'
    client.set_service_url(schematicsURL)
    schematics_regions = []
    schematics_locations_list = client.list_locations(headers={'X-Feature-Region-Visibility' : 'true'}).get_result()
    for location in schematics_locations_list['locations']:
        region = location['region']
        schematics_regions.append(region)
    return schematics_regions

def target_schematics_region(region):
    client  = SchematicsV1(authenticator=authenticator)
    schematicsURL = 'https://' + region + '.schematics.cloud.ibm.com'
    client.set_service_url(schematicsURL)
    return client

def get_all_workspaces():
    regions = get_schematics_regions()
    all_workspaces = []
    for region in regions:
        client = target_schematics_region(region)
        workspaces = client.list_workspaces().get_result()['workspaces']
        for workspace in workspaces:
            workspace['region'] = region
            name = workspace['name']
            status = workspace['status']
            created_by = workspace['created_by']
            # workspace_id = workspace['id']
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
    workspaces = get_all_workspaces()
except ApiException as e:
    print("ERROR: " + str(e.code) + " " + e.message)
# refreshToken = authenticator.token_manager.request_token()['refresh_token']
# client  = SchematicsV1(authenticator=authenticator)
# schematicsURL = 'https://us-south.schematics.cloud.ibm.com'
# client.set_service_url(schematicsURL)

# schematics_locations_list = client.list_locations(headers={'X-Feature-Region-Visibility' : 'true'}).get_result()
# schematics_regions = []
# for location in schematics_locations_list['locations']:
#     region = location['region']
#     schematics_regions.append(region)

# print(json.dumps(schematics_regions, indent=2))


import argparse
import os

from ibm_secrets_manager_sdk.secrets_manager_v2 import *
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from rich import box
from rich.console import Console
from rich.table import Table
from rich.progress import Progress, BarColumn

def ibm_client():

    ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
    if not ibmcloud_api_key:
        raise ValueError("IBMCLOUD_API_KEY environment variable not found")

    authenticator = IAMAuthenticator(apikey=ibmcloud_api_key)
    return authenticator

def secrets_manager_client():
    authenticator = ibm_client()
    sm_instance_id = os.environ.get('SM_INSTANCE_ID')
    if not sm_instance_id:
        raise ValueError("SM_INSTANCE_ID environment variable not found")

    sm_instance_region = os.environ.get('SM_INSTANCE_REGION')
    if not sm_instance_region:
        raise ValueError("SM_INSTANCE_REGION environment variable not found")

    secrets_manager_service = SecretsManagerV2(authenticator=authenticator)
    secrets_manager_service.set_service_url(f'https://{sm_instance_id}.{sm_instance_region}.secrets-manager.appdomain.cloud')
    return secrets_manager_service

def get_secret_groups():
    secrets_manager_service = secrets_manager_client()
    get_secret_groups = secrets_manager_service.list_secret_groups().get_result()['secret_groups']
    return get_secret_groups

def secret_group_table():
    sm_instance_id = os.environ.get('SM_INSTANCE_ID')
    table = Table(show_header=True, header_style="bold blue", box=box.HEAVY_HEAD, title="Secrets Groups")
    table.add_column("Group Name")
    table.add_column("ID")
    table.add_column("Created By")
    table.add_column("Description")

    console = Console()
    secret_groups = get_secret_groups()
    for secret_group in secret_groups:
        sm_name = secret_group['name']
        sm_description = secret_group['description']
        sm_id = secret_group['id']
        sm_created_by = secret_group['created_by']

        table.add_row(sm_name, sm_id, sm_created_by, sm_description)
    
    console.print(table)
try:
    secret_group_table()
except ApiException as e:
    print("Failed to list secret groups: {0}".format(e.message))
# sm_instance_id = os.environ.get('SM_INSTANCE_ID')
# if not sm_instance_id:
#     raise ValueError("SM_INSTANCE_ID environment variable not found")


# sm_instance_region = os.environ.get('SM_INSTANCE_REGION')
# if not sm_instance_region:
#     raise ValueError("SM_INSTANCE_REGION environment variable not found")

# secrets_manager_service = SecretsManagerV2(authenticator=authenticator)
# secrets_manager_service.set_service_url(f'https://{sm_instance_id}.{sm_instance_region}.secrets-manager.appdomain.cloud')

# get_secret_groups = secrets_manager_service.list_secret_groups().get_result()['secret_groups']
# for secret_group in get_secret_groups:
#     print(secret_group['name'])


    

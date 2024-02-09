import argparse
import os
from prettytable import PrettyTable
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

def get_all_secrets():
    secrets_manager_service = secrets_manager_client()
    all_results = []
    pager = SecretsPager(
        client=secrets_manager_service,
        limit=50
        )

    while pager.has_next():
        next_page = pager.get_next()
        assert next_page is not None
        all_results.extend(next_page)
    return all_results

def display_secrets_in_table():
    all_secrets = get_all_secrets()
    sorted_all_secrets = sorted(all_secrets, key=lambda secret: secret['secret_group_id'])
    table = Table(show_header=True, header_style="bold blue", box=box.HEAVY_HEAD, title="All Secrets in Secrets Manager Instance")
    table.add_column("Secret Name")
    table.add_column("Secret Type")
    table.add_column("Secret ID")
    table.add_column("Downloaded (T/F)")
    table.add_column("Secret Group ID")
    table.add_column("Labels")
    console = Console()
    for secret in all_secrets:
        secret_name = secret['name']
        secret_type = secret['secret_type']
        secret_group_id = secret['secret_group_id']
        secret_id = secret['id']
        labels = type(secret['labels'])
        downloaded = str(secret['downloaded'])

        table.add_row(secret_name, secret_type, secret_id, downloaded, secret_group_id, labels)
    
    console.print(table)



    # console = Console()
    # for secret in all_secrets:
    #     table.add_row([secret['name'], secret['secret_type'], secret['secret_group_id'], secret['downloaded']])
    # console.print(table)

# Get all secrets

try:
    all_secrets = get_all_secrets()
    print(all_secrets)
    print(type(all_secrets))
    # display_secrets_in_table()
except ApiException as e:
    print("Failed to list secrets: %s\n" % e)
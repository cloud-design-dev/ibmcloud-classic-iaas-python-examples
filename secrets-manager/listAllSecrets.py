
import os
from ibm_secrets_manager_sdk.secrets_manager_v2 import *
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from rich import box
from rich.console import Console
from rich.table import Table
from utils import SMClient
import logging
from dotenv import load_dotenv

load_dotenv()

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

ibm_client = SMClient(ibmcloud_api_key)
secrets_manager_service = ibm_client.create_secrets_manager_service()

def setup_logging(default_path='logging.json', default_level=logging.info, env_key='LOG_CFG'):
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

def get_secret_groups():
    try:
        get_secret_groups = secrets_manager_service.list_secret_groups().get_result()['secret_groups']
        return get_secret_groups
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit()

def get_all_secrets():
    try:
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
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit()

def get_secret_group(secret_group_id):
    try:
        get_group = secrets_manager_service.get_secret_group(
            id=secret_group_id
        ).get_result()
        return get_group
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit()


def display_secrets_in_table():
    all_secrets = get_all_secrets()
    sorted_all_secrets = sorted(all_secrets, key=lambda secret: secret['secret_group_id'])
    table = Table(show_header=True, header_style="bold blue", box=box.HEAVY_HEAD, title="All Secrets in Secrets Manager Instance")
    table.add_column("Secret Name")
    table.add_column("Secret Type")
    table.add_column("Secret ID")
    table.add_column("Downloaded (T/F)")
    table.add_column("Secret Group Name")
    table.add_column("Labels")
    console = Console()
    for secret in all_secrets:
        secret_name = secret['name']
        secret_type = secret['secret_type']
        secret_group_id = secret['secret_group_id']
        secret_grp = get_secret_group(secret_group_id)
        group_name = secret_grp['name']
        secret_id = secret['id']
        labels = ", ".join(secret['labels']) 
        downloaded = str(secret['downloaded'])

        table.add_row(secret_name, secret_type, secret_id, downloaded, group_name, labels)
    
    console.print(table)

    # print(json.dumps(sorted_all_secrets, indent=2))


    # console = Console()
    # for secret in all_secrets:
    #     table.add_row([secret['name'], secret['secret_type'], secret['secret_group_id'], secret['downloaded']])
    # console.print(table)

# Get all secrets

try:
    # all_secrets = get_all_secrets()
    # print(all_secrets)
    # print(type(all_secrets))
    display_secrets_in_table()
except ApiException as e:
    print("Failed to list secrets: %s\n" % e)
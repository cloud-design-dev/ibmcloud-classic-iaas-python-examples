
import os
from ibm_secrets_manager_sdk.secrets_manager_v2 import *
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import click
import json
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

def get_secret(secret_type, secret_name, secret_group_name):
    try:
        get_secret = secrets_manager_service.get_secret_by_name_type(
            secret_type=secret_type,
            name=secret_name,
            secret_group_name=secret_group_name
        ).get_result()
        return get_secret
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit()

@click.command()
@click.option('--secret_type', '-t', help='Type of secret to retrieve', required=True)
@click.option('--secret_name', '-n', help='Name of secret to retrieve', required=True)
@click.option('--secret_group_name', '-g', help='Name of secret group to retrieve secret from', required=True)
def main(secret_type, secret_name, secret_group_name):
    try:
        secret = get_secret(secret_type, secret_name, secret_group_name)
        print(secret)
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit()
        
if __name__ == '__main__':
    main()

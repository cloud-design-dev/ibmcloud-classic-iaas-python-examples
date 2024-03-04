import os
import json
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import click
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

def get_id_by_name(secret_group_name):
    try:
        secret_groups = get_secret_groups()
        for group in secret_groups:
            if group['name'] == secret_group_name:
                return group['id']
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


def createIamSecret(secret_group_id, name, service_id):
    try:
        secret_prototype_model = {
            'custom_metadata': {'mycooltestkey': 'mycooltestvalue'},
            'description': 'Testing Iam Service cred to see what labels it adds.',
            'name': name,
            'secret_group_id': secret_group_id,
            'secret_type': 'iam_credentials',
            'ttl': '7d',
            'service_id': service_id,
            'reuse_api_key': True
        }

        response = secrets_manager_service.create_secret(
            secret_prototype=secret_prototype_model,
        )
        secret = response.get_result()

        print(json.dumps(secret, indent=2))
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit()

@click.command()
@click.option('--secret_group_name', prompt='Enter the Secret Group name for new IAM secret', help='The secret group name')
@click.option('--secret_name', prompt='Enter the name for the new IAM secret', help='The secret name')
@click.option('--service_id', prompt='Enter the service id for the new IAM secret', help='The service id')
def main(group_name, name, service_id):
    secret_group_id = get_id_by_name(group_name)
    createIamSecret(secret_group_id, name, service_id)

# Need to add logic here that if the service-id passed  in does not beghin with 'ServiceId-' then we need to do an iam lookup to translate from service ID name to the actual ID.

if __name__ == "__main__":
    main()
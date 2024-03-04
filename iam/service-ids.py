import os
import json
import click
from pprint import pprint
from ibm_platform_services import IamIdentityV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from datetime import datetime, timedelta

account_id = os.environ.get('IBMCLOUD_ACCOUNT_ID')
if not account_id:
    raise ValueError("IBMCLOUD_ACCOUNT_ID environment variable not found")
ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

def ibm_client():  
  authenticator = IAMAuthenticator(apikey=ibmcloud_api_key)
  iamIdentityService = IamIdentityV1(authenticator=authenticator)
  return iamIdentityService

def getAccountId():
    try:
        client = ibm_client()
        api_key = client.get_api_keys_details(
          iam_api_key=ibmcloud_api_key
        ).get_result()
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit(1)
    account_id = api_key["account_id"]
    return account_id

@click.group()
def cli():
    """Group to hold our commands"""
    pass

@cli.command()
@click.option('--name', '-n', help='Name of the service ID to create', required=True)
@click.option('--description', '-d', help='Description of the service ID to create', required=True)
def create_service_id(name, description):
  client = ibm_client()
  account_id = getAccountId()
  apiKeyModel = {}
  apiKeyModel['name'] = "python-example-svc-id-api-key"
  apiKeyModel['description'] = "Seeing if this generates an API key for the service ID"
  apiKey = apiKeyModel
  newServiceId = client.create_service_id(
    account_id=account_id,
    name=name,
    apikey=apiKey,
    description=description
  ).get_result()

  print(newServiceId)
  srvcId = newServiceId['id']
  return srvcId

@cli.command()
@click.option('--prefix', default=None, help='Prefix to filter service IDs.')
def list_service_ids(prefix):
    client = ibm_client()
    account_id = getAccountId()
    serviceIds = client.list_service_ids(
        account_id=account_id,
        sort="modified_at",
        pagesize=100
    ).get_result().get("serviceids")

    print("Listing Service IDs on the account:\n-----")

    # Using filter with lambda
    if prefix:
        filtered_serviceIds = list(filter(lambda x: x['name'].startswith(prefix), serviceIds))
        for serviceId in filtered_serviceIds:
            print(f"Name: {serviceId['name']}\tID: {serviceId['id']}\n")
    else:
        for serviceId in serviceIds:
            print(f"Name: {serviceId['name']}\tID: {serviceId['id']}\n")

@cli.command()
@click.option('--service-id', '-s', help='ID of the service ID to delete', required=True)
def get_service_id(service_id):
  client = ibm_client()
  
  
  serviceId = client.get_service_id(
    id=service_id,
    include_activity=True,
    include_history=True
  ).get_result()

  print(serviceId)



## TODO: Adjust command to pull authentication count on service ID. Need to add function to delete all service IDs with 0 authentications in the last 6 months.
@cli.command()
def get_auth_count():
  client = ibm_client()

  account_id = getAccountId()
  serviceIds = client.list_service_ids(
        account_id=account_id,
        sort="modified_at",
        pagesize=100
  ).get_result().get("serviceids")

  for id in serviceIds:
    service_id = id['id']
    svcid = client.get_service_id(
      id=service_id,
      include_activity=True,
      include_history=True
    ).get_result()

    print(svcid)
    authentications = svcid['activity']['authn_count']
    print(authentications)

if __name__ == '__main__':
    cli()

import os
import json
from pprint import pprint
from ibm_platform_services import IamIdentityV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from datetime import datetime, timedelta

## Used in the construction of many of the IBM Cloud API endpoints, which can be versioned.
## Requests to these APIs require a major version as the first segment of the request path (ex. /v1/) 
## and a date-based version as a query parameter in the format version=YYYY-MM-DD
## For safety I set this to one day behind the current date 
today = datetime.now()
date = today + timedelta(days = -1)
version_date = date.strftime("%Y-%m-%d")

account_id = os.environ.get('ACCOUNT_ID')

## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))

iamIdentityService = IamIdentityV1(authenticator=authenticator)

def create_service_id(iamIdentityService):

  apiKeyModel = {}
  apiKeyModel['name'] = "python-example-svc-id-api-key"
  apiKeyModel['description'] = "Seeing if this generates an API key for the service ID"
  apiKey = apiKeyModel
  newServiceId = iamIdentityService.create_service_id(
    account_id=account_id,
    name='python-example-svc-id',
    apikey=apiKey,
    description='Example ServiceId created using the Python SDK'
  ).get_result()

  print(newServiceId)
  srvcId = newServiceId['id']
  return srvcId



def list_service_ids(iamIdentityService):

  serviceIds = iamIdentityService.list_service_ids(
    account_id=account_id
  ).get_result().get("serviceids")

  print("Listing Service IDs on the account:\n-----")

  for serviceId in serviceIds:
    print("Name: " + serviceId['name'] + "\tID: " + serviceId['id'] + "\n") 

def get_service_id(iamIdentityService):

  srvcId = ""
  serviceId = iamIdentityService.get_service_id(
    id=id
  )

  serviceIdDetails = serviceId.get_result()
  serviceIdEtag = serviceId.get_headers()['Etag']
  print("Srvc ID: " + serviceIdDetails['id'] + " has Etag: " + serviceIdEtag)


try:
  list_service_ids(iamIdentityService)
  create_service_id(iamIdentityService)
  get_service_id(iamIdentityService)
except ApiException as ae:
  print("Method failed")
  print(" - status code: " + str(ae.code))
  print(" - error message: " + ae.message)
  if ("reason" in ae.http_response.json()):
    print(" - reason: " + ae.http_response.json()["reason"])
 
  # + (api_key_list(iamIdentityService,iamId=serviceId['id'])))


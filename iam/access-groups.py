import os
import json
from ibm_platform_services import IamAccessGroupsV2
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

## Pull Account ID from Environment variable
account_id = os.environ.get('ACCOUNT_ID')

# Set access group used in the get_access_group function
access_group_id = 'AccessGroupId-00f95bd8-1471-440b-be1d-52af2b994676'


## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))
accessGroupService = IamAccessGroupsV2(authenticator=authenticator)

def list_access_groups(accessGroupService):
    groupsList = accessGroupService.list_access_groups(
        account_id=account_id,
        limit=100
    ).get_result().get("groups")

    for group in groupsList:
        print(json.dumps(group, indent=2))
        
def get_access_group(accessGroupService, access_group_id):
    accessGroup = accessGroupService.get_access_group(
        access_group_id
    ).get_result()

    ag = accessGroup
    print(json.dumps(ag, indent=2))
  
def create_access_group(accessGroupService):
    print("Creating new access group:")
    acessGroup = accessGroupService.create_access_group(
        name='cool-project-access-group',
        account_id=account_id,
        description='Example Access Group created using the Python SDK for our cool new project'
    ).get_result()

    newAccessGroup = acessGroup
    print(json.dumps(newAccessGroup, indent=2))

try:
  #list_access_groups(accessGroupService)
  get_access_group(accessGroupService, access_group_id=access_group_id)
  #create_access_group(accessGroupService)
except ApiException as ae:
  print("Method failed")
  print(" - status code: " + str(ae.code))
  print(" - error message: " + ae.message)
  if ("reason" in ae.http_response.json()):
    print(" - reason: " + ae.http_response.json()["reason"])
 







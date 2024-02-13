import os
import sys
import json 
from pprint import pprint
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Set up IAM authenticator
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))

# Set up Schematics service client and endpoint 
schematics_service = SchematicsV1(authenticator=authenticator)
schematics_service.set_service_url('https://us.schematics.cloud.ibm.com')

# Fetch the workspace ID and refresh token from environment variables
WORKSPACE_ID = os.environ.get('WORKSPACE_ID')

workspace_activities = schematics_service.list_workspace_activities(
    w_id=WORKSPACE_ID
).get_result()

for activity in workspace_activities.get('actions'):
    print(activity['action_id'], "\t",  activity['status'])
import os
import json
from pprint import pprint
from ibm_schematics.schematics_v1 import SchematicsV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))

schematicsService = SchematicsV1(authenticator=authenticator)

schematicsService.set_service_url(os.environ.get('IBM_SCHEMATICS_URL'))

workspace_id = ""

list_template_resources = schematicsService.get_workspace_resources(
    w_id=workspace_id
).get_result()

allResources = list_template_resources[0]['resources']

# for resource in allResources:
#     print("Resource Type: " + resource['resource_type'] + " ID: " + resource['resource_id'] + " Name: " + resource['resource_extension']['resource_name'])




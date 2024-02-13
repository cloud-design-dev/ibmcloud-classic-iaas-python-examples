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

workspace_id = ''

workspaceOutputs = schematicsService.get_workspace_outputs(
    w_id=workspace_id
).get_result()

#print(json.dumps(workspaceOutputs, indent=2))

print("Outputs for Schematics Workspace ID: " + workspace_id)

for wsOutput in workspaceOutputs[0]['output_values']:
    print(json.dumps(wsOutput, indent=2))


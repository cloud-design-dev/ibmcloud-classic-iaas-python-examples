import os
import json
from pprint import pprint
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibm_container_registry.container_registry_v1 import *
from datetime import datetime

## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))

containerRegistryService = ContainerRegistryV1(
    authenticator=authenticator,
    account=(os.environ.get('ACCOUNT_ID')),
    )

def get_container_images(containerRegistryService):

    getContainerImages = containerRegistryService.list_images().get_result()
    print(getContainerImages)


def get_container_namespaces(containerRegistryService):
    getContainerNamespaces = containerRegistryService.list_namespaces().get_result()

    print(json.dumps(getContainerNamespaces, indent=2))

try:
  get_container_images(containerRegistryService)
  get_container_namespaces(containerRegistryService)
except ApiException as ae:
  print("Method failed")
  print(" - status code: " + str(ae.code))
  print(" - error message: " + ae.message)
  if ("reason" in ae.http_response.json()):
    print(" - reason: " + ae.http_response.json()["reason"])
 



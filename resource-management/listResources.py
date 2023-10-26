import os
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_platform_services.resource_controller_v2 import *
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich import box

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

account_id = os.environ.get('IBMCLOUD_ACCOUNT_ID')
if not account_id:
    raise ValueError("IBMCLOUD_ACCOUNT_ID environment variable not found")

resource_group_id = 'ac83304b2fb6492e95995812da85b653'

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

service = ResourceControllerV2(authenticator=authenticator)

all_results = []
pager = ResourceInstancesPager(
  client=service,
  resource_group_id=resource_group_id,
)
while pager.has_next():
  next_page = pager.get_next()
  assert next_page is not None
  all_results.extend(next_page)

# print(json.dumps(all_results, indent=2))

resource_instances = []
for result in all_results:
    resource_instances.append({
        'name': result.get('name'),
        'state': result.get('state'),
        'region': result.get('region_id')
    })

print(json.dumps(resource_instances, indent=2))
# for result in all_results:
#     print(f"name: {result.name}")



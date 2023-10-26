import os
import json
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_platform_services import GlobalSearchV2
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

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

service = GlobalSearchV2(authenticator=authenticator)

response = service.search(
    query='family:is',
    fields=['name', 'type'],
    limit=100)

scan_result = response.get_result()

print(json.dumps(scan_result, indent=2))
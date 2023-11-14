import os
import json 

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_container_registry.container_registry_v1 import *
from rich import box
from rich.console import Console
from rich.table import Table

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

ibmcloud_account = os.environ.get('IBMCLOUD_ACCOUNT_ID')
if not ibmcloud_account:
    raise ValueError("IBMCLOUD_ACCOUNT_ID environment variable not found")

def registry_client():

    authenticator=IAMAuthenticator(
        apikey=ibmcloud_api_key
    )

    client = ContainerRegistryV1(
        account=ibmcloud_account,
        authenticator=authenticator
    )

    return client


def list_namespaces(endpoint):
    client = registry_client()
    client.set_service_url(f"https://{endpoint}")
    list_namespaces = client.list_namespaces().get_result()
    # list_namespaces = response('namespaces', [])  
    # return [ns['name'] for ns in list_namespaces]
    return list_namespaces
    
cr_endpoints = [
    "icr.io",
    "jp.icr.io", 
    "au.icr.io", 
    "br.icr.io", 
    "ca.icr.io",
    "de.icr.io",
    "jp2.icr.io",
    "uk.icr.io",
    "us.icr.io"
]

console = Console()

table = Table(show_header=True, header_style="bold magenta")
table.add_column("Image Names", style="dim", width=20)

for endpoint in cr_endpoints:
    table.add_column(endpoint, justify="center")

for endpoint in cr_endpoints:
    regional_namespaces = list_namespaces(endpoint)
    if not regional_namespaces:
        table.add_row(f"No namespaces in {endpoint}")
    else:
        for ns in regional_namespaces:
            table.add_row(ns, *[endpoint == cr_endpoint for cr_endpoint in cr_endpoints])

console.print(table)

# import os
# from ibm_cloud_sdk_core import ApiException  
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# from ibm_container_registry.container_registry_v1 import ContainerRegistryV1

# from rich.console import Console
# from rich.table import Table

# def list_namespaces(endpoint):

#   client = ContainerRegistryV1(...)  

#   namespaces = client.list_namespace_details().get_result()

#   return [ns['name'] for ns in namespaces]

# def print_namespaces(endpoints, namespaces):
  
#   console = Console()

#   table = Table()
#   table.add_column("Namespaces")

#   for endpoint, namespaces in zip(endpoints, namespaces):

#     if namespaces:
#       table.add_row(", ".join(namespaces)) 
#     else:
#       table.add_row("[red]No Namespaces[/red]")

#   console.print(table)


# endpoints = ["us.icr.io", "jp.icr.io"...] 

# namespaces = []

# for endpoint in endpoints:

#   ns = list_namespaces(endpoint)
#   namespaces.append(ns)

# print_namespaces(endpoints, namespaces)


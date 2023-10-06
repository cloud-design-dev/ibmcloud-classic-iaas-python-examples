import argparse
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

status_colors = {
  'OK': '[green]',
  'FAIL': '[red]',
  'INCOMPLETE': '[yellow]'
}

authenticator=IAMAuthenticator(
    apikey=ibmcloud_api_key
  )

def list_images(region):

    client = ContainerRegistryV1(
        account=ibmcloud_account,
        authenticator=authenticator
    )

    client.set_service_url(f"https://{region}.icr.io")
    response = client.list_images(
        include_ibm=False,
        include_private=True
    ).get_result()
    regional_images = response
    all_images = []
    for image in regional_images:
        name = image['RepoTags'][0]
        all_images.append(image)      
    return all_images

def print_images(images):
  sorted_images = sorted(images, key=lambda i: i['RepoTags'][0].split('/')[1])

  tag_colors = {
    0: '[green]',
    1: '[green]',
    2: '[green]',
    3: '[green]',
    4: '[red]'
  }

  console = Console()
  table = Table(show_header=True, header_style="white", box=box.ROUNDED)
  table.add_column("Namespace")
  table.add_column("Image")
  table.add_column("Tag Count")

  for image in sorted_images:

    name = image['RepoTags'][0]
    tmp_name = name.split('/')
    namespace = tmp_name[1]
    image_name = tmp_name[-1]
    tag_count = len(image['RepoTags'])
    tag_color = tag_colors.get(tag_count, '')
    colored_tags = f"{tag_color}{tag_count}[/]"

    table.add_row(
      namespace, 
      image_name,
      str(colored_tags)
    )

  console.print(table)

try:
    parser = argparse.ArgumentParser(description='List all images in a region.')
    parser.add_argument('--region', type=str, required=True, help='The region to target for listing images.')
    args = parser.parse_args()
    all_images = list_images(args.region)
    print_images(images=all_images)
except ApiException as e:
    print(f'Failed to list images in {args.region}:\n{e.message}')

import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_cloud_sdk_core import GlobalTaggingV1
from rich.console import Console
from rich.table import Table
from rich import box

def main():
    """
    This function lists all the attached tags for the specified providers and tag type.
    It uses the IBM Cloud Python SDK to authenticate and call the Global Tagging API.
    It then prints the results in a table using the Rich library.
    """
    console = Console()

    table = Table(show_header=True, header_style="white", box=box.ROUNDED)
    table.add_column("Tag Name")
    table.add_column("Provider")
    table.add_column("Resources", justify="right")

    ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
    if not ibmcloud_api_key:
        raise ValueError("IBMCLOUD_API_KEY environment variable not found")

    authenticator = IAMAuthenticator(
        apikey=ibmcloud_api_key
    )

    service = GlobalTaggingV1(authenticator=authenticator)

    try:
        tag_list = service.list_tags(
          tag_type='user',
          attached_only=True,
          full_data=True,
          providers=['ghost,ims'],
          order_by_name='asc').get_result()
        
        for tag in tag_list['items']:
        
          providers = ", ".join(sorted(tag.get('providers', [])))
          
          count = 0
          if 'attached_to_resources' in tag:
            count = tag['attached_to_resources']['ghost']
          else:
            count = "N/A"
        
          table.add_row(
            tag['name'],
            providers,
            str(count)
          )
        
        console.print(table)
    except ApiException as e:
        print("Exception when calling GlobalTaggingV1: %s\n" % e)

if __name__ == "__main__":
    main()

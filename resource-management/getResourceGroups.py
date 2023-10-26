import os
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core.api_exception import ApiException
from ibm_platform_services import ResourceManagerV2
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

service = ResourceManagerV2(authenticator=authenticator)


def main():
    console = Console()

    table = Table(show_header=True, header_style="white", box=box.ROUNDED)
    table.add_column("Resource Group Name")
    table.add_column("State")
    table.add_column("ID")
    table.add_column("Created")

    try:
        resource_group_list = service.list_resource_groups(
            account_id=account_id,
            include_deleted=True,
        ).get_result()


        for resource_group in resource_group_list['resources']:
            state_text = Text(resource_group['state']) 
            
            if resource_group['state'] == 'DELETED':
                state_text.stylize('red')
            elif resource_group['state'] == 'ACTIVE':
                state_text.stylize('green')

            table.add_row(
                resource_group['name'],
                state_text,
                resource_group['id'],
                resource_group['created_at']
            )

        console.print(table)
    except ApiException as e:
        print("Exception when calling ResourceManagerV2: %s\n" % e)


if __name__ == "__main__":
    main()
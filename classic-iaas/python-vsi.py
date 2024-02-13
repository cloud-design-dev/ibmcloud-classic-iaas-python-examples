import SoftLayer
from prettytable import PrettyTable
import click
from datetime import datetime
from rich.console import Console
from rich.table import Column, Table

# Other imports 



class VSIExample():
    def __init__(self):
        client = SoftLayer.Client()
        self.account_service = client['Account']

    def get_vsi_list(self, dc=None):
        object_filter = None
        vsi_list = None

        # Use filters if datacenter is set
        if dc:
            object_filter = {
                'virtualGuests': {
                    'datacenter': {
                        'name': {'operation': dc}
                            }
                    }
            }

        try:
            vsi_list = self.account_service.getVirtualGuests(filter=object_filter)
        except SoftLayer.SoftLayerAPIError as e:            
            print("Unable to get the VSI list: %s, %s" % (e.faultCode, e.faultString))

        return vsi_list

@click.command()
@click.option('--dc', default=None, help='Datacenter to filter by')
def main(dc):
    console = Console()
    # table = PrettyTable(['ID','Name','Public IP', 'Private IP', 'Status', 'Created On'])
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Name")
    table.add_column("Public IP", justify="right")
    table.add_column("Private IP", justify="right")
    table.add_column("Status", style="green")
    table.add_column("Created On")

    guests = VSIExample()
    guests_list = guests.get_vsi_list(dc)

    # add lbaas data to the table
    for i in guests_list:
        createDate = i['createDate']
        date_object = datetime.strptime(createDate, '%Y-%m-%dT%H:%M:%S%z')
        simplified_date = date_object.strftime('%Y-%m-%d')
        status = i['status']['name']
        Public_IP = i.get('primaryIpAddress', 'N/A') 
        table.add_row(
            str(i['id']), i['hostname'], Public_IP, i['primaryBackendIpAddress'], status, simplified_date
        )

    console.print(table)

if __name__ == "__main__":
    main()
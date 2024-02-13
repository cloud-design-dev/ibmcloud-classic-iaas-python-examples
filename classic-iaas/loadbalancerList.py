import SoftLayer
from prettytable import PrettyTable
import click

class LBaasExample():
    def __init__(self):
        client = SoftLayer.Client()
        self.lbaas_service = client['Network_LBaaS_LoadBalancer']

    def get_list(self, dc=None):
        _filter = None
        lbaas_list = None

        # Use filters if datacenter is set
        if dc:
            _filter = {"datacenter":{"name":{"operation": dc}}}

        try:
            # Retrieve load balancer objects
            lbaas_list = self.lbaas_service.getAllObjects(filter=_filter)
        except SoftLayer.SoftLayerAPIError as e:            
            print("Unable to get the LBaaS list: %s, %s" % (e.faultCode, e.faultString))

        return lbaas_list



@click.command()
@click.option('--dc', default=None, help='Datacenter filter')  
@click.option('--json', is_flag=True, help='Output as JSON')
def main(dc, json):
    if json:
        data = []
    else:    
        table = PrettyTable(['ID', 'Name', 'Address',  
                             'Type', 'Location', 'Status'])

    lbaas = LBaasExample()
    lbaas_list = lbaas.get_list(dc)

    for lb in lbaas_list:
        _mask = "mask[listeners]"
        details = lbaas.lbaas_service.getObject(id=lb['id'], mask=_mask)
        isPublic = "Public" if lb['isPublic'] == 1 else "Private"
        if json:
            # Omit fields for json
            del lb['uuid'] 
            del lb['description']
            del details['listeners']
            data.append(lb)
        else:
            # Omit fields for table view
            table.add_row([lb['id'], lb['name'], lb['address'],  
                           isPublic, lb['datacenter']['longName'],
                           lb['operatingStatus']])
    
    if json:
        print(json.dumps(data, indent=4)) 
    else:
        print(table)

if __name__ == "__main__":
    main()
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

    def get_loadbalancer_listeners(self, uuid):
        _mask = "mask[listeners]"
        get_listeners = self.lbaas_service
        try:
            get_listeners = self.lbaas_service.getLoadBalancer(uuid, mask=_mask)
            listeners = get_listeners['listeners']
            return listeners
        except SoftLayer.SoftLayerAPIError as e:            
            print("Unable to retrieve LBaaS details: %s, %s" % (e.faultCode, e.faultString))


@click.command()
@click.option('--dc', default=None, help='Datacenter to filter by')
def main(dc):
    table = PrettyTable(['ID','UUID','Name', 'Address', 'Description', 
                         'Type', 'Location', 'Status', 'Listener IDs'])

    lbaas = LBaasExample()
    # remove dc=datacenter to retrieve all the load balancers in the account
    lbaas_list = lbaas.get_list(dc)
    
    lb_listener_dict = {}
    # add lbaas data to the table
    for i in lbaas_list:
        uuid = i['uuid']
        details = lbaas.get_loadbalancer_listeners(uuid)
        listeners = details['listeners']

    # Initialize an empty list to store the listener IDs for the current load balancer
        listener_ids = []

    # Iterate over the listeners and add their IDs to the list
        for listener in listeners:
            listener_ids.append(listener['id'])

    # Add the load balancer UUID and its corresponding listener IDs to the dictionary
        lb_listener_dict[uuid] = listener_ids


        isPublic = "Public" if i['isPublic'] == 1 else "Private"
        description = i.get('description', 'N/A')  # 'N/A' will be used if 'description' key does not exist
        table.add_row([i['id'], i['uuid'], i['name'], i['address'], description,
                    isPublic,i['datacenter']['longName'],i['operatingStatus'], listener_ids])

    print (table)

if __name__ == "__main__":
    main()
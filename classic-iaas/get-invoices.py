from pprint import pprint
import SoftLayer
from SoftLayer.CLI import environment
from SoftLayer.CLI import formatting

endpoint_url="https://api.softlayer.com/rest/v3.1/"
client = SoftLayer.create_client_from_env(username="DSW2779714", api_key="cfeaa09c5b55473e9a93afabf91ef6d9f7afb14337bce67670111493393fde0c")

def call(self, service, method, *args, **kwargs):
    """Make a SoftLayer API call.
    :param method: the method to call on the service
    :param \\*args: (optional) arguments for the remote call
    :param id: (optional) id for the resource
    :param mask: (optional) object mask
    :param dict filter: (optional) filter dict
    :param dict headers: (optional) optional XML-RPC headers
    :param boolean compress: (optional) Enable/Disable HTTP compression
    :param dict raw_headers: (optional) HTTP transport headers
    :param int limit: (optional) return at most this many results
    :param int offset: (optional) offset results by this many
    :param boolean iter: (optional) if True, returns a generator with the results
    :param bool verify: verify SSL cert
    :param cert: client certificate path"""

past_invoice_object_filter = {
    "invoices":{
        "createDate":{
            "operation":"betweenDate","options":[{
                "name":"startDate","value":["02/01/2024"]},
                {"name":"endDate","value":["02/13/2024"]}]}}}

get_invoices_between = client.call('Account', 'getInvoices', filter=past_invoice_object_filter)
pprint(get_invoices_between)




import os
import json
from pprint import pprint
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_networking_services import TransitGatewayApisV1
from ibm_cloud_sdk_core import ApiException, read_external_sources
from datetime import datetime, timedelta

## Used in the construction of the TGW API client which must be versioned.
## Requests to the TGA API require a major version as the first segment of the request path (/v1/) 
## and a date-based version as a query parameter in the format version=YYYY-MM-DD
## For safety I set this to one day behind the current date 
today = datetime.now()
date = today + timedelta(days = -1)
version_date = date.strftime("%Y-%m-%d")

## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))

# The ID of the TGW you want to check against
transitGatewayId = '739a69c1-766e-405d-8325-86b87047e774'

transitGatewayService = TransitGatewayApisV1(
    authenticator=authenticator,
    version=version_date
    )

transitGatewayService.set_service_url('https://transit.cloud.ibm.com/v1')


def get_all_tgws(transitGatewayService):

    all_gws = transitGatewayService.list_transit_gateways().get_result()

    pprint(all_gws)

    for gw in all_gws['transit_gateways']:
        #pprint(gw)
        print("TGW " + gw['name'] + " is located in " + gw['location'] + ". The TGW has global routing: " + str(gw['global']))

try:
  get_all_tgws(transitGatewayService)
except ApiException as ae:
  print("Method failed")
  print(" - status code: " + str(ae.code))
  print(" - error message: " + ae.message)
  if ("reason" in ae.http_response.json()):
    print(" - reason: " + ae.http_response.json()["reason"])

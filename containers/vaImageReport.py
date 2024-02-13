import os
import json
from pprint import pprint
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException
from ibm_container_registry.vulnerability_advisor_v3 import *
from datetime import datetime

## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))
imageName =  ''

account = os.environ.get('ACCOUNT_ID')
accept_language = 'en_US'

vulnerabilityAdvisorService = VulnerabilityAdvisorV3(
    authenticator=authenticator,
    account=account
    )

def get_all_scan_results(vulnerabilityAdvisorService):
  scanreport = vulnerabilityAdvisorService.account_status_query_path().get_result()
  #print(json.dumps(scanreport, indent=2))
  image_report = scanreport['images']
  for image in image_report:
       print("Image: " + image['name'] + "\nVA Status: " + image['status'] + "\nLast Scan: " + str(datetime.fromtimestamp(image['scan_time'])) + "\n")

def va_scan_report(vulnerabilityAdvisorService, imageName):
  scan_report = vulnerabilityAdvisorService.image_report_query_path(
    name=imageName
  ).get_result()

  print(json.dumps(scan_report, indent=2))

try:
  get_all_scan_results(vulnerabilityAdvisorService)
  #va_scan_report(vulnerabilityAdvisorService, imageName=imageName)
except ApiException as ae:
  print("Method failed")
  print(" - status code: " + str(ae.code))
  print(" - error message: " + ae.message)
  if ("reason" in ae.http_response.json()):
    print(" - reason: " + ae.http_response.json()["reason"])
 

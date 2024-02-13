import os
import json
import sys
from pprint import pprint
from ibm_vpc import VpcV1
from ibm_platform_services import ResourceManagerV2, GlobalSearchV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))

# Configure the Search provider service 
searchService = GlobalSearchV2(authenticator=authenticator)
searchService.set_service_url('https://api.global-search-tagging.cloud.ibm.com')
searchTag = sys.argv[1]
print(searchTag)

def getVpcInstances(searchService,searchTag=searchTag):
    tagQuery = '(region:*) AND (family:is) AND (tags:searchTag)'
    search = searchService.search(query=tagQuery,
                        fields=['*'],limit=100)
    scan_result = search.get_result()

    resources = scan_result['items']
    print("VPC Resouce:")
    for resource in resources:
        print("Resouce: " + resource['name'] + " | Type: " + resource['type'] + " | Location: " + resource['region'])

getVpcInstances(searchService)


# def getAllInstances(searchService):
#     tagQuery = '(region:*) AND (tags:"owner:ryantiffany")'
#     search = searchService.search(query=tagQuery,
#                         fields=['*'],limit=100)
#     scan_result = search.get_result()

#     resources = scan_result['items']

#     for resource in resources:
#         print("Resource Instance: " + resource['name'] + " - Type: " + resource['service_name'] + " -  Location: " + resource['region'])
#         #print(resource)

# getAllInstances(searchService)


# def getServiceInstances(searchService,searchTag=searchTag):
#     result = searchService.search(
#         query='tags:(searchTag)',
#         fields=['resource_id', 'name', 'service_name', 'tags']
#     ).get_result()
#     resources = result['items']
#     while 'search_cursor' in result.keys():
#         result = searchService.search(search_cursor=result['search_cursor']).get_result()
#         resources.extend(result['items'])
#     print("Resource count:", len(resources))

# getServiceInstances(searchService)
import os
import json
from pprint import pprint
from ibm_vpc import VpcV1
from ibm_platform_services import GlobalTaggingV1, ResourceManagerV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_cloud_sdk_core import ApiException

## Construct IAM Authentication using IBMCLOUD_API_KEY Environment variable
authenticator = IAMAuthenticator(os.environ.get('IBMCLOUD_API_KEY'))

tagService = GlobalTaggingV1(authenticator=authenticator)
tagService.set_service_url('https://tags.global-search-tagging.cloud.ibm.com')

def get_attached_tags_full(tagService):
    tag_list = tagService.list_tags(
    tag_type='user',
    attached_only=True,
    full_data=True,
    limit=250,
    providers=['ghost,ims'],
    order_by_name='asc').get_result()

    #print(tag_list)
    alltags = tag_list['items']
    for tag in alltags:
        print(tag['name'])

def get_attached_tags_short(tagService):
    tag_list = tagService.list_tags(
    tag_type='user',
    attached_only=True,
    full_data=False,
    providers=['ghost,ims'],
    limit=250,
    order_by_name='asc').get_result()

    # print(tag_list)
    alltags = tag_list['items']
    for tag in alltags:
        print(tag['name'])

short = get_attached_tags_short(tagService)
full = get_attached_tags_full(tagService)




import argparse
import json
import os

from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services import GlobalTaggingV1  

def main(resource_crn, tag_name):

    ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
    if not ibmcloud_api_key:
        raise ValueError("IBMCLOUD_API_KEY environment variable not found")

    authenticator = IAMAuthenticator(apikey=ibmcloud_api_key)

    service = GlobalTaggingV1(authenticator=authenticator)

    resource_model = {'resource_id': resource_crn}

    tag_results = service.detach_tag(
        resources=[resource_model],
        tag_names=[tag_name],
        tag_type='user').get_result()

    print(json.dumps(tag_results, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--resource_crn', required=True, help='The CRN of the resource to untag')
    parser.add_argument('-t', '--tag_name', required=True, help='The name of the tag to detach from the resource')
    args = parser.parse_args()

    main(args.resource_crn, args.tag_name)

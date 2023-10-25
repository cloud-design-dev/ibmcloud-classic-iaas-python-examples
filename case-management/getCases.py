import os
import argparse
import csv
from ibm_platform_services.case_management_v1 import *
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

## Set our API Key from the environment, If the environment variable is not found, raise an error
ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

## Setting up the authenticator for IAM to use our API key
authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

# Use call to get all cases, and then iterate through the pages to get all results
def get_cases(all_cases=False):
    case_management_service = CaseManagementV1(authenticator=authenticator)
    all_results = []

    pager = GetCasesPager(client=case_management_service, sort='updated_at', limit=20 if all_cases else None, status=None if all_cases else ['new', 'in_progress'])
    while pager.has_next():
        next_page = pager.get_next()
        assert next_page is not None
        all_results.extend(next_page)

    cases = []
    for result in all_results:
        cases.append({
            'number': result.get('number'),
            'updated_at': result.get('updated_at'),
            'severity': result.get('severity')
        })

    return cases

try:
    parser = argparse.ArgumentParser(description='Get support cases on IBM Account.')
    parser.add_argument('--all', action='store_true', help='Retrieve all tickets on the account, regardless of status. Default is to only retrieve open and in-progress tickets')
    parser.add_argument('--csv', action='store_true', help='Write output to CSV file. The file will be pre-pended with "all_" if --all is specified, otherwise it will be "open_"')
    args = parser.parse_args() 
    cases = get_cases(all_cases=args.all)
    header_mapping = {
        'number': 'Case Number',
        'updated_at': 'Last Updated',
        'severity': 'Case Severity'
    }

    # If the `--csv` flag is specified, write the results to a CSV file, otherwise print the results to the console.
    if args.csv:
        filename = 'all_cases.csv' if args.all else 'open_cases.csv'
        print(f"Writing cases to {filename} CSV file in current directory")
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = [header_mapping[key] for key in ['number', 'updated_at', 'severity']]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for case in cases:
                mapped_case = {header_mapping[key]: case[key] for key in case}
                writer.writerow(mapped_case)
    else:
        title = "All cases on the account" if args.all else "All open and in-progress cases on the account"
        print(title)
        for case in cases:
            print(f"Number: {case['number']}, Updated At: {case['updated_at']}, Severity: {case['severity']}")
except ApiException as e:
    print(f'Error: {e.code} - {e.message}')


#!/usr/bin/env python3
# Author: Ryan Tiffany
# Copyright (c) 2023
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

__author__ = 'ryantiffany'
import os
import pandas as pd
import argparse
import csv
from ibm_platform_services import IamIdentityV1, UsageReportsV4, GlobalTaggingV1, GlobalSearchV2
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_platform_services.resource_controller_v2 import *
from ibm_platform_services.case_management_v1 import *
## Set our API Key from the environment, If the environment variable is not found, raise an error
ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

## Setting up the authenticator for IAM to use our API key
authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def getAccountId(apikey):
    ##########################################################
    ## Get AccountId for this API Key
    ##########################################################

    try:
        iam_identity_service = IamIdentityV1(authenticator=authenticator)
        api_key = iam_identity_service.get_api_keys_details(
          iam_api_key=apikey
        ).get_result()
    except ApiException as e:
        logging.error("API exception {}.".format(str(e)))
        quit()

    return api_key["account_id"]



def getCases():
    all_results = []
    case_management_service = CaseManagementV1(authenticator=authenticator)
    case_management_service.enable_retries(max_retries=5, retry_interval=1.0)
    case_management_service.set_http_config({'timeout': 120})
    pager = GetCasesPager(client=case_management_service, limit=10)
    while pager.has_next():
        next_page = pager.get_next()
        assert next_page is not None
        all_results.extend(next_page)
    return all_results

def parseCases(accountId, cases):
    data =[]
    for case in cases:
        row = {
        'accountId': accountId,
        "number":  case["number"],
        "short_description": case["short_description"],
        "description": case["description"],
        "created_at": case["created_at"],
        "created_by": case["created_by"]["name"],
        "updated_at": case["updated_at"],
        "updated_by": case["updated_by"]["name"],
        "contact_type": case["contact_type"],
        "status": case["status"],
        "severity": case["severity"],
        "support_tier": case["support_tier"],
        "resolution": case["resolution"]
        }
        data.append(row.copy())

    cases_df = pd.DataFrame(data,
        columns=[
            "accountId",
            "number",
            "short_description",
            "description",
            "created_at",
            "created_by",
            "updated_at",
            "updated_by",
            "contact_type",
            "status",
            "severity",
            "support_tier",
            "resolution"])
    return cases_df

def writeCases(cases_df):
    """
    Write cases to excel
    """
    print("Creating Cases tab.")
    cases_df.to_excel(writer, "Cases")
    worksheet = writer.sheets['Cases']
    totalrows,totalcols=cases_df.shape
    worksheet.autofilter(0,0,totalrows,totalcols)
    return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Get Account Cases.")
    parser.add_argument("--output", default=os.environ.get('output', 'cases.xlsx'), help="Filename Excel input file for list of resources and tags. (including extension of .xlsx)")
    args = parser.parse_args()
    cases_df = pd.DataFrame()
    apikey = os.environ.get('IBMCLOUD_API_KEY')
    accountId = getAccountId(apikey)
    print("Getting cases for account {}.".format(accountId))
    cases = getCases()
    print("Parsing cases for account {}.".format(accountId))
    cases_df = pd.concat([cases_df, parseCases(accountId, cases)])
    output = args.output
    split_tup = os.path.splitext(args.output)
    """ remove file extension """
    file_name = split_tup[0]
    writer = pd.ExcelWriter(file_name + ".xlsx", engine='xlsxwriter')
    workbook = writer.book
    writeCases(cases_df)
    writer.close()

    print("Getting Cases Complete.")
















# # Use call to get all cases, and then iterate through the pages to get all results
# def get_cases():
#     case_management_service = CaseManagementV1(authenticator=authenticator)
#     all_results = []
#     pager = GetCasesPager(client=case_management_service)
#     while pager.has_next():
#         next_page = pager.get_next()
#         assert next_page is not None
#         all_results.extend(next_page)

#     # print(json.dumps(all_results, indent=2))
#     return all_results

# try:
#     cases = get_cases()

#     # Extract all unique statuses 
#     statuses = set([c['status'].replace(' ', '_') for c in cases])

#     # Create dict to store cases
#     cases_by_status = {status: [] for status in statuses}

#     # Populate dict
#     for case in cases:
#         status = case['status'].replace(' ', '_')  
#         cases_by_status[status].append(case)

#     # Now cases_by_status is populated

#     cases_dfs = {}
#     for status, cases in cases_by_status.items():
#         df = pd.DataFrame(cases)
#         cases_dfs[status] = df

#     # Write excel sheets 
#     with pd.ExcelWriter('cases.xlsx') as writer:
#         for status, df in cases_dfs.items():
#             df.to_excel(writer, sheet_name=status)
        
#         writer.close() 


#     # ticket_status_options = ['New', 'InProgress', 'Waiting_on_Client', 'Resolution_Provided', 'Resolved', 'Closed']
#     # # Create a dictionary to store the cases for each ticket status
#     # cases_by_status = {status: [] for status in ticket_status_options}

#     # # Iterate through the cases and group them by ticket status
#     # for case in cases:
#     #     status = case['status'].replace(' ', '_')
#     #     cases_by_status[status].append(case)

#     # # Write each ticket status as a separate sheet in the CSV file
#     # with open('cases_by_status.csv', 'w', newline='') as csvfile:
#     #     writer = csv.writer(csvfile)
#     #     for status, cases in cases_by_status.items():
#     #         # Write the ticket status as the sheet name
#     #         writer.writerow([status])

#     #         # Write the case details as rows in the sheet
#     #         writer.writerow(['Case Number', 'Last Updated', 'Case Severity', 'Short Description'])
#     #         for case in cases:
#     #             writer.writerow([case['number'], case['updated_at'], case['severity'], case['short_description']])

# except ApiException as e:
#     print(f'Error: {e.code} - {e.message}')

# # try:
# #     parser = argparse.ArgumentParser(description='Get support cases on IBM Account.')

# #     args = parser.parse_args() 
# #     cases = get_cases(all_cases=args.all)
# #     header_mapping = {
# #         'number': 'Case Number',
# #         'updated_at': 'Last Updated',
# #         'severity': 'Case Severity',
# #         'short_description': 'Short Description'
# #     }

# #     # If the `--csv` flag is specified, write the results to a CSV file, otherwise print the results to the console.
# #     if args.csv:
# #         filename = 'all_cases.csv' if args.all else 'open_cases.csv'
# #         print(f"Writing cases to {filename} CSV file in current directory")
# #         with open(filename, 'w', newline='') as csvfile:
# #             fieldnames = [header_mapping[key] for key in ['number', 'updated_at', 'severity', 'short_description']]
# #             writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
# #             writer.writeheader()
# #             for case in cases:
# #                 mapped_case = {header_mapping[key]: case[key] for key in case}
# #                 writer.writerow(mapped_case)
# #     else:
# #         title = "All cases on the account" if args.all else "All open and in-progress cases on the account"
# #         print(title)
# #         for case in cases:
# #             print(f"Number: {case['number']}, Updated At: {case['updated_at']}, Severity: {case['severity']}")
# # except ApiException as e:
# #     print(f'Error: {e.code} - {e.message}')
import argparse
import os

import ibm_vpc
from ibm_cloud_sdk_core import ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from rich import box
from rich.console import Console
from rich.table import Table
from rich.tree import Tree

ibmcloud_api_key = os.environ.get('IBMCLOUD_API_KEY')
if not ibmcloud_api_key:
    raise ValueError("IBMCLOUD_API_KEY environment variable not found")

authenticator = IAMAuthenticator(
    apikey=ibmcloud_api_key
)

def get_vpcs(region):
    service = ibm_vpc.VpcV1(authenticator=authenticator)
    service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')

    list_vpcs = service.list_vpcs().get_result()['vpcs']
    vpcs = []
    for vpc in list_vpcs:
        vpc_info = {'name': vpc['name'], 'id': vpc['id']}
        # list_subnets = service.list_subnets().get_result()['subnets']
        # subnets_in_vpc = [subnet for subnet in list_subnets if subnet['vpc']['id'] == vpc['id']]
        # public_subnets = sum(1 for subnet in subnets_in_vpc if subnet.get('public_gateway'))
        # private_subnets = len(subnets_in_vpc) - public_subnets
        # vpc_info['public_subnets'] = public_subnets
        # vpc_info['private_subnets'] = private_subnets
        list_subnets = service.list_subnets().get_result()['subnets']
        subnets_in_vpc = [subnet for subnet in list_subnets if subnet['vpc']['id'] == vpc['id']]
        vpc_info['subnets'] = [{'name': subnet['name'], 'has_public_gateway': bool(subnet.get('public_gateway'))} for subnet in subnets_in_vpc]


        list_instances = service.list_instances().get_result()['instances']
        instances_in_vpc = [instance for instance in list_instances if instance['vpc']['id'] == vpc['id']]
        total_instances = len(instances_in_vpc)
        running_instances = len([instance for instance in instances_in_vpc if instance['status'] == 'running'])
        stopped_instances = total_instances - running_instances
        vpc_info['total_instances'] = total_instances
        vpc_info['running_instances'] = running_instances
        vpc_info['stopped_instances'] = stopped_instances

        # Add placeholders for ALBs and NLBs as they are not calculated yet
        vpc_info['albs'] = 0
        vpc_info['nlbs'] = 0

        vpcs.append(vpc_info)

    return vpcs

# def get_vpcs(region):
#     service = ibm_vpc.VpcV1(authenticator=authenticator)
#     service.set_service_url(f'https://{region}.iaas.cloud.ibm.com/v1')

#     list_vpcs = service.list_vpcs().get_result()['vpcs']
#     vpcs = []
#     for vpc in list_vpcs:
#         vpc_info = {'name': vpc['name'], 'id': vpc['id']}
#         list_subnets = service.list_subnets().get_result()['subnets']
#         subnets_in_vpc = [subnet for subnet in list_subnets if subnet['vpc']['id'] == vpc['id']]
#         public_subnets = sum(1 for subnet in subnets_in_vpc if subnet.get('public_gateway'))
#         private_subnets = len(subnets_in_vpc) - public_subnets
#         vpc_info['subnets'] = f"[green]{public_subnets}[/green] / [white]{private_subnets}[/white]"

#         list_instances = service.list_instances().get_result()['instances']
#         instances_in_vpc = [instance for instance in list_instances if instance['vpc']['id'] == vpc['id']]
#         total_instances = len(instances_in_vpc)
#         running_instances = len([instance for instance in instances_in_vpc if instance['status'] == 'running'])
#         stopped_instances = total_instances - running_instances
#         vpc_info['instances'] = f"[yellow]{total_instances}[/yellow] / [green]{running_instances}[/green] / [red]{stopped_instances}[/red]"

#         vpcs.append(vpc_info)

#     return vpcs

def display_vpcs(vpcs):
    console = Console()

    for vpc in vpcs:
        tree = Tree(f"{vpc['name']}", guide_style="bold bright_blue")

        instances_node = tree.add("Instances")
        instances_node.add(f"{vpc['total_instances']} Total")
        instances_node.add(f"[green]{vpc['running_instances']} Running[/green]")
        instances_node.add(f"[red]{vpc['stopped_instances']} Stopped[/red]")
        

        load_balancers_node = tree.add("Load-Balancers")
        load_balancers_node.add(f"{vpc['albs']} ALBs")
        load_balancers_node.add(f"{vpc['nlbs']} NLBs")

        subnets_node = tree.add("Subnets")
        for subnet in vpc['subnets']:
            color = "green" if subnet['has_public_gateway'] else "red"
            subnets_node.add(f"[{color}]{subnet['name']}[/{color}]")

        console.print(tree)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='List all VPCs in a region.')
    parser.add_argument('--region', type=str, required=True, help='The region to list VPCs from.')
    args = parser.parse_args()
    vpcs = get_vpcs(args.region)
  
    display_vpcs(vpcs)

# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='List all VPCs in a region.')
#     parser.add_argument('--region', type=str, required=True, help='The region to list VPCs from.')
#     args = parser.parse_args()

#     vpcs = get_vpcs(args.region)
#     print_vpcs(vpcs)

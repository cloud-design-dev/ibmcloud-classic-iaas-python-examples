import argparse
import json
import socket
import threading

import SoftLayer
from rich import box
from rich import print
from rich.console import Console
from rich.table import Table

linux_table = Table(show_header=True, header_style="blue", box=box.ROUNDED) 

linux_table.add_column("Server ID")
linux_table.add_column("Public IP")
linux_table.add_column("Open Port")
linux_table.add_column("Provision Date")
linux_table.add_column("Provisioned By")

def scan_hosts(hosts, port):
  # split hosts into batches
  threads = []
  
  for batch in hosts:
    for vm in batch:
      ip = vm['public_ip']
      id = vm['server_id']
      thread = threading.Thread(target=check_port, args=(ip, port))
      threads.append(thread)
      thread.start()

  for thread in threads:
    thread.join()
    

def check_port(ip, port):

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  result = sock.connect_ex((ip, port))
  
  if result == 0:
    return port

  return None
  sock.close()


# Create SoftLayer client object
client = SoftLayer.create_client_from_env()

def get_public_vms():

  vms = client['Account'].getVirtualGuests()
  filtered_vms = [s for s in vms if s.get('primaryIpAddress')]
  return filtered_vms

def filter_hosts(filtered_vms, os_type):
  if os_type == 'windows':
    return [h for h in filtered_vms if h['os'].startswith('WIN')]
  elif os_type == 'linux':  
    return [h for h in filtered_vms if not h['os'].startswith('WIN')]

def main():

  parser = argparse.ArgumentParser()
  parser.add_argument('--type', choices=['rdp', 'ssh'], required=True)
  args = parser.parse_args()

  hosts = get_public_vms()

  if args.type == 'rdp':
    hosts = filter_hosts(hosts, 'windows')
    scan_hosts(hosts, 3389)
  elif args.type == 'ssh':
    hosts = filter_hosts(hosts, 'linux')
    scan_hosts(hosts, 22)

main()
# Get all virtual guests



# for vm in filtered_vms:

#   # Get VM details
#   vm_id = vm['id']
#   object_mask = "mask[id,globalIdentifier,fullyQualifiedDomainName,hostname,domain,createDate,modifyDate,provisionDate,notes,dedicatedAccountHostOnlyFlag,privateNetworkOnlyFlag,primaryBackendIpAddress,primaryIpAddress,networkComponents[id,status,speed,maxSpeed,name,macAddress,primaryIpAddress,port,primarySubnet,securityGroupBindings[securityGroup[id, name]]],lastKnownPowerState.name,powerState,status,maxCpu,maxMemory,datacenter,activeTransaction[id, transactionStatus[friendlyName,name]],lastOperatingSystemReload.id,blockDevices,blockDeviceTemplateGroup[id, name, globalIdentifier],postInstallScriptUri,operatingSystem[passwords[username,password],softwareLicense.softwareDescription[manufacturer,name,version,referenceCode]],softwareComponents[passwords[username,password,notes],softwareLicense[softwareDescription[manufacturer,name,version,referenceCode]]],hourlyBillingFlag,userData,billingItem[id,package,nextInvoiceTotalRecurringAmount,nextInvoiceChildren[description,categoryCode,recurringFee,nextInvoiceTotalRecurringAmount],children[description,categoryCode,nextInvoiceTotalRecurringAmount],orderItem[id,order.userRecord[username],preset.keyName]],tagReferences[id,tag[name,id]],networkVlans[id,vlanNumber,networkSpace],dedicatedHost.id,transientGuestFlag,lastTransaction[transactionGroup]]"
#   vm_details = client['Virtual_Guest'].getObject(
#   	id=vm_id,
# 	  mask=object_mask
# 	)
#   public_ip = vm_details.get('primaryIpAddress')
#   provision_date = vm_details.get('provisionDate')
#   os_data = vm_details.get('operatingSystem')
#   billingItem = vm_details.get('billingItem')
#   provision_user = billingItem['orderItem']['order']['userRecord']['username']
#   os_ref_code = "NOT FOUND" if os_data is None else os_data['softwareLicense']['softwareDescription']['referenceCode']
#   if os_ref_code.startswith('WIN_'):
#     win_hosts.append({
#       'server_id': vm_id,
#       'public_ip': public_ip,  
#       'provision_date': provision_date,
#       'provision_user': provision_user
#     })

#   else:
#     nix_hosts.append({
#       'server_id': vm_id,
#       'public_ip': public_ip,
#       'provision_date': provision_date,
#       'provision_user': provision_user
#     })

# def nix_host_scan():
#   threads = []
#   batch_size = 10
#   print("Checking ports on Nix hosts")
#   # Split nix_hosts into batches 
#   nix_batches = [nix_hosts[i:i+batch_size] for i in range(0, len(nix_hosts), batch_size)]

#   for batch in nix_batches:

#     threads = []

#     for vm in batch:
#         ip = vm['public_ip']
#         thread = threading.Thread(target=check_port, args=(ip, 22))
#         threads.append(thread)
#         thread.start()

#         for thread in threads:
#           thread.join()
#         id = vm['server_id']
#         user = vm['provision_user']
#         date = vm['provision_date']
    
#         if thread:
#           linux_table.add_row(str(id), str(ip), str(22), str(date), str(user))
  

#     console = Console()

#     console.print(linux_table)

# def win_host_scan():
#   batch_size = 10
#   print("Checking ports on Windows hosts")
#   # Split windows_hosts into batches 
#   win_batches = [win_hosts[i:i+batch_size] for i in range(0, len(win_hosts), batch_size)]

#   for batch in win_batches:

#     threads = []

#     for vm in batch:
#         ip = vm['public_ip']
#         open_port = check_port(ip, 3389)
#         id = vm['server_id']
#         user = vm['provision_user']
#         date = vm['provision_date']
    
#         if open_port:
#           windows_table.add_row(str(id), str(ip), str(open_port), str(date), str(user))
  
#   console = Console()
#   console.print(windows_table)

# try:
#   nix_host_scan()
#   win_host_scan()

# except:
#   print("Error: unable to start thread")

# #

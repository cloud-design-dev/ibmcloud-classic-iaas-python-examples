import json
import socket
import threading

import SoftLayer
from rich import box
from rich import print
from rich.console import Console
from rich.table import Table


windows_table = Table(show_header=True, header_style="green", box=box.ROUNDED)  
linux_table = Table(show_header=True, header_style="blue", box=box.ROUNDED) 

linux_table.add_column("Server ID")
linux_table.add_column("Public IP")
linux_table.add_column("Open Port")
linux_table.add_column("Provision Date")
linux_table.add_column("Provisioned By")

def check_port(ip, port):

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  result = sock.connect_ex((ip, port))
  
  if result == 0:
    return port

  return None
  sock.close()

win_hosts = []
nix_hosts = []
# Create SoftLayer client object
client = SoftLayer.create_client_from_env()

# Get all virtual guests
vms = client['Account'].getVirtualGuests()
filtered_vms = [s for s in vms if s.get('primaryIpAddress')]

for vm in filtered_vms:

  # Get VM details
  vm_id = vm['id']
  object_mask = "mask[id,globalIdentifier,fullyQualifiedDomainName,hostname,domain,createDate,modifyDate,provisionDate,notes,dedicatedAccountHostOnlyFlag,privateNetworkOnlyFlag,primaryBackendIpAddress,primaryIpAddress,networkComponents[id,status,speed,maxSpeed,name,macAddress,primaryIpAddress,port,primarySubnet,securityGroupBindings[securityGroup[id, name]]],lastKnownPowerState.name,powerState,status,maxCpu,maxMemory,datacenter,activeTransaction[id, transactionStatus[friendlyName,name]],lastOperatingSystemReload.id,blockDevices,blockDeviceTemplateGroup[id, name, globalIdentifier],postInstallScriptUri,operatingSystem[passwords[username,password],softwareLicense.softwareDescription[manufacturer,name,version,referenceCode]],softwareComponents[passwords[username,password,notes],softwareLicense[softwareDescription[manufacturer,name,version,referenceCode]]],hourlyBillingFlag,userData,billingItem[id,package,nextInvoiceTotalRecurringAmount,nextInvoiceChildren[description,categoryCode,recurringFee,nextInvoiceTotalRecurringAmount],children[description,categoryCode,nextInvoiceTotalRecurringAmount],orderItem[id,order.userRecord[username],preset.keyName]],tagReferences[id,tag[name,id]],networkVlans[id,vlanNumber,networkSpace],dedicatedHost.id,transientGuestFlag,lastTransaction[transactionGroup]]"
  vm_details = client['Virtual_Guest'].getObject(
  	id=vm_id,
	  mask=object_mask
	)
  public_ip = vm_details.get('primaryIpAddress')
  provision_date = vm_details.get('provisionDate')
  os_data = vm_details.get('operatingSystem')
  billingItem = vm_details.get('billingItem')
  provision_user = billingItem['orderItem']['order']['userRecord']['username']
  os_ref_code = "NOT FOUND" if os_data is None else os_data['softwareLicense']['softwareDescription']['referenceCode']
  if os_ref_code.startswith('WIN_'):
    win_hosts.append({
      'server_id': vm_id,
      'public_ip': public_ip,  
      'provision_date': provision_date,
      'provision_user': provision_user
    })

  else:
    nix_hosts.append({
      'server_id': vm_id,
      'public_ip': public_ip,
      'provision_date': provision_date,
      'provision_user': provision_user
    })

batch_size = 10
print("Checking ports on Nix hosts")
# Split nix_hosts into batches 
nix_batches = [nix_hosts[i:i+batch_size] for i in range(0, len(nix_hosts), batch_size)]

for batch in nix_batches:

  threads = []

  for vm in batch:
      ip = vm['public_ip']
      open_port = check_port(ip, 22)
      id = vm['server_id']
      user = vm['provision_user']
      date = vm['provision_date']
  
      if open_port:
        linux_table.add_row(str(id), str(ip), str(open_port), str(date), str(user))

console = Console()

console.print(linux_table)

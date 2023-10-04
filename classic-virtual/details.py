import json
import socket
import threading
from concurrent.futures import ThreadPoolExecutor

import SoftLayer
from rich import box
from rich import print as rprint
from rich.console import Console
from rich.table import Table

client = SoftLayer.create_client_from_env()

def get_vms(client):
  vms = client['Account'].getVirtualGuests()
  return [vm for vm in vms if vm.get('primaryIpAddress')]

def get_vm_details(vm):
  # Get VM details
  vm_id = vm['id']
  mask = "mask[id,globalIdentifier,fullyQualifiedDomainName,hostname,domain,createDate,modifyDate,provisionDate,notes,dedicatedAccountHostOnlyFlag,privateNetworkOnlyFlag,primaryBackendIpAddress,primaryIpAddress,networkComponents[id,status,speed,maxSpeed,name,macAddress,primaryIpAddress,port,primarySubnet,securityGroupBindings[securityGroup[id, name]]],lastKnownPowerState.name,powerState,status,maxCpu,maxMemory,datacenter,activeTransaction[id, transactionStatus[friendlyName,name]],lastOperatingSystemReload.id,blockDevices,blockDeviceTemplateGroup[id, name, globalIdentifier],postInstallScriptUri,operatingSystem[passwords[username,password],softwareLicense.softwareDescription[manufacturer,name,version,referenceCode]],softwareComponents[passwords[username,password,notes],softwareLicense[softwareDescription[manufacturer,name,version,referenceCode]]],hourlyBillingFlag,userData,billingItem[id,package,nextInvoiceTotalRecurringAmount,nextInvoiceChildren[description,categoryCode,recurringFee,nextInvoiceTotalRecurringAmount],children[description,categoryCode,nextInvoiceTotalRecurringAmount],orderItem[id,order.userRecord[username],preset.keyName]],tagReferences[id,tag[name,id]],networkVlans[id,vlanNumber,networkSpace],dedicatedHost.id,transientGuestFlag,lastTransaction[transactionGroup]]" 
  return client['Virtual_Guest'].getObject(id=vm_id, mask=mask)

def check_port(ip, port):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  result = sock.connect_ex((ip, port))
  sock.close()
  return port if result == 0 else None

def scan_hosts(hosts, port):
  results = []
  with ThreadPoolExecutor() as executor:
    futures = [executor.submit(check_port, vm['primaryIpAddress'], port) 
               for vm in hosts]
    for future in futures:
      port, vm = future.result() 
      if port:
        results.append((port, vm))
  return results
      
def main():
  
  windows_table = Table(show_header=True, header_style="white", box=box.ROUNDED)
  windows_table.add_column("Server ID")
  windows_table.add_column("Public IP")
  windows_table.add_column("Open Port")
  windows_table.add_column("Provision Date")
  windows_table.add_column("Provisioned By")

  linux_table = Table(show_header=True, header_style="blue", box=box.ROUNDED)
  linux_table.add_column("Server ID")
  linux_table.add_column("Public IP")
  linux_table.add_column("Open Port")
  linux_table.add_column("Provision Date")
  linux_table.add_column("Provisioned By")

  try:
    client = SoftLayer.create_client_from_env()
    
    vms = get_vms(client)
    
    win_vms = []
    nix_vms = []
    for vm in vms:
      details = get_vm_details(vm)
      if details['operatingSystem']['softwareLicense']['softwareDescription']['referenceCode'].startswith('WIN_'):
        win_vms.append(details)  
      else:
        nix_vms.append(details)

    rprint("Checking ports on Windows hosts")  
    win_ports = scan_hosts(win_vms, 3389)
    for port, vm in win_ports:
      windows_table.add_row(str(vm['id']), str(vm['primaryIpAddress']), 
                            str(port), str(vm['provisionDate']), 
                            str(vm['billingItem']['orderItem']['order']['userRecord']['username']))

    rprint("Checking ports on Linux hosts")
    nix_ports = scan_hosts(nix_vms, 22)
    for port in nix_ports:
      vm = port['vm']
      linux_table.add_row(str(vm['id']), str(vm['primaryIpAddress']), 
                          str(port), str(vm['provisionDate']),
                          str(vm['billingItem']['orderItem']['order']['userRecord']['username']))
    
    console = Console()
    console.print(windows_table)
    console.print(linux_table)

  except Exception as e:
    rprint(f"Error: {e}")
  
if __name__ == "__main__":
  main()

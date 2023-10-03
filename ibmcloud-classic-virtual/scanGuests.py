import SoftLayer
import json
import socket
import threading

def check_port(ip, port, id, provision_user):

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

  result = sock.connect_ex((ip, port))
  
  if result == 0:
    print(f"Server {id} has open port {port} on public ip {ip}. Provisioned by {provision_user}")
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
      'provision_user': provision_user,
      'os_ref_code': os_ref_code
    })

  else:
    nix_hosts.append({
      'server_id': vm_id,
      'public_ip': public_ip,
      'provision_date': provision_date,
      'provision_user': provision_user,
      'os_ref_code': os_ref_code
    })

batch_size = 10

print("Checking ports on Nix hosts")
# Split nix_hosts into batches 
nix_batches = [nix_hosts[i:i+batch_size] for i in range(0, len(nix_hosts), batch_size)]

for batch in nix_batches:

  threads = []

  for vm in batch:

    ip = vm['public_ip']
    id = vm['server_id']
    provision_user = vm['provision_user']

    t = threading.Thread(target=check_port, args=(ip, 22, id, provision_user)) 
    threads.append(t)
    t.start()

  # Wait for all threads to complete
  for t in threads:
    t.join()

print("Checking ports on Windows hosts")
# Split win_hosts into batches
win_batches = [win_hosts[i:i+batch_size] for i in range(0, len(win_hosts), batch_size)]



for batch in win_batches:

  threads = []

for vm in win_hosts:

  ip = vm['public_ip']
  id = vm['server_id']
  provision_user = vm['provision_user']
  provision_date = vm['provision_date']

  t = threading.Thread(target=check_port, args=(ip, 3389, id, provision_user)) 
  threads.append(t)
  t.start()

  # Wait for all threads to complete
  for t in threads:
    t.join()

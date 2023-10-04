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
bms = client['Account'].getHardware()
filtered_bms = [s for s in bms if s.get('primaryIpAddress')]

for bm in filtered_bms:

  bm_id = bm['id']
  object_mask = "mask[id,globalIdentifier,fullyQualifiedDomainName,hostname,domain,provisionDate,hardwareStatus,processorPhysicalCoreAmount,memoryCapacity,notes,privateNetworkOnlyFlag,primaryBackendIpAddress,primaryIpAddress,networkManagementIpAddress,userData,datacenter,networkComponents[id,status,speed,maxSpeed,name,ipmiMacAddress,ipmiIpAddress,macAddress,primaryIpAddress,port,primarySubnet[id,netmask,broadcastAddress,networkIdentifier,gateway]],hardwareChassis[id,name],operatingSystem[softwareLicense[softwareDescription[manufacturer,name,version,referenceCode]],passwords[username,password]],billingItem[id,nextInvoiceTotalRecurringAmount,children[nextInvoiceTotalRecurringAmount],nextInvoiceChildren[description,categoryCode,nextInvoiceTotalRecurringAmount],orderItem.order.userRecord[username]],hourlyBillingFlag,tagReferences[id,tag[name,id]],networkVlans[id,vlanNumber,networkSpace],remoteManagementAccounts[username,password],lastTransaction[transactionGroup],activeComponents]"
  bm_details = client['Hardware'].getObject(
  	id=bm_id,
	  mask=object_mask
	)
  allDetails = json.dumps(bm_details, indent=2)
#   public_ip = bm_details.get('primaryIpAddress')
#   provision_date = bm_details.get('provisionDate')
#   os_data = bm_details.get('operatingSystem')
#   billingItem = bm_details.get('billingItem')

# print(billingItem)

#   provision_user = billingItem['orderItem']['order']['userRecord']['username']
#   os_ref_code = "NOT FOUND" if os_data is None else os_data['softwareLicense']['softwareDescription']['referenceCode']
#   if os_ref_code.startswith('WIN_'):
#     win_hosts.append({
#       'server_id': bm_id,
#       'public_ip': public_ip,  
#       'provision_date': provision_date,
#       'provision_user': provision_user,
#       'os_ref_code': os_ref_code
#     })

#   else:
#     nix_hosts.append({
#       'server_id': bm_id,
#       'public_ip': public_ip,
#       'provision_date': provision_date,
#       'provision_user': provision_user,
#       'os_ref_code': os_ref_code
#     })

# batch_size = 10

# print("Checking ports on Nix hosts")
# # Split nix_hosts into batches 
# nix_batches = [nix_hosts[i:i+batch_size] for i in range(0, len(nix_hosts), batch_size)]

# for batch in nix_batches:

#   threads = []

#   for bm in batch:

#     ip = bm['public_ip']
#     id = bm['server_id']
#     provision_user = bm['provision_user']

#     t = threading.Thread(target=check_port, args=(ip, 22, id, provision_user)) 
#     threads.append(t)
#     t.start()

#   # Wait for all threads to complete
#   for t in threads:
#     t.join()

# print("Checking ports on Windows hosts")
# # Split win_hosts into batches
# win_batches = [win_hosts[i:i+batch_size] for i in range(0, len(win_hosts), batch_size)]



# for batch in win_batches:

#   threads = []

# for bm in win_hosts:

#   ip = bm['public_ip']
#   id = bm['server_id']
#   provision_user = bm['provision_user']
#   provision_date = bm['provision_date']

#   t = threading.Thread(target=check_port, args=(ip, 3389, id, provision_user)) 
#   threads.append(t)
#   t.start()

#   # Wait for all threads to complete
#   for t in threads:
#     t.join()

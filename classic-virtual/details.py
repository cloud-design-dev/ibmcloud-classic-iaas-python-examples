import json

import SoftLayer

client = SoftLayer.create_client_from_env()

vm_id = 137682113

def print_keys(d, parent_key=''):
  for k, v in d.items():
    key = parent_key + '.' + k if parent_key else k
    if isinstance(v, dict):
      print_keys(v, key)
    else:
      print(key)

vm_details = client['Virtual_Guest'].getObject(id=vm_id)

print_keys(vm_details)

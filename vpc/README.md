# Python VPC Scripts

Handy scripts for interacting with IBM Cloud VPC API


## Install dependencies

```shell
pip install -r requirements.txt
```

## Export API Key

```shell
export IBMCLOUD_API_KEY=<YOUR API KEY>
```

---

## Scripts

### List VPCs in region

Pretty simple, mainly used to test output stuff related to `rich` python module. 

```shell
python listVpcs.py --region <VPC Region>
```

![Example Output](../images/listVpcsOutput.png)

### Generate OpenVPN Config for VPN

You can use this script to generate an OpenVPN profile to connect to the CDE Client to Site VPN server. 

#### Export Script Variables

Contact Ryan if you need to get these variables:

```
export VPN_KEY_SM_NAME=<Name of Key Secret in SM>
export VPN_CERT_SM_NAME=<Name of Cert Secret in SM>
export SM_INSTANCE_NAME=<Name of SM Instance>
export IBMCLOUD_API_KEY=<Your API Key>
```

#### Run Script

```
python generateVpnConfig.py 
```

If the script runs correctly, you should now have a file called `client-full.ovpn` in the current directory. Double-click on the file to start the profile import process in OpenVPN Connect. 

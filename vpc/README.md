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

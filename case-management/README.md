# Get Support Cases on IBM Cloud Account

## Install python modules

```shell
pip install -r requirements.txt
```

## Scripts

### Retrieve support tickets for an account

The `getCases.py` script will pull the tickets on an account and optionally write them to a csv file. The script uses the `argparse` library to allow for command line options. The script will default to only retrieving open and in-progress tickets. To retrieve all tickets on the account, use the `--all` option. To write the output to a csv file, use the `--csv` option. 

```shell
❯ python getCases.py --help 
usage: getCases.py [-h] [--all] [--csv]

Get support cases on IBM Account.

options:
  -h, --help  show this help message and exit
  --all       Retrieve all tickets on the account, regardless of status. Default is to only retrieve open and in-progress tickets
  --csv       Write output to CSV file. The file will be pre-pended with "all_" if --all is specified, otherwise it will be "open_"
```
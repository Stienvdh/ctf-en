import requests
from requests.auth import HTTPBasicAuth
from env import config
import json

headers = {
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

orgs_url = f"{config['MERAKI_BASE_URL']}/organizations"
resp = requests.get(orgs_url, headers=headers)

if resp.status_code == 200:
    for org in resp.json():
        print(org["id"])
        print(org["name"])

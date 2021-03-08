import requests
from requests.auth import HTTPBasicAuth
from env import config
import json

headers = {
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

def get_org_id():
    orgs_url = f"{config['MERAKI_BASE_URL']}/organizations"
    resp = requests.get(orgs_url, headers=headers)

    if resp.status_code == 200:
        for org in resp.json():
            if org["name"] == config["stage1-org"]:
                return org["id"]
    return 0

def get_network_id(org_id):
    networks_url = f"{config['MERAKI_BASE_URL']}/organizations/{org_id}/networks"
    resp = requests.get(networks_url, headers=headers)

    if resp.status_code == 200:
        for network in resp.json():
            if network["name"] == config["stage1-network"]:
                return network["id"]
    return 0

def get_devices(network_id):
    devices_url = f"{config['MERAKI_BASE_URL']}/networks/{network_id}/devices"
    resp = requests.get(devices_url, headers=headers)

    if resp.status_code == 200:
        return resp.json()
    return {}

if __name__ == "__main__":
    ORG_ID = get_org_id()
    NET_ID = get_network_id(ORG_ID)

    inventory = []
    for device in get_devices(NET_ID):
        inv_entry = {}
        if "name" in device:
            inv_entry["name"] = device["name"]
        if "type" in device:
            inv_entry["type"] = device["type"]
        if "mac" in device:
            inv_entry["mac"] = device["mac"]
        if "serial" in device:
            inv_entry["serial"] = device["serial"]
        inventory += [inv_entry]
    
    with open("inventory.json", "w") as f:
        f.write(json.dumps(inventory, indent=2))
        f.close()
    
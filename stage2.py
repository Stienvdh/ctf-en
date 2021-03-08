import requests
from requests.auth import HTTPBasicAuth
from env import config
import json
import stage1

def get_auth_token():
    dnac_auth_url = f"{config['DNAC_BASE_URL']}/dna/system/api/v1/auth/token"

    resp = requests.post(dnac_auth_url, auth=HTTPBasicAuth(config['DNAC_USER'], config['DNAC_PASSWORD']))

    if resp.status_code == 200:
        return resp.json()["Token"]
    return 0

def get_inventory(token):
    headers = {
        "X-Auth-Token": token,
    }

    devices_url = f"{config['DNAC_BASE_URL']}/dna/intent/api/v1/network-device"
    resp = requests.get(devices_url, headers=headers)

    if resp.status_code == 200:
        inventory = []
        for device in resp.json()["response"]:
            inv_entry = {"category" : "DNA-Center"}
            if "hostname" in device:
                inv_entry["name"] = device["hostname"]
            if "family" in device:
                inv_entry["type"] = device["family"]
            if "macAddress" in device:
                inv_entry["mac"] = device["macAddress"]
            if "serialNumber" in device:
                inv_entry["serial"] = device["serialNumber"]
            inventory += [inv_entry]
        return inventory
    return 0

if __name__ == "__main__":
    AUTH_TOKEN = get_auth_token()
    INVENTORY = get_inventory(AUTH_TOKEN)

    with open("inventoryDNA.json", "w") as f:
        f.write(json.dumps(INVENTORY, indent=2))
        f.close()
    
    full_inventory = INVENTORY + stage1.get_inventory()
    with open("inventory-full.json", "w") as f:
        f.write(json.dumps(full_inventory, indent=2))
        f.close()

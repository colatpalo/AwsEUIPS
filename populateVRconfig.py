import requests
from urllib3.exceptions import InsecureRequestWarning

# Disable SSL warnings (use with caution)
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Palo Alto Firewall Details
firewall_ip = "x.x.x.x"  # Replace with your firewall's IP
username = "admin"  # Replace with your username
password = "xxxxxx"  # Replace with your password
prefix_file = "xxxx"  # Text file containing prefixes (one per line)

# API Endpoint for key generation
auth_url = f"https://{firewall_ip}/api/"
auth_params = {
    "type": "keygen",
    "user": username,
    "password": password,
}

# Get API Key
auth_response = requests.post(auth_url, params=auth_params, verify=False)

# Extract API Key from Response
if "<key>" in auth_response.text:
    api_key = auth_response.text.split("<key>")[1].split("</key>")[0]
    print(f"Generated API Key: {api_key}")
else:
    print("Failed to obtain API Key")
    exit(1)

# Base API URL for sending configurations
config_url = f"https://{firewall_ip}/api/"

# BGP Policy XPath
xpath = "/config/devices/entry[@name='localhost.localdomain']/network/virtual-router/entry[@name='default']/protocol/bgp/policy/import/rules/entry[@name='my_prefix_list']/match/address-prefix"

# Read Prefixes from File & Send Requests
try:
    with open(prefix_file, "r") as file:
        for line in file:
            prefix = line.strip()
            if prefix:
                # XML Element for each prefix
                element = f"<entry name='{prefix}'/>"

                # Request Parameters
                params = {
                    "type": "config",
                    "action": "set",
                    "key": api_key,
                    "xpath": xpath,
                    "element": element,
                }

                # Send Config Request
                response = requests.post(config_url, params=params, verify=False)
                
                # Print Response for Each Entry
                print(f"Added Prefix {prefix}: {response.status_code}")
                print(response.text)
except FileNotFoundError:
    print(f"Error: File '{prefix_file}' not found.")
except Exception as e:
    print(f"Unexpected error: {e}")
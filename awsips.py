import json
import re
import requests

def extract_ips_from_json(json_data, region_filter):
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    
    def extract_ips(obj):
        if isinstance(obj, dict):
            return [ip for value in obj.values() for ip in extract_ips(value)]
        elif isinstance(obj, list):
            return [ip for item in obj for ip in extract_ips(item)]
        elif isinstance(obj, str):
            return ip_pattern.findall(obj)
        return []
    
    return list(set(extract_ips(json_data)))

def fetch_aws_ips(regions):
    url = "https://ip-ranges.amazonaws.com/ip-ranges.json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        filtered_ips = [prefix["ip_prefix"] for prefix in data["prefixes"] if prefix["region"] in regions]
        with open("aws_ips.txt", "w") as file:
            file.write("\n".join(filtered_ips))
        return filtered_ips
    else:
        return []

# Fetch and save IPs for eu-west-1 and eu-west-2
fetch_aws_ips(["eu-west-1", "eu-west-2"])
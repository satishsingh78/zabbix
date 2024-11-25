import requests
import json

# Zabbix API details
ZABBIX_API_URL = "http://44.203.236.104/zabbix/api_jsonrpc.php"
ZABBIX_USERNAME = "Admin"
ZABBIX_PASSWORD = "zabbix"

# Host details
HOST_NAME = "Cost-Dashboard"
HOST_IP = "3.209.22.148"
GROUP_ID = "2"  # Use the appropriate group ID from your Zabbix server
TEMPLATE_ID = "10001"  # Use the appropriate template ID

# Login function to get the authentication token
def zabbix_login():
    payload = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "username": ZABBIX_USERNAME,  # Use "username" for Zabbix 7
            "password": ZABBIX_PASSWORD
        },
        "id": 1
    }

    headers = {'Content-Type': 'application/json-rpc'}
    
    try:
        response = requests.post(ZABBIX_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_json = response.json()
            if 'result' in response_json:
                print("Login successful")
                return response_json['result']
            elif 'error' in response_json:
                print(f"API Error: {response_json['error']}")
        else:
            print(f"Failed to connect to Zabbix API: HTTP {response.status_code}")
            print("Response Text:", response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
    
    return None

# Function to add a host
def add_host(auth_token):
    payload = {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": {
            "host": HOST_NAME,
            "interfaces": [
                {
                    "type": 1,  # Agent interface
                    "main": 1,
                    "useip": 1,
                    "ip": HOST_IP,
                    "dns": "",
                    "port": "10050"
                }
            ],
            "groups": [
                {
                    "groupid": GROUP_ID
                }
            ],
            "templates": [
                {
                    "templateid": TEMPLATE_ID
                }
            ]
        },
        "auth": auth_token,
        "id": 2
    }

    headers = {'Content-Type': 'application/json-rpc'}
    
    try:
        response = requests.post(ZABBIX_API_URL, headers=headers, json=payload)
        
        if response.status_code == 200:
            response_json = response.json()
            if 'result' in response_json:
                print(f"Host '{HOST_NAME}' added successfully with hostid: {response_json['result']['hostids'][0]}")
            elif 'error' in response_json:
                print(f"API Error: {response_json['error']}")
        else:
            print(f"Failed to add host: HTTP {response.status_code}")
            print("Response Text:", response.text)
        
    except requests.exceptions.RequestException as e:
        print(f"HTTP Request failed: {e}")
        


# Main execution
if __name__ == "__main__":
    # Get authentication token
    token = zabbix_login()
    if token:
        print("Zabbix API Token:", token)
        # Add a host using the token
        add_host(token)
    else:
        print("Failed to authenticate with Zabbix API")


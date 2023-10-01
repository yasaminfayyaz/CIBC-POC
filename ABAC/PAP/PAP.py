import requests
"""
This script is used to push a XACML policy to the AuthzForce PDP.
"""

# Define the AuthzForce details
domain_id = "A0bdIbmGEeWhFwcKrC9gSQ"
#TODO: TBD host =
port = 8080
# Define the file path to the XACML policy
file_path = "Digital Policy/src-gen/CIBC.root.xml"

# Read the XACML policy from the file
with open(file_path, 'r', encoding='utf-8') as file:
    xacml_policy = file.read()

# Define the URL for the request
url = f"http://{host}:{port}/authzforce-ce/domains/{domain_id}/pap/policies"

# Define the headers as per the specification
headers = {
    "Content-Type": "application/xml; charset=UTF-8"
}

# Make the HTTP request to push the policy
response = requests.post(url, data=xacml_policy.encode('utf-8'), headers=headers)

# Check the response
if response.status_code == 200 or response.status_code == 201:
    print("Policy successfully pushed! Link to manage the new policy:", response.text)
else:
    print("Failed to push policy:", response.text)

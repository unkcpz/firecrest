#!/usr/bin/python3
import requests
import sys
import jwt
import json

keycloak_ip = sys.argv[1]

token_uri=f"http://{keycloak_ip}:8080/auth/realms/kcrealm/protocol/openid-connect/token"
client_secret="b391e177-fa50-4987-beaf-e6d33ca93571"
client_id="firecrest-sample"

print(f"client_id: {client_id}")
print(f"token_uri: {token_uri}")

headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {"grant_type":"client_credentials",
                "client_id": client_id,
            "client_secret":client_secret}

UTILITIES_URL="http://10.150.130.158:5004"
    
try:
  resp = requests.post(token_uri, headers=headers, data=data)

  if resp.ok:
    access_token = resp.json()['access_token']

    print(resp.json())

    print("Token OK")
    # decoded_token = jwt.decode(access_token, verify=False)
    # print(f"access_token: {resp.json()['access_token']}")
    # print(json.dumps(decoded_token, indent=4))
    

    resp_util = requests.get(f"{UTILITIES_URL}/ls", params={"targetPath":"/tmp"}, headers={"X-Machine-Name": "cluster", "Authorization": f"Bearer {access_token}"})

    print(resp_util.json())
    print(resp_util.headers)
    print(resp_util.status_code)
  else:
  
    print(resp.json())
    print(resp.status_code)
    print(resp.headers)

except Exception as e:
  print(f"Error: {e}")



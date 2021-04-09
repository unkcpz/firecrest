#!/usr/bin/python3
import requests
import sys
import jwt
import json

# keycloak_ip = sys.argv[1]

token_uri=f"http://localhost:8080/auth/realms/kcrealm/protocol/openid-connect/token"
client_secret="b391e177-fa50-4987-beaf-e6d33ca93571"
client_id="firecrest-sample"

print(f"client_id: {client_id}")
print(f"token_uri: {token_uri}")

headers = {"Content-Type": "application/x-www-form-urlencoded"}
data = {"grant_type":"client_credentials",
                "client_id": client_id,
            "client_secret":client_secret}

FIRECREST_URL = "http://localhost:8000"
    
try:
  print("#####################################################")
  print("TEST KEYCLOAK")
  print("-----------------------------------------------------")
  resp = requests.post(token_uri, headers=headers, data=data)
  if not resp.ok:    
  
    print(resp.json())
    print(resp.status_code)
    print(resp.headers)
    print("-----------------------------------------------------")
    print("KEYCLOAK ERROR")
    sys.exit(1)
except Exception as e:
  print(f"Error: {e}")
  print("-----------------------------------------------------")
  print("KEYCLOAK ERROR")
  sys.exit(1)
  
try:
  access_token = resp.json()['access_token']

  print(resp.json())
  print("-----------------------------------------------------")
  print("KEYCLOAK OK")
  # decoded_token = jwt.decode(access_token, verify=False)
  # print(f"access_token: {resp.json()['access_token']}")
  # print(json.dumps(decoded_token, indent=4))
  print("#####################################################")
  print("TEST STATUS")
  print("-----------------------------------------------------")
  resp_status = requests.get(f"{FIRECREST_URL}/status/services", headers={"Authorization": f"Bearer {access_token}"})
  if resp_status.ok:
    print(json.dumps(resp_status.json(),indent=2))
    print("-----------------------------------------------------")      
    print("STATUS OK")
    
  else:

    print(resp_status.text)
    print(resp_status.headers)
    print(resp_status.status_code)
    print("-----------------------------------------------------")
    print("STATUS ERROR") 
except Exception as e:
  print(f"Error: {e}")
  print("-----------------------------------------------------")
  print("STATUS ERROR")
  

try:
  print("#####################################################")
  print("TEST UTILITIES")
  print("-----------------------------------------------------")
  resp_util = requests.get(f"{FIRECREST_URL}/utilities/ls", params={"targetPath":"/tmp"}, headers={"X-Machine-Name": "cluster", "Authorization": f"Bearer {access_token}"})

  if resp_util.ok:
    print(json.dumps(resp_util.json(),indent=2))
    print("-----------------------------------------------------")
    print("UTILITIES OK")      
  else:

    print(resp_util.text)
    print(resp_util.headers)
    print(resp_util.status_code)
    print("-----------------------------------------------------")
    print("UTILITIES ERROR") 
except Exception as e:
  print(f"Error: {e}")
  print("-----------------------------------------------------")
  print("UTILITIES ERROR")
  
 

except Exception as e:
  print(f"Error: {e}")
  




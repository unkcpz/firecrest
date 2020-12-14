#!/usr/bin/python3
import requests
import sys

opa_ip = sys.argv[1]

opa_uri=f"http://{opa_ip}:8181/v1/data/f7t/authz"
data_ok = {"input":{"user": "test1", "system": "cluster"}}
data_err= {"input":{"system":"cluster", "user":"none"}}

print(opa_uri)

    
try:
  resp_ok = requests.post(opa_uri, json=data_ok)
  resp_err = requests.post(opa_uri, json=data_err) 


  if resp_ok.ok:
    print(f"Test OK: access: {resp_ok.json()['result']}")
  else:
  
    print(resp_ok.json())
    print(resp_ok.status_code)
    print(resp_ok.headers)

  if resp_err.ok:
    print(f"Test ERR: access: {resp_err.json()['result']}")
  else:

    print(resp_err.json())
    print(resp_err.status_code)
    print(resp_err.headers)

except Exception as e:
  print(f"Error: {e}")


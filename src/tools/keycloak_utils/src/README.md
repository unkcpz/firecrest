# Keycloak Service Account abstraction

The Python class `KeycloakServiceAccount` can be used to simplify development of Keycloak clients with Service Account approach.

## Setting up the class constructor

```
import keycloak_utils

keycloak = keycloak_utils.KeycloakServiceAccount(client_id, client_secret, token_uri, debug=True)

```

## Using the login decorator

Example with Bearer token authentication

```
@keycloak.service_account_login
def test_api():
        
    headers = {f"Authorization": f"Bearer {keycloak.get_access_token()}"}

    resp = requests.get(f"{api_url}/endpoint", headers=headers)

```

## Demo client for FirecREST

```
git clone https://github.com/eth-cscs/firecrest
cd firecrest
git checkout tutorial
cd src/tools/keycloak_utils/src
```

Replace `client_id`, `client_secret`, `token_uri` and `firecrest_url` with correspondent values in `client.py`

```
python3 client.py
```
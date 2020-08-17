import keycloak_utils
import json
import time
import requests


# These fields should be filled with corresponding data
client_id = "" # client_id from keycloak ŕegistration
client_secret = "" # client_secret returned on keycloak ŕegistration
token_uri = "" # URI of the token endpoint in keycloak server "https://auth.your-keycloak-server.com/auth/realms/cscs/protocol/openid-connect/token"
firecrest_url = "" # URL of the firecrest instance where to connect

# Create a keycloak service account object
keycloak = keycloak_utils.KeycloakServiceAccount(client_id, client_secret, token_uri, debug=True)

# the decorator logins and refresh without user or client intervention
@keycloak.service_account_login
def test_status():
    """Test the service status endpoint of firecrest: firecrest_url/status/services
    """

    headers = {f"Authorization": f"Bearer {keycloak.get_access_token()}"}

    resp = requests.get(f"{firecrest_url}/status/services", headers=headers)

    print(json.dumps(resp.json(), indent=2))



if __name__ == "__main__":
    test_status()
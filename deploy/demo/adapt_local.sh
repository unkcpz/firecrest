#!/bin/bash

if [ $# -ne 2 ]; then echo "Usage: adapt_local.sh cluster_username  local_ssh_priv_key_path"; exit 1; fi



echo "Adapting for local config:"
echo " - Keycloack"
sed  -i -e 's#"username" : "test1"#"username" : "'$1'"#'  keycloak/config.json
echo " - OPA"
sed  -i -e 's#"test1"#"'$1'"#'  opa/data.json
echo " - .env"
sed -i 's#USER_KEY_PRIV=.*#USER_KEY_PRIV='$2'#' .env

echo "done."




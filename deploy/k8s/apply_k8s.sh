#!/bin/bash

wait_running() {
  echo -n "  - waiting for $1 "
  k1=''
  while [ "$k1" == "" ]; do
    k1=$(kubectl get pods | grep ^deploy-$1 | grep Running)
    echo -n "."
    sleep 1;
  done
  echo ' up'
  pod=${k1%% *}
}


echo "* Deleting services..."
kubectl delete all --all --grace-period=3
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi

echo -n "* Killing port forwardings..."
pkill -f "kubectl port-forward deploy-"
echo ""

echo -e "\n* Starting k8s..."
kubectl apply -f . -R
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
echo "  done."

echo -e "\n* Creating port forwardings..."
pod=""
wait_running kong
kubectl port-forward $pod 8000:8000 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$!"

wait_running keycloak
kubectl port-forward $pod 8080:8080 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running minio
kubectl port-forward $pod 9000:9000 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running jaeger
kubectl port-forward $pod 16686:16686 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running openapi
kubectl port-forward $pod 9090:8080 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running f7t-client
kubectl port-forward $pod 7000:5000 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

echo "  all done, to kill forward processes: kill $p"

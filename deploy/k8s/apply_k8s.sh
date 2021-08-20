#!/bin/bash

microservices="certificator client cluster compute config jaeger keycloak kong minio openapi reservations status storage tasks utilities"

wait_running() {
  echo -n "  - waiting for $1 "
  k1=''
  while [ "$k1" == "" ]; do
    k1=$(microk8s kubectl get pods | grep ^deploy-$1 | grep Running)
    echo -n "."
    sleep 1;
  done
  echo ' up'
  pod=${k1%% *}
}


echo "* Deleting services..."
microk8s kubectl delete all --all --grace-period=3
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi

echo "* Deleting network policies..."
microk8s kubectl delete networkpolicy --all
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi

echo -n "* Killing port forwardings..."
pkill -f "kubectl port-forward deploy-"
echo ""

for ms in $microservices
do
  echo -e "\n* Starting $ms..."
  kubectl apply -f $ms -R
  if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
  echo "  done."
done

echo -e "\n* Creating port forwardings..."
pod=""
wait_running kong
microk8s kubectl port-forward $pod 8000:8000 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$!"

wait_running keycloak
microk8s kubectl port-forward $pod 8080:8080 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running minio
microk8s kubectl port-forward $pod 9000:9000 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running jaeger
microk8s kubectl port-forward $pod 16686:16686 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running openapi
microk8s kubectl port-forward $pod 9090:8080 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

wait_running f7t-client
microk8s kubectl port-forward $pod 7000:5000 &> /dev/null &
if [ $? -ne 0 ]; then echo 'failed.'; exit 1; fi
p="$p $!"

echo "  all done, to kill forward processes: kill $p"

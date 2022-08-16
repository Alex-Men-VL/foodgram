#!/bin/bash -e

cd `dirname "$0"`

echo "Run deploy"
echo

kubectl apply -f configmap.yaml
kubectl apply -f component_backend.yaml
kubectl apply -f component_frontend.yaml
kubectl apply -f ingress_service.yaml

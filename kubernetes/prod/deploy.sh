#!/bin/bash -e

cd `dirname "$0"`

echo "Run deploy"
echo

kubectl apply -f configmap.yaml
kubectl apply -f django.yaml

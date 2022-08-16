#!/bin/bash -e

cd `dirname "$0"`

echo "Run deploy"
echo

# Setup configmap
kubectl apply -f configmap.yaml

# Run django jobs
for manifest in job_django.yaml cron_job_clearsessions.yaml
do
    kubectl apply -f $manifest
done

# Start backend & frontend services
for manifest in component_django.yaml component_react.yaml
do
    kubectl apply -f $manifest
done

# Start ingress service
kubectl apply -f ingress_service.yaml

echo
echo "Project deployed successfully"

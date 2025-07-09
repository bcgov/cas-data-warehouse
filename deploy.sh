#!/bin/bash

### Script meant for shipit to set the appropriate environment variables,
### and deploy the helm chart with the required values.
set -euo pipefail

git_sha1=$(git rev-parse HEAD)

dagConfig=$(echo "{\"org\": \"bcgov\", \"repo\": \"cas-ciip-portal\", \"ref\": \"$(git_sha1)\", \"path\": \"dags/cas_data_warehouse_import_data_sources.py\"}" | base64 -w0); 

helm dep up ./helm/cas-data-warehouse
helm repo add cas-postgres https://bcgov.github.io/cas-postgres/
helm repo update

helm upgrade --install --timeout 900s \
  --namespace "$CIIP_NAMESPACE_PREFIX-$ENVIRONMENT" \
  -f ./helm/cas-data-warehouse/values.yaml \
  -f "./helm/cas-data-warehouse/values-$ENVIRONMENT.yaml" \
  --set download-cas-ciip-portal-dags.dagConfiguration="$dagConfig" \
  cas-data-warehouse ./helm/cas-data-warehouse 

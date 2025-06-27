#!/bin/bash

### Script meant for shipit to set the appropriate environment variables,
### and deploy the helm chart with the required values.
set -euo pipefail

gitsha1=$(git rev-parse HEAD)
dagConfig=$(echo "{\"org\": \"bcgov\", \"repo\": \"cas-data-warehouse\", \"ref\": \"$gitsha1\", \"path\": \"dags/cas_data_warehouse_import_data_sources.py\"}" | base64 -w0); 

helm dep up ./helm/cas-data-warehouse
helm repo add cas-postgres https://bcgov.github.io/cas-postgres/
helm repo update

helm upgrade --install --timeout 900s \
  --namespace "$CIIP_NAMESPACE_PREFIX-$ENVIRONMENT" \
  -f ./helm/cas-data-warehouse/values.yaml \
  -f "./helm/cas-data-warehouse/values-$ENVIRONMENT.yaml" \
  --set download-cas-data-warehouse-dags.dagConfiguration="$dagConfig" \
  cas-data-warehouse ./helm/cas-data-warehouse 

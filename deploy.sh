#!/bin/bash

### Script meant for shipit to set the appropriate environment variables,
### and deploy the helm chart with the required values.
set -euo pipefail

git_sha1=$(git rev-parse HEAD)

helm dep up ./helm/cas-data-warehouse
helm repo add cas-postgres https://bcgov.github.io/cas-postgres/
helm repo update

helm upgrade --install --timeout 900s \
  --namespace "$CIIP_NAMESPACE_PREFIX-$ENVIRONMENT" \
  -f ./helm/cas-data-warehouse/values.yaml \
  -f "./helm/cas-data-warehouse/values-$ENVIRONMENT.yaml" \
  cas-data-warehouse ./helm/cas-data-warehouse 
  
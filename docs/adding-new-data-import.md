

## Adding a new data import

A few things need to be done to add a new data source for this data warehouse:

- [ ] Create a cronjob with an import script in the helm chart
- [ ] Add that cronjob as part of the import DAG
- [ ] The data source will need to allow remote access through a KNP - see example below

## Example remote access KNP for the data warehouse import

```yaml
kind: NetworkPolicy
apiVersion: networking.k8s.io/v1
metadata:
  name: <<my app name>>-allow-warehouse-import
spec:
  podSelector:
    matchLabels:
      app.kubernetes.io/instance: <<my app name>>
  ingress:
    - from:
        - podSelector:
            matchLabels:
              app.kubernetes.io/instance: cas-data-warehouse
          namespaceSelector:
            matchLabels:
              environment: {{ .Values.environment }}
              name: {{ .Values.warehouse.namespace }}
  policyTypes:
    - Ingress
```

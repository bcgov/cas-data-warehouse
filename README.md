# CAS Data Warehouse

A data warehouse to help ingest several different sources of data


### Roadmap

#### 1. V1

A single postgres cluster with a single database.

Features and shortcomings
- Every data source will be ingested as a separate postgresql schema
- Permissive data access with no restrictions (user roles will have access to all the data in the warehouse)


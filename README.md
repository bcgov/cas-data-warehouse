# CAS Data Warehouse

A data warehouse to help ingest several different sources of data


### Roadmap

#### 1. V1 (in progress)

A single postgres cluster with a single database.

Features and shortcomings
- Every data source will be ingested as a separate postgresql schema
- Permissive data access with no restrictions (user roles will have access to all the data in the warehouse)



#### 2. V2

A multi-database deployment with:
- push strategy from the various data sources
- a query engine like trino.io allowing users to aggregate datasets seamlessly
- a comprehensive data access framework allowing data sharing with multiple access scopes

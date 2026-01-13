# CAS Data Warehouse

A data warehouse to help ingest several different sources of data


### Roadmap

#### 1. V1 (in progress)

A single postgres cluster with a single database.

Features and shortcomings
- Every data source will be ingested as a separate postgresql schema
- Permissive data access with no restrictions (user roles will have access to all the data in the warehouse)

Documentation on how to add data sources to this deployment can be found [here](./docs/adding-new-data-import.md)

#### 2. V2

A multi-database deployment with:
- push strategy from the various data sources
- a query engine like trino.io allowing users to aggregate datasets seamlessly
- a comprehensive data access framework allowing data sharing with multiple access scopes


### Release process

The release process is handled automatically by [release-it](https://github.com/release-it/release-it).
To start a release:
- create and checkout a `chore/release` branch: `git checkout -b chore/release`
- push the branch to the remote: `git push -u origin chore/release`
- run `yarn release`
- Create PR & merge
- To push to -test and -prod, merge develop into main: 
  - `git checkout main`
  - `git merge develop --ff-only`
  - `git push`
  
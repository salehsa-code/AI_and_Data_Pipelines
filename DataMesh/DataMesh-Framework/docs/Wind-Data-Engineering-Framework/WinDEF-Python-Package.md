# WinDEF Python Package

As mentioned [here](../Wind-Data-Engineering-Framework.md#overview) WinDEF is one
of the central tools to share code among developers and teams. It consists of a
number of sub-packages/modules.

## (Sub-)Modules

The frameworks modules can be roughly grouped into the following categories:

### 1. Data Handling

Contains tools to interact with data sources and targets.

The (sub)-modules are:

- `reader`: Read data from different sources.
- `writer`: Write data to different targets.
- `delta_manager`: Manage Delta tables, including e.g., merges and appends.

> Find the [user documentation here](./User-Guide/Data-Handling.md).

### 2. Validation

The Data Validation module is used to validate the actual data of a Table or
Column. It will check if the data is valid and consistent according to checks
defined in the data contract.

> Find the [user documentation here](./User-Guide/Data-Validation.md).

### 3. Clients

WinDEF defines clients to interact with different external services.

The (sub)-modules are:

- `api_client`: An API Client to interact with REST APIs.
- `power_bi_client`: Power BI REST API, e.g. to refresh a dataset.
- `alation_client`: Alation REST API, e.g. to update Metadata in Alation.

> Find the [user documentation here](./User-Guide/Clients.md).

### 4. Metadata

Tools to parse and validate Metadata from Data Contracts.

The (sub)-modules are:

- `models`: This module includes a parser for Data Contracts, and Adapters to
  derive Metadata from different source, e.g., Unity Catalog schemas or tables.

> Find the [user documentation here](./User-Guide/Model.md).

### 5. Utils

Utility tools to support data engineering tasks.

The (sub)-modules are:

- `logging`: Logging utilities, e.g. Log Analytics Handler.
- `session`: Abstractions for Databricks Sessions and DBUtils.

> Find the [user documentation here](./User-Guide/Utils.md).

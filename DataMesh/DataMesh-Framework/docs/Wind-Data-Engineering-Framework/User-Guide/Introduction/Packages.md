# Packages

The Wind Data Engineering Framework is a collection of packages that provide
tools for data engineering tasks in the BA Wind. The packages can roughly be
categorized into the following groups:

- **Data Handling**: Tools to interact with data sources and targets.
  - `data_handling`, incl. `reader`, `writer`, `delta_manager`, ...
- **Validation**: Provides tools to validate data.
  - `validation`
- **Clients**: Clients to interact with different external services.
  - `api_client`: An API Client to interact with REST APIs.
  - `power_bi_client`: Power BI REST API, e.g. to refresh a dataset.
  - `alation_client`: Alation REST API, e.g. to update Metadata in Alation.
- **Metadata**: Tools to parse and validate Metadata from Data Contracts.
  - `models`, incl. Contract parser and Adapters.
- **Utils**: Utility tools to support data engineering tasks.
  - `logging`: Logging utilities, e.g. Log Analytics Handler.
  - `session`: Abstractions for Databricks Sessions and DBUtils.

The dependencies between these packages can be visualized as follows:

:::mermaid
graph LR
    A[alation_client]
    B[power_bi_client]
    C[api_client]
    D[logging]
    E[session]
    F[data_handling]
    G[validation]
    H[models]
    I[pipeline]

    A --> D
    A --> H

    B --> C
    B --> D

    C --> E
    C --> D

    F --> E
    F --> D
    F --> H

    G --> E

    I --> Z[*]

:::

> The `pipeline` packages make use of all other packages by implementing them in
> pipeline actions. This is not reflected in the graph above for readability.

# Onboarding

This document outlines the process of onboarding a new data product.

> From the platform's perspective, we don't directly map products to VDTs. A VDT
> that is already onboarded to WDAP might skip some steps, such as if AD Groups
> are reused. This may be sensible in certain cases, for instance, if the
> developer groups are the same, but it is not generally a good solution and
> depends on the specific use case.

:::mermaid
graph LR
    B[Value Delivery Team] -.->|1:n| A[Data Product]
:::

## Process

During this process the **Data Kong** provide this to the **VDT**:

- Onboarding to platform Access Management
- Pre-configured DevOps repository
- Databricks and Unity Catalog resources
- Containers on the ADLS

---

The following diagrams show the dependency and responsibilities for tasks
related to onboarding a new data product. The diagram below defines the color
coding.

:::mermaid
flowchart
    style A fill:#003f5c,stroke-width:1px,color:#fff
    style B fill:#f95d6a,stroke-width:1px,color:#fff

    subgraph Legend
        direction TB
        A[Value Delivery Team]
        B[Data Kong]
    end
:::

> The length of objects in the gantt chart does not indicate the actual time to complete.

## Access Management

The onboarding for Access Management is a shared responsibility between the
Value Delivery Team (VDT) and Data Kong.

:::mermaid
flowchart LR
    style A fill:#003f5c,stroke-width:1px,color:#fff
    style B fill:#003f5c,stroke-width:1px,color:#fff
    style C fill:#f95d6a,stroke-width:1px,color:#fff

    A[Order AD Groups]
    B[Define Omada Role Mapping]
    C[Order Omada Roles]

    A --> B --> C
:::

To enable Access Management, these steps are required:

1. The **VDT** prepares the Active Directory groups (follow [this
process](../Access-Management/New-Dataproduct.md#ad-groups)).
1. The **VDT** defines the mapping of groups to Omada Roles in this format:
   | Role   | AD Group   |
   | ------ | ---------- |
   | Role 1 | AD Group 1 |
   | Role 1 | AD Group 2 |
   | Role 2 | AD Group 3 |
1. The **Data Kong** order the Omada Roles from the Active Directory team,
following [this process](../Access-Management/New-Dataproduct.md#omada-roles).

## Resources & Infrastructure

:::mermaid
flowchart LR
    style A fill:#003f5c,stroke-width:1px,color:#fff
    style B fill:#f95d6a,stroke-width:1px,color:#fff
    style C fill:#003f5c,stroke-width:1px,color:#fff
    style D fill:#003f5c,stroke-width:1px,color:#fff

    A[Fill in Configuration]
    B[Bootstrap data product]
    C[Update Configuration in Repo]
    D[Trigger Infrastructure CI/CD pipeline ]

    A --> B --> C --> D
:::

These steps are required for the deployment of Azure Resources:

1. The **VDT** completes the configuration files for the data product bootstrap.
Find the documentation for this
[here](../IaC-Framework/Solutions/20-Data-Product-Bootstrap.md).
1. The **Data Kong** will deploy the bootstrapped resources. Which resources
are deployed is specified in [this
documentation](../IaC-Framework/Solutions/20-Data-Product-Bootstrap.md).
1. The **VDT** updates the configuration files deployed during the
   bootstrapping.
1. The **VDT** executes the [Data Product Azure CICD
   Pipeline](../IaC-Framework/Solutions/21-Data-Product.md). Find a description
   about how to execute the pipeline
   [here](../IaC-Framework/IaC-Framework-User-Guide.md#using-the-deployment-pipelines).

## Data

:::mermaid
flowchart LR
    style A fill:#003f5c,stroke-width:1px,color:#fff
    style B fill:#003f5c,stroke-width:1px,color:#fff
    style C fill:#f95d6a,stroke-width:1px,color:#fff

    A[Identify relevant data sources]
    B[Fill in Data Contract Metadata]
    C[Integrate sources]

    A --> B --> C
:::

These steps are required for the integration of data:

1. The **VDT** defines the required data sources
2. The **VDT** completes the data product contract
    > This does not necessarily have to include the metadata for all tables, columns etc.
3. The **Data Kong** ensure availability of primary data products derived
   from the information about required data sources and the business object
   model.

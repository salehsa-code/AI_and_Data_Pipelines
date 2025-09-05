# Access Management Concepts for WDAP

## Content

1. [Concepts](Access-Management) (this document)
2. [Responsibilities](Access-Management/Responsibilities.md)
3. [Processes](Access-Management/Processes.md)
4. [Naming](Access-Management/Naming.md)
5. [Omada](Access-Management/Omada.md)

## Components

> The resources outlined in this section are examples and may not represent the full list.

| Azure Resources   | Power BI Service | Azure DevOps     | Azure Databricks |
|-------------------|------------------|------------------|------------------|
| Resource Group    | Datasets         | Git Repositories | Clusters         |
| Key Vault         | Workspace        | Branch Policies  | Cluster Policies |
| Azure Data Lake   | App              | Azure Pipelines  | Secret Scope     |
| Databricks Workspace | Deployments   | Project          | Data Objects in UC |
| ... | ...   | ...          | ... |

## Environments

![Access Patterns across Environments](./.img/access-management/access-patterns.png =600x)

## Personas

> Please note that this list aims to cover all major personas, but it may not be exhaustive.

![Personas in WDAP](./.img/access-management/personas.png =600x)

### End Users

- Reporting Users: These users have access to reports, dashboards, and apps, primarily on Power BI.
- Data Analysts: They use datasets to derive insights and may expand on these datasets.
- Data Scientists: Their role is to develop machine learning models.

### Product Delivery

#### Development

- BI Analyst
- Data Engineer
- Data Scientist
- Administrators
- Service Users: These are technical users such as Service Principal or Managed Identity.
- Product Owners
- Business Controllers: They define and translate business requirements, construct prototypes, and possess write permissions on the Sandbox

#### Test Users

- Testers: This role is typically held by Business Controllers.

#### Additional Personas

- Scrum Master
- Solution Designer

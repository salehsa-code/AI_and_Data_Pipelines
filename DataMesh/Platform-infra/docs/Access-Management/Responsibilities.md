# Responsibilities

[[_TOC_]]

## Scope

The Scope of this document is to define which components of the platform
permissions can be granted on and in whoms responsibility it lies to grant or
deny those permissions.

## Components

### Data-related-resources

::: mermaid
graph TB
    subgraph business ["Business"]
        D[Business Application]
    end

    subgraph dataProductTeam ["Data Product Team"]
        C[Secondary Data Product]
    end

    subgraph dataKong ["Data Kong"]
        A[Azure Data Lake Storage]
        B[Primary Data Product]
    end

:::

#### Azure Data Lake Storage (ADLS)

Data Kong are responsible for granting access to raw files in ADLS. This can be
achieved through either Role-Based Access Control (RBAC) assignments or Access
Control Lists (ACLs). The process is
[defined here](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Analytics%20Platform/17682/processes).

However, in most cases, these measures may not be necessary as data consumption requests
should be processed via the Unity Catalog (UC). For specific scenarios, it
may be necessary to create [Volumes](https://learn.microsoft.com/en-us/azure/databricks/sql/language-manual/sql-ref-volumes),
an action that must be performed by Data Kong. This centralizes Access Management
information in a single location.

#### Primary & Secondary Data Products

> :warning: Access to Tables and Views
> The Infrastructure as Code (IaC) framework currently doesn't support providing
> access to individual tables or views. If such a feature becomes necessary,
> it would require development and implementation by the Data Kong.

While Primary and Secondary Data Products are in different areas of responsibility,
both follow the same process. For Primary Data Products the _Data Kong_ Product Owner
is responsible, while for the Data Product, the _Data Product_ Owner is responsible.

Access to these external locations and schemas can be managed through a configuration
file in the Data Products' repository. Refer to this [Process Guide]([link](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Analytics%20Platform/17160/processes?anchor=request-data-product-access-in-unity-catalog))
or this [Configuration Guide](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Analytics%20Platform/17160/processes?anchor=request-data-product-access-in-unity-catalog)
for detailed instructions.

#### Business Applications

The Business team is in charge of managing access to Business Applications,
and this needs to be determined on an application-by-application basis.
The Data Product Team sets up roles in Omada, enabling users to request access
as per the process [outlined here](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Analytics%20Platform/17160/processes?anchor=request-business-application-access).

### Platform-related-resources

::: mermaid
graph TB
    subgraph platformOwner ["Platform Owner*"]
        subgraph azureDevOps ["Azure DevOps"]
            C
            D
            G
        end
        subgraph azureResources ["Azure Resources"]
            A
            B
        end
        E
    end

    A[Azure Resource Groups]
    B[Core Azure Key Vaults]
    C[Core Repositories]
    D[Core Build Pipelines]
    E[Omada Roles]
    G[DevOps Project]
:::
\* Implementations are done by the Data Kong team.

::: mermaid
graph TB
    subgraph Data Product Team
        subgraph azureDevOpsDP ["Azure DevOps"]
            F
            J
        end
        subgraph azureResourcesDP ["Azure Resources"]
            I
        end
        K
    end

    F[Data Product Repository]
    I[Data Product Azure Key Vaults]
    J[Data Product Build Pipelines]
    K[DP Omada Roles]
:::

#### Azure Resource Groups (RG)

By default, all developers in any Data Product Omada Role receive the 'Reader'
role for the environment's resource group (RG). Only the Infrastructure Team,
namely the Data Kong, have Contributor permissions on the RGs.

If more resource group role-based access control (RBAC) assignments are needed,
the Platform Owner must evaluate and assign them through the Cloud Service Portal
(CSP).

#### Azure Key Vaults (KV)

The KVs `vap2-<env>-winddata-[atm|cmn]-kv` are exclusively for the Data Kong
Team's use, and no other team should have role-based access control (RBAC) or access
control list (ACL) access.

Each Data Product can deploy a KV using the `21-data_product` terraform solution
within the Infrastructure as Code (IaC) Framework. The access control lists for
this key vault can be managed through a configuration file located in the Data
Products' repository, as detailed in the [linked
documentation](../IaC-Framework/Solutions/21-Data-Product.md).

#### DevOps Project

Access to the DevOps project is automatically granted via the Omada roles for developers, e.g., `Data Engineer DEV`.

Additional requests and DevOps specific permissions can be requested from the Platform
Owner or a delegate (e.g., a Scrum Master) and must be implemented manually.

#### DevOps Repository

Data Kong are granted access to the `core repositories` through their specific Azure
Active Directory (AAD) groups. All teams have read access to these repositories and can
submit pull requests to the `Datapipeline Framework` & `Tools` repositories.

Access to Data Product repositories is initially given to the respective Data Product
AAD groups during the bootstrapping of a new Data Product. After this, the Data Product
team can manage their own access.

#### Build Pipelines

Central Build Pipelines are exclusively for Data Kong, which include pipelines for
solutions like `11-platform-infra` & `12-workspace_config`. Access to run these
pipelines is given to the Data Kong through their AAD groups.

Data Product pipelines are stored in the core infrastructure repository
[wind-da-platform-infra](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-infra?path=/build-scripts/terraform&version=GBmain&_a=contents).
They cannot be altered by the Data Product team, even though the Team can run these
pipelines to configure their infrastructure. The configuration files for these
pipelines are located in the Data Product repository.

#### Omada Roles

Platform related Omada roles (such as "Data Engineer DEV" etc.) are maintained by the Platform Owner.
Data Product related Omada roles (such as "Windcockpit Reader DEV" etc.) are maintained by the Data Product
Team and governed by the Business.
the process to order Omada Roles is described
[here](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Analytics%20Platform/17160/processes?anchor=create-an-omada-resource).
General information about Omada is documented
[here](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Analytics%20Platform/17159/omada).

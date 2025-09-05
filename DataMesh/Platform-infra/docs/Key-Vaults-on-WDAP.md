# Key Vaults on WDAP

Key Vaults are an essential solution for managing secrets on WDAP, and provide a secure way to share secrets between users or programs.

> :bulb: WDAP supports an automated secret rotation, that supports different types of secrets. Find a detailed guide [here](./VCS/Solutions/Secret-Rotation.md).

## Core Key Vaults

| Key Vault Name | Environments | Scope |
| --- | --- | --- |
| **`vap2-<env>-winddata-dbx-kv`** | `dev`, `tst`, `acc`, `prd` | Secrets, that should be accessible to every user of WDAP. These are crucial for WinDEF to work. E.g. Key for the Log Analytics Workspace. This Key Vault is accessible as a keyvault-backed secret scope on the ELT Databricks Workspace. |
| **`vap2-<env>-argocd-kv`** | `dev`, `prd` | Secrets, that are used by the ArgoCD k8s integration. These are potentially accessible to every user of the winddata k8s namespace and are used, e.g., for the authentication of ArgoCD towards Azure DevOps and jFrog. |
| **`vap2-<env>-winddata-atm-kv`** | `dev`, `tst`, `acc`, `prd` | Secrets, that are used in Data Kong automation processes. Access to this Key Vault should not be shared outside of Data Kong, because it allows for potential elevation of privileges. These include e.g. the client secrets for ETL Service Principals and the Access Management Monitoring Principal |
| **`vap2-<env>-winddata-cmn-kv`** | `dev`, `tst`, `acc`, `prd` | Secrets, that are used by Data Kong outside of automation processes. Access to this Key Vault should not be shared outside of Data Kong, because it allows for potential elevation of privileges. This Key Vault stores e.g. access data for s1 and s7 users. |

## Data Product Key Vaults

Data products can opt to create a new Key Vault that is managed by the IaC
Framework. Find a more detailed description for this
[here](./IaC-Framework/IaC-Framework-User-Guide.md#creating-a-new-data-product).
The scope of this Key Vault can be defined by the Value Delivery Team
responsible for the Data Product.

## Where to store new secrets?

::::mermaid
flowchart TD
    A[Start] --> B{Is it Product related?}
    B -->|Yes| C[Proceed to VDT Decision]
    B -->|No| D{Is it Accessible to all<br>WDAP Users?} -->|Yes| E["vap2-$env$-winddata-dbx-kv"]
    D -->|No| G{Is it Required in k8s?}
    G -->|Yes| H{Is it ArgoCD specific?} -->|Yes| I["vap2-$env$-argocd-kv"]
    H -->|No| J{Is it use case specific?} -->|Yes| K{Is it a Data <br>Kong use case?}
    K -->|Yes| L["vap2-$env$-winddata-atm-kv"]
    K -->|No| M[Proceed to VDT Decision]
    D -->|No| N{For Automation<br>use case?} -->|Yes| P["vap2-$env$-winddata-atm-kv"]
    D -->|No| O{For Non-Automation<br>use case?}  -->|Yes| Q["vap2-$env$-winddata-cmn-kv"]
::::

This is a terraform solution for the deployment of the core infrastructure of
the Wind Data Platform. It deploys the storage accounts for the data lake
layers on the platform, as well as the storage account and file system for the
Unity Catalog.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azapi | >= 1.13.0 |
| azurerm | ~> 3 |
| databricks | >=1.7.0 |

## Providers

| Name | Version |
|------|---------|
| azurerm | ~> 3 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| action\_group | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/action_group | 20240404.3 |
| datalake\_blob\_service\_logs | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/diagnostic_settings | 20240116.2 |
| datalake\_storage\_accounts | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/storage_account | 20241017.2 |
| datalake\_storage\_container | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/adls_filesystem | 20240116.2 |
| log\_alert | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/log_alert | 20240805.1 |
| uc\_additional\_storage\_container | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/adls_filesystem | 20240116.2 |
| uc\_blob\_service\_logs | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/diagnostic_settings | 20240116.2 |
| uc\_storage\_account | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/storage_account | 20241017.2 |
| uc\_storage\_container | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/adls_filesystem | 20240116.2 |

## Resources

| Name | Type |
|------|------|
| [azurerm_databricks_access_connector.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/databricks_access_connector) | resource |
| [azurerm_key_vault.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault) | resource |
| [azurerm_log_analytics_workspace.monitoring](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/log_analytics_workspace) | resource |
| [azurerm_user_assigned_identity.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/user_assigned_identity) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |
| [azurerm_log_analytics_workspace.monitoring](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/log_analytics_workspace) | data source |
| [azurerm_resource_group.wdap](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/resource_group) | data source |
| [azurerm_subnet.allowed_list](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/subnet) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the lakehouse storage configs directory. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| databricks\_access\_connector\_id | Id of the Databricks access connector used for external locations. |
| databricks\_access\_connector\_name | Name of the Databricks access connector used for external locations. |
| key\_vault\_id | Map of Key Vault Ids |
| key\_vault\_network\_acls | Firewall settings of the key vaults. |
| log\_analytics\_diagnostic\_settings\_name | Name of the diagnostic settings used for monitoring |
| log\_analytics\_workspace\_id | Name of the log analytics workspace |
| log\_analytics\_workspace\_name | Name of the log analytics workspace |
| resource\_group\_ids | Id of the resource group where the platform is deployed. |
| resource\_group\_locations | Azure region of the resource group where the platform is deployed. |
| resource\_group\_names | Name of the resource group where the platform is deployed. |
| storage\_account\_ids | A map of WDAP storage accounts and their Ids. |
| storage\_account\_names | A map of WDAP storage accounts and their names. |
| uc\_storage\_container\_name | Name of the catalog storage container on the root storage account. |
| uc\_storage\_credential\_name | Id of the Databricks access connector used for external locations. |
| user\_assigned\_identity\_id | Resource Id of the user assigned identities. |

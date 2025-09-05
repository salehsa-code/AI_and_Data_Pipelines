This is a terraform solution for the depoloyment of the infrastructure managed
by a data prodcut.

Filesystems are deployed to the data lake storage accounts and directories are
created.

Based on the directories, external locations and corresponding schemas are
created in the Databricks catalog.

Permissions on the Databricks catalog objects are set.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azurerm | ~>3 |
| databricks | >=1.37.0 |

## Providers

| Name | Version |
|------|---------|
| azurerm | ~>3 |
| databricks.etl | >=1.37.0 |
| terraform | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| action\_group | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/action_group | 20240404.3 |
| adls\_filesystem | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/adls_filesystem | 20240404.3 |
| external\_location | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_external_location | 20240404.3 |
| external\_volume | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_external_volume | 20240404.3 |
| kv\_secret\_scope\_etl | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/secret_scope_kv | 20240404.3 |
| kv\_secret\_scope\_srv | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/secret_scope_kv | 20240404.3 |
| log\_alert | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/log_alert | 20240404.3 |
| schema | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_schema | 20240404.3 |
| tables | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_table | 20240529.1 |

## Resources

| Name | Type |
|------|------|
| [azurerm_key_vault.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault) | resource |
| [azurerm_key_vault_secret.external_location_path](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault_secret) | resource |
| [databricks_directory.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/directory) | resource |
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |
| [terraform_remote_state.dbrks_catalog](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.dbrks_workspace_etl](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.dbrks_workspace_srv](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.platform_infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the backend storage configs directory. | `string` | yes |

## Outputs

No outputs.

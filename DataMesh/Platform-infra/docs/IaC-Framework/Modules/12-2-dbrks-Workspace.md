This is a terraform solution for the deployment of the Databricks Workspace
Configuration.

Custom workspace configurations are set. Cluster policies, secret scopes and
cluster scoped init scripts are deployed.

Additionally, workspace level groups are deployed to manage access to cluster
policies and secret scopes on workspace level.

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
| databricks | >=1.37.0 |
| terraform | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| interactive\_cluster | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/cluster | 20240318.4 |
| secret\_scope\_dbrks | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/secret_scope_dbrks | 20240116.2 |
| secret\_scope\_kv | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/secret_scope_kv | 20240116.2 |
| sql\_warehouse | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/sql_warehouse | 20241105.2 |
| workspace\_cluster\_pools | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/cluster_pool | 20240116.2 |
| workspace\_interactive\_cluster\_policies | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/cluster_policy | 20240116.2 |
| workspace\_job\_cluster\_policies | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/cluster_policy | 20240116.2 |
| workspace\_logs | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/diagnostic_settings | 20240116.2 |

## Resources

| Name | Type |
|------|------|
| [databricks_group.workspace_groups](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/group) | resource |
| [databricks_group_member.workspace_groups](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/group_member) | resource |
| [databricks_workspace_binding.catalog](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_binding) | resource |
| [databricks_workspace_binding.data_replication_catalogs_elt](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_binding) | resource |
| [databricks_workspace_binding.data_replication_catalogs_srv](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_binding) | resource |
| [databricks_workspace_binding.data_replication_external_locations_elt](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_binding) | resource |
| [databricks_workspace_binding.data_replication_external_locations_srv](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_binding) | resource |
| [databricks_workspace_binding.external_locations](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_binding) | resource |
| [databricks_workspace_conf.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/workspace_conf) | resource |
| [azurerm_databricks_workspace.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/databricks_workspace) | data source |
| [azurerm_key_vault.secret_scope](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/key_vault) | data source |
| [azurerm_resource_group.wdap](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/resource_group) | data source |
| [databricks_group.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/group) | data source |
| [databricks_service_principal.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/service_principal) | data source |
| [databricks_user.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/user) | data source |
| [terraform_remote_state.dbrks_catalog](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.platform_infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the databricks workspace configs directory. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| databricks\_workspace\_groups | Workspace Groups deployed on this Workspace. |
| databricks\_workspace\_id | Workspace Id of the Azure Databricks Workspace. |
| databricks\_workspace\_name | Names of the Azure Databricks Workspace. |
| databricks\_workspace\_resource\_id | Azure resource Id of the Azure Databricks Workspace. |
| databricks\_workspace\_url | URL of the Azure Databricks Workspace. |
| secret\_scopes\_dbrks | Id of the external location secret scope |

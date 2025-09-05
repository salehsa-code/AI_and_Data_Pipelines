This is a terraform solution for the deployment of the Databricks Catalog
Configuration.

Permissions on Catalog Level are configured. Central external locations,
schemas and external volumes are created and permissions are configured.

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
| external\_locations | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_external_location | 20240318.4 |
| external\_volumes | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_external_volume | 20240318.4 |
| schemas | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_schema | 20240318.4 |

## Resources

| Name | Type |
|------|------|
| [azurerm_key_vault_secret.external_location_path](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/key_vault_secret) | resource |
| [databricks_file.init_script](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/file) | resource |
| [databricks_grants.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grants) | resource |
| [azurerm_databricks_workspace.provider](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/databricks_workspace) | data source |
| [terraform_remote_state.platform_infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the databricks workspace configs directory. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| databricks\_catalogs | Map of databricks catalogs with their names and owner groups. |
| external\_locations | Map of external location names. |
| init\_script\_files | Map of init script paths. |

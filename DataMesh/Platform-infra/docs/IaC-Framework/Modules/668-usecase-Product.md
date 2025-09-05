This is a solution for the deployment and configuration of usecase product
Unity Catalog objects.

New schemas are created and privileges on schema level are granted.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azurerm | ~>3 |
| databricks | >=1.37.0 |

## Providers

| Name | Version |
|------|---------|
| terraform | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| schema | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/uc_schema | 20241211.2 |

## Resources

| Name | Type |
|------|------|
| [terraform_remote_state.dbrks_catalog](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.dbrks_workspace](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the backend storage configs directory. | `string` | yes |

## Outputs

No outputs.

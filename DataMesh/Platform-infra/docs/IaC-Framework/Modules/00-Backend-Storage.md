This is a terraform solution for the deployment of the remote state storage.
It deploys the storage account and container that are used to store the
Terraform remote states of all deployments from this repository.

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| azurerm | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| storage\_account | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/storage_account | 20240306.2 |
| storage\_container | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/storage_container | v0.0.1 |

## Resources

| Name | Type |
|------|------|
| [azurerm_resource_group.wdap](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/resource_group) | data source |
| [azurerm_subnet.allowed_list](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/subnet) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the backend storage configs directory. | `string` | yes |

## Outputs

No outputs.

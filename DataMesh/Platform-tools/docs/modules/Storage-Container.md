# Storage Container

This module deploys a container on a storage account, including ACLs.

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| azurerm | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_storage_data_lake_gen2_filesystem.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_data_lake_gen2_filesystem) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| ace | A map of ACL entries. With the fields: `id`, Object Id of the AAD Object. `aad_name`, name of the AAD Object. `type` of the AAD Object (`user`, `service-principal` or `group`) entry. `permissions` maps the permissions that are granted in `access` and `default` scope. | <pre>map(object({<br>    id       = string<br>    aad_name = string<br>    type     = string<br>    permissions = object({<br>      access  = string<br>      default = string<br>    })<br>  }))</pre> | yes |
| name | Name of the storage container. | `string` | yes |
| storage\_account\_id | Id of the storage account where the storage container should be deployed. | `string` | yes |

## Outputs

No outputs.

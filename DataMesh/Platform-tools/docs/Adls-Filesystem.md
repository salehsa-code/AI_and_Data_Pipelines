# ADLS gen2 File System

This module deploys a filesystem (storage container) on an ADLS gen2 storage account, including ACLs, and creates directories inside the filesystem.

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
| [azurerm_storage_data_lake_gen2_path.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_data_lake_gen2_path) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| ace | A map of ACL entries. With the fields: `id`, Object Id of the AAD Object. `aad_name`, name of the AAD Object. `type` of the AAD Object (`user`, `service-principal` or `group`) entry. `permissions` maps the permissions that are granted in `access` and `default` scope. | <pre>map(object({<br>    id       = string<br>    aad_name = string<br>    type     = string<br>    permissions = object({<br>      access  = string<br>      default = string<br>    })<br>  }))</pre> | no |
| directories | A list of directories that are deployed on the storage container. Needs ADLS gen2 storage acount. | `set(string)` | no |
| name | Name of the storage container. | `string` | yes |
| storage\_account\_id | Id of the storage account where the storage container should be deployed. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| name | Name of the ADLS gen2 filesystem |

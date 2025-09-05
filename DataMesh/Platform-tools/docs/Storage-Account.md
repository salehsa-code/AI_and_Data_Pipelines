# Storage Account

This module deploys a storage account and potentially storage tables.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azurerm | >= 3.31.0 |

## Providers

| Name | Version |
|------|---------|
| azurerm | >= 3.31.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_management_lock.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/management_lock) | resource |
| [azurerm_storage_account.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_account) | resource |
| [azurerm_storage_table.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/storage_table) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| account\_replication\_type | Replication type, e.g. ZRS or LRS. | `string` | yes |
| account\_tier | Account tier, i.e. Standard or Premium. | `string` | yes |
| allowed\_subnets | List of allowed Subnet Resource Ids. | `set(string)` | yes |
| is\_hns\_enabled | Enable hierarchical file system. | `bool` | yes |
| location | Azure region, where the storage account is deployed. | `string` | yes |
| lock | If true, a `CanNotDelete` resource lock is added to the storage account. | `bool` | yes |
| name | Name of the storage account. | `string` | yes |
| private\_link\_access | List of allowed Private Link Resources. Specifying the `resource_id` and `tenant_id`. This includes granting access to specific resource instances. | <pre>list(object({<br>    endpoint_resource_id = string<br>    endpoint_tenant_id   = string<br>  }))</pre> | yes |
| resource\_group\_name | Name of the resource group, where the storage account is deployed. | `string` | yes |
| shared\_access\_key\_enabled | Allow usage of SAS Tokens (Shared Access Signature). | `bool` | no |
| storage\_tables | List of tables to be created in the storage account. | `set(string)` | no |
| tags | Key-value pairs that will be set as resource tags. | `map(string)` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | Id of the Storage account. |
| name | Name of the Storage account. |

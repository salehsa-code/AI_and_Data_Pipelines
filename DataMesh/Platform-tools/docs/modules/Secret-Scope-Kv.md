# Azure Key Vault Backed Secret Scope

This module deploys a Databricks backed Secret Scope.

The Secret Scope is managed by the `admins` local workspace group,
if other groups need manage permissions, these should be granted using the "CAN\_MANAGE" permission in the ACLs

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| databricks | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_secret_acl.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/secret_acl) | resource |
| [databricks_secret_scope.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/secret_scope) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| key\_vault\_id | Resource Id of the backend key vault. | `string` | yes |
| key\_vault\_uri | URI of the backend key vault. | `string` | yes |
| name | Name of the secret scope. | `string` | yes |
| permissions | Map of groups and their permissions on the secret scope. | `map(string)` | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Id of the Databricks backed secret scope. |
| name | Name of the Databricks backed secret scope. |

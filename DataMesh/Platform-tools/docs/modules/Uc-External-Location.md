# Unity Catalog - External Location

This module deploys an external location within a Databricks Catalog and assigns permissions to it.
The external location uses a storage credential to provide access to the specified path on the data lake.

## Requirements

| Name | Version |
|------|---------|
| databricks | >= 1.9.0 |

## Providers

| Name | Version |
|------|---------|
| databricks | >= 1.9.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_external_location.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/external_location) | resource |
| [databricks_grant.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grant) | resource |
| [databricks_grants.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grants) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| container\_name | Name of the target container of the external location. | `string` | yes |
| credential\_name | Name of the storage credential used for the external location. | `string` | yes |
| grant\_exclusive | Decides if grants should be granted exclusively i.e., using the `databricks_grants` resource, or federated i.e., using `databricks_grant` resources. | `bool` | no |
| grants | Map of groups and their permissions on the external location. | `map(set(string))` | yes |
| owner | Owner of the external locations. | `string` | yes |
| storage\_account\_name | Name of the target storage account of the external location. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| name | Name of the external location. |
| url | URL of the location on the data lake. |

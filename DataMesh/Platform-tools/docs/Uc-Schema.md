# Unity Catalog - Schema

This module deploys a schema within a Databricks catalog and assigns permissions to it.

## Requirements

| Name | Version |
|------|---------|
| databricks | >= 1.36.0 |

## Providers

| Name | Version |
|------|---------|
| databricks | >= 1.36.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_grant.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grant) | resource |
| [databricks_grants.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/grants) | resource |
| [databricks_schema.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/schema) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| catalog\_name | Name of the catalog where the schema is deployed. | `string` | yes |
| grant\_exclusive | Decides if grants should be granted exclusively i.e., using the `databricks_grants` resource, or federated i.e., using `databricks_grant` resources. | `bool` | no |
| grants | Map of groups and their permissions on the schema. | `map(set(string))` | yes |
| include\_name\_in\_path | Decides if the schema name should be added to the managed storage location. | `bool` | no |
| name | Name of the schema. | `string` | yes |
| owner | Owner of the schemas. | `string` | yes |
| path | Additional path on the storage container, where the schema is deployed. | `string` | no |
| uc\_container | Name of the catalog storage container. | `string` | yes |
| uc\_storage\_account | Name of the catalog storage account. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| name | Name of the schema. |

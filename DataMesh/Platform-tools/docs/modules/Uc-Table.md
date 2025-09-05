# Unity Catalog - Table

This module deploys permissions on a table or view in Unity Catalog.

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

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| catalog\_name | Name of the catalog the tables/views live in. | `string` | yes |
| grants | Map, where they key is the Table name and the value is a list of privileges. | `map(set(string))` | yes |
| principal | Name of the Principal, e.g. AD-Group name. | `string` | yes |
| schema\_name | Name of the schema the tables/views live in. | `string` | yes |

## Outputs

No outputs.

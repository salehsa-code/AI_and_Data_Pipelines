# Databricks Directory

This module deploys a Databricks directory and assigns permissions to it.

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
| [databricks_directory.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/directory) | resource |
| [databricks_permissions.folder_usage](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permissions) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| groups | Map of groups and their permissions on the Databricks directory. | `map(string)` | yes |
| path | Path of the Databricks directory. | `string` | yes |

## Outputs

No outputs.

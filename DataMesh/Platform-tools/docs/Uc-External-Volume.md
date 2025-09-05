# Unity Catalog - External Volume

This module deploys an external volume inside a given schema in a Databricks
catalog and assigns permissions to it.

Grants can be set either exclusively, meaning that this module will overwrite
all existing grants and replace them with the grants configured here, or
federated, meaning that this module will only add or remove the grants managed
in it's scope, but leave other grants untouched.

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
| [databricks_volume.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/volume) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| catalog\_name | Name of the catalog where the external volume is deployed. | `string` | yes |
| grant\_exclusive | Decides if grants should be granted exclusively i.e., using the `databricks_grants` resource, or federated i.e., using `databricks_grant` resources. | `bool` | no |
| grants | Map of groups and their permissions on the external volume. | `map(set(string))` | yes |
| name | Name of the external volume. | `string` | yes |
| owner | Owner of the external volume. | `string` | yes |
| schema\_name | Name of the schema where the external volume is deployed. | `string` | yes |
| storage\_location | Location inside an external location. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| name | Name of the external volume. |
| path | Path of the external volume. |
| storage\_location | Storage location of the external volume. |

# Cluster Pool

This module deploys a cluster pool to the Databricks workspace and
set permissions accordingly.

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
| [databricks_instance_pool.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/instance_pool) | resource |
| [databricks_permissions.pool_usage](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permissions) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| autoterminate\_minutes | The number of minutes before idle instances are auto-terminated. | `number` | yes |
| enable\_elastic\_disk | Flag to enable or disable elastic disk. | `bool` | yes |
| groups | Display Names of groups with 'CAN\_ATTACH\_TO' permission on the pool. | `set(string)` | yes |
| max\_capacity | The maximum capacity of the instance pool. | `number` | no |
| min\_idle\_instances | The minimum number of idle instances. | `number` | yes |
| node\_type\_id | The type of node to be used in the instance pool. | `string` | yes |
| pool\_name | The name of the instance pool | `string` | yes |
| preloaded\_spark\_versions | Set of preloaded Spark versions, with at most one entry. | `set(string)` | yes |
| spot | Flag to enable or disable spot instances. | `bool` | yes |

## Outputs

| Name | Description |
|------|-------------|
| node\_type\_id | n/a |
| pool\_id | n/a |

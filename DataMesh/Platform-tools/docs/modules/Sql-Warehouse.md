# SQL Warehouse

This module deploys a SQL warehouse and manages permissions on the warehouse.

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
| [databricks_permissions.endpoint_usage](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permissions) | resource |
| [databricks_sql_endpoint.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/sql_endpoint) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| auto\_stop\_mins | Minutes until idle SQL warehouse stops. | `number` | yes |
| cluster\_size | Size of the clusters allocated to the SQL warehouse. | `string` | yes |
| enable\_photon | Enable Photon on the SQL warehouse. | `bool` | yes |
| max\_num\_clusters | Maximum number of clusters available when SQL warehouse is runnning. | `number` | yes |
| min\_num\_clusters | Minimum number of clusters available when SQL warehouse is runnning. | `number` | yes |
| name | Name of the SQL warehouse. | `string` | yes |
| permissions | Map of group names and their permissions. | `map(string)` | yes |
| spot\_instance\_policy | The spot policy to use for allocating instances to clusters: 'COST\_OPTIMIZED' or 'RELIABILITY\_OPTIMIZED'. | `string` | yes |
| tags | Key value pairs of custom tags for all SQL warehouse resources. | `map(string)` | yes |
| warehouse\_type | SQL warehouse type. 'PRO', 'CLASSIC', or 'SERVERLESS' | `string` | yes |

## Outputs

No outputs.

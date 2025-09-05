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
| [databricks_cluster.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/cluster) | resource |
| [databricks_permissions.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permissions) | resource |
| [databricks_node_type.smallest](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/node_type) | data source |
| [databricks_spark_version.latest_lts](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/spark_version) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| autoscale | The autoscale configuration for the Databricks cluster, including 'max\_workers' and 'min\_workers'. | `object({ min_workers = optional(number), max_workers = number })` | no |
| autotermination\_minutes | The autotermination minutes for the Databricks cluster | `number` | no |
| azure\_attributes | The azure attributes for the Databricks cluster. | <pre>object({<br>    availability       = string<br>    first_on_demand    = number<br>    spot_bid_max_price = number<br>  })</pre> | no |
| cluster\_name | The name of the Databricks cluster | `string` | yes |
| custom\_tags | The custom tags for the Databricks cluster | `map(string)` | no |
| data\_security\_mode | Sets the security features of the cluster | `string` | no |
| driver\_node\_type\_id | The driver node type id for the Databricks cluster | `string` | no |
| enable\_elastic\_disk | Enable elastic disk for the Databricks cluster | `bool` | yes |
| init\_scripts | List of init scripts to pass to the cluster. Each script is represented as a map with either a 'dbfs' or 'file' object. E.g., [ { dbfs = { destination = 'dbfs:/databricks/init-script.sh' } }, { file = { destination = 'file:/local/path/to/init-script2.sh' } }] | `list(map(any))` | no |
| node\_type\_id | The node type id for the Databricks cluster | `string` | no |
| num\_workers | The number of workers for the Databricks cluster | `number` | no |
| permissions | Map of permissions, with a key of groupname and a value of permission. Permission can be any of 'CAN\_ATTACH\_TO', 'CAN\_RESTART' or 'CAN\_MANAGE'. The deploying user will always get 'CAN\_MANAGE' permissions. | `map(string)` | no |
| pool\_id | Id of the pool to draw nodes from for this clusters. | `string` | yes |
| spark\_conf | The Spark configuration for the Databricks cluster | `map(string)` | yes |
| spark\_env\_vars | The Spark environment variables for the Databricks cluster | `map(string)` | no |
| spark\_version | The Spark version of the Databricks cluster | `string` | yes |
| ssh\_public\_keys | The SSH public keys for the Databricks cluster | `list(string)` | no |

## Outputs

No outputs.

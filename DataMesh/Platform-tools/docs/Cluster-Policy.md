# Cluster Policy

This module deploys a cluster policy to the Databricks workspace and assigns "CAN\_USE" permissions to it.

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
| [databricks_cluster_policy.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/cluster_policy) | resource |
| [databricks_permissions.policy_usage](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/permissions) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| groups | List of groups that get the `CAN_USE` permission on this cluter policy. | `set(string)` | yes |
| policy\_definition | Cluster policies in JSON format. | `string` | yes |
| policy\_name | Name of the cluster policy. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Id of the cluster policy. |

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
| [databricks_job.this](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/job) | resource |
| [databricks_clusters.selected_ids](https://registry.terraform.io/providers/databricks/databricks/latest/docs/data-sources/clusters) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| job | Job module parameters. | <pre>object({<br>    name         = string<br>    tasks        = map(object({ notebook_path = string }))<br>    cluster_name = string<br>  })</pre> | yes |

## Outputs

| Name | Description |
|------|-------------|
| job\_url | n/a |

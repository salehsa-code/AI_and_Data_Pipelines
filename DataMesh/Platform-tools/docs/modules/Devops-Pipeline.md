# DevOps Pipeline

This module deploys a DevOps pipeline using an existing YAML definition file in a DevOps repository.
Pipeline authorizations can be granted and permissions on the pipeline can be set.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azuredevops | >=0.10.0 |

## Providers

| Name | Version |
|------|---------|
| azuredevops | >=0.10.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azuredevops_build_definition.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/build_definition) | resource |
| [azuredevops_build_definition_permissions.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/build_definition_permissions) | resource |
| [azuredevops_pipeline_authorization.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/pipeline_authorization) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| name | Name of the pipeline. | `string` | yes |
| path | Path of the pipeline. | `string` | yes |
| permissions | Map of permissions on the pipeline: group -> {id, list of allowed actions}. For each action listed, 'Allow' will be set on this pipeline. | <pre>map(object({<br>    id          = string<br>    permissions = set(string)<br>  }))</pre> | yes |
| pipeline\_authorizations | Map of pipeline authorizations: name -> {id, type}. This pipeline will be authorized on each object in this map. Supported types are 'endpoint', 'queue', 'variablegroup', 'environment', 'repository'. | <pre>map(object({<br>    id   = string<br>    type = string<br>  }))</pre> | yes |
| project\_id | Id of the DevOps project. | `string` | yes |
| repo\_id | Id of the Repository, where the pipeline definition is located. | `string` | yes |
| yaml\_path | Path to the pipeline definition YAML file. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Id of the pipeline. |

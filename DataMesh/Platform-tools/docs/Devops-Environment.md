# DevOps Environment

This module deploys a DevOps environment and sets permissions on the environment.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azuredevops | >=0.10.0 |
| restapi | >=1.18.0 |

## Providers

| Name | Version |
|------|---------|
| azuredevops | >=0.10.0 |
| restapi | >=1.18.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azuredevops_environment.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/environment) | resource |
| [restapi_object.environment_permission_project_admin](https://registry.terraform.io/providers/Mastercard/restapi/latest/docs/resources/object) | resource |
| [azuredevops_group.project_administrators](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/group) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| name | Name of the environment. | `string` | yes |
| project\_id | Id of the DevOps project. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Id of the environment. |

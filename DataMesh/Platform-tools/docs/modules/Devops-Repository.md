# DevOps Repository

This module deploys a DevOps repository and adds initial files to it.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azuredevops | >=0.6.0 |

## Providers

| Name | Version |
|------|---------|
| azuredevops | >=0.6.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azuredevops_git_permissions.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_permissions) | resource |
| [azuredevops_git_repository.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository) | resource |
| [azuredevops_git_repository_file.repository_files](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| name | Name of the DevOps Repository. | `string` | yes |
| permissions | Map of permissions on the repository: group -> {id, list of allowed actions}. For each action listed, 'Allow' will be set on this repository. | <pre>map(object({<br>    id          = string<br>    permissions = set(string)<br>  }))</pre> | yes |
| project\_id | Id of the DevOps project. | `string` | yes |
| repository\_files | Map of repository files with file name as the key and an object with content and target\_location attributes as the value. | <pre>map(object({<br>    content         = string<br>    target_location = string<br>  }))</pre> | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Id of the data product repository. |

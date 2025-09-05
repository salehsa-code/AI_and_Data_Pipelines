# Data Product Repository

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azuredevops | >=0.6.0 |
| restapi | >=1.18.0 |

## Providers

| Name | Version |
|------|---------|
| azuredevops | >=0.6.0 |
| restapi | >=1.18.0 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azuredevops_build_definition.pipeline](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/build_definition) | resource |
| [azuredevops_build_definition_permissions.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/build_definition_permissions) | resource |
| [azuredevops_environment.dtap](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/environment) | resource |
| [azuredevops_git_permissions.core](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_permissions) | resource |
| [azuredevops_git_permissions.data_product](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_permissions) | resource |
| [azuredevops_git_repository.data_product](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository) | resource |
| [azuredevops_git_repository_branch.data_product](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_branch) | resource |
| [azuredevops_git_repository_file.backend_config](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_git_repository_file.data_product_config](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_git_repository_file.pipeline](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_git_repository_file.remote_config](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_git_repository_file.repository_files](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_group.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/group) | resource |
| [restapi_object.environment_permission_project_admin](https://registry.terraform.io/providers/Mastercard/restapi/latest/docs/resources/object) | resource |
| [azuredevops_group.project_administrators](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/group) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| backend\_config | Backend config for each environment, including the file content, the terraform solution and environment. | <pre>map(object({<br>    content            = string<br>    terraform_solution = string<br>    environment        = string<br>    })<br>  )</pre> | yes |
| data\_product\_config\_content | Content of the data product config file in the infra repository for each environment. | `map(string)` | yes |
| data\_product\_name | Name of the Data Product. | `string` | yes |
| data\_product\_short\_name | A brief, human-readable identifier for the Data Product. Must be no longer than 12 characters. | `string` | yes |
| environments | Environments that are deployed for the data product. | `set(string)` | yes |
| group\_pipeline\_permissions | A list of objects defining the permissions for each group and pipeline combination. | <pre>map(object({<br>    group_key    = string<br>    pipeline_key = string<br>    permissions  = list(string)<br>  }))</pre> | yes |
| groups | n/a | <pre>map(object({<br>    pipeline     = set(string)<br>    repositories = map(set(string))<br>  }))</pre> | yes |
| pipelines | Map of pipeline objects with pipeline\_name as the key and an object with pipeline\_content and pipeline\_path attributes as the value. | <pre>map(object({<br>    content     = string<br>    devops_path = string<br>    yaml_path   = string<br>  }))</pre> | yes |
| project\_id | Id of the DevOps project. | `string` | yes |
| remote\_config\_files | Config file names and content deployed to the data product repository. | <pre>map(object({<br>    name        = string<br>    environment = string<br>    content     = string<br>  }))</pre> | yes |
| repo\_ids | Names and Ids of the Wind DataAnalytics Platform core repositories. | `map(string)` | yes |
| repository\_files | Map of repository files with file name as the key and an object with content and target\_location attributes as the value. | <pre>map(object({<br>    content         = string<br>    target_location = string<br>  }))</pre> | yes |

## Outputs

| Name | Description |
|------|-------------|
| environments | Map of the environments. |
| id | Id of the data product repository. |

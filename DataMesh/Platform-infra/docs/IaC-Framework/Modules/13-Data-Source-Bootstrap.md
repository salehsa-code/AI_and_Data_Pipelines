This is a terraform solution for the depoloyment of the DevOps resources for a
new data product.

A new repository for the data product is created and filled with default
configuration files for the actual deployment of the data product.

DevOps groups for the data product are created and their permissions to the
data product and infrastructure repositories are set.

In the winddata-platfrom-infra repositry, a new branch is created with the
pipeline definition and configuration to deploy the data product.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azuredevops | >=0.6.0 |
| azurerm | >= 3.31.0 |

## Providers

| Name | Version |
|------|---------|
| azuredevops | >=0.6.0 |

## Modules

| Name | Source | Version |
|------|--------|---------|
| devops\_pipeline | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/devops_pipeline | 20231129.3 |

## Resources

| Name | Type |
|------|------|
| [azuredevops_git_repository_branch.infra](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_branch) | resource |
| [azuredevops_git_repository_branch.sources](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_branch) | resource |
| [azuredevops_git_repository_file.backend_config](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_git_repository_file.pipelines](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_git_repository_file.remote_config](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/git_repository_file) | resource |
| [azuredevops_agent_queue.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/agent_queue) | data source |
| [azuredevops_git_repository.core](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/git_repository) | data source |
| [azuredevops_group.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/group) | data source |
| [azuredevops_project.wind](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/project) | data source |
| [azuredevops_serviceendpoint_azurerm.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/serviceendpoint_azurerm) | data source |
| [azuredevops_variable_group.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/variable_group) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the backend storage configs directory. | `string` | yes |
| pat | DevOps Personal Access Token used for the deployment. | `string` | yes |

## Outputs

No outputs.

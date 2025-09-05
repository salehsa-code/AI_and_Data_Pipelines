This is a terraform solution for the configuration of the core Azure DevOps repositories.
It configures branch policies & sets allowed approvers for pull requests.

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

## Modules

| Name | Source | Version |
|------|--------|---------|
| auto\_reviewers | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/devops_build_validation_approvers | 20230919.2 |
| devops\_environment | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/devops_environment | 20231129.3 |
| devops\_repository | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/devops_repository | 20231129.3 |

## Resources

| Name | Type |
|------|------|
| [azuredevops_branch_policy_build_validation.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/branch_policy_build_validation) | resource |
| [azuredevops_branch_policy_comment_resolution.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/branch_policy_comment_resolution) | resource |
| [azuredevops_branch_policy_merge_types.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/branch_policy_merge_types) | resource |
| [azuredevops_branch_policy_min_reviewers.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/branch_policy_min_reviewers) | resource |
| [azuredevops_branch_policy_work_item_linking.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/branch_policy_work_item_linking) | resource |
| [azuredevops_build_definition.build_validation](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/build_definition) | data source |
| [azuredevops_group.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/group) | data source |
| [azuredevops_project.wind](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/project) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the core\_repositories configs directory. | `string` | yes |
| pat | AAD or DevOps personal access token. | `string` | yes |

## Outputs

No outputs.

# DevOps - Build Validation: Auto Reviewers

This module deploys a branch policy to add auto reviewers to a Pull Request.

## Requirements

| Name | Version |
|------|---------|
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
| [azuredevops_branch_policy_auto_reviewers.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/resources/branch_policy_auto_reviewers) | resource |
| [azuredevops_group.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/group) | data source |
| [azuredevops_users.this](https://registry.terraform.io/providers/microsoft/azuredevops/latest/docs/data-sources/users) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| blocking | This branch policy is blocking the PR. | `bool` | yes |
| enabled | This branch policy is enabled. | `bool` | yes |
| match\_type | The match type to use when applying the policy. Supported values are Exact, Prefix or DefaultBranch. | `string` | yes |
| project\_id | Project Id. | `string` | yes |
| repository\_id | Repository Id. | `string` | yes |
| respository\_ref | Repository Ref, e.g., Branch 'refs/heads/main'. | `string` | yes |
| reviewer\_groups | Set of Groups that are added as auto reviewers to PRs. Notice that Teams are Groups aswell. | `set(string)` | yes |
| reviewer\_users | Set of users that are added as auto reviewers to PRs. | `set(string)` | yes |
| submitter\_can\_vote | The submitter of the PR can approve it. | `bool` | yes |

## Outputs

No outputs.

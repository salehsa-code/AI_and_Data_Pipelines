# Terraform IaC Framework contributing guide

 This guide is intended for developers and contributors to the Terraform IaC
 Framework.

## Pull Request process

Changes to the framework should reflect a work item from the Data Kong
backlog. Make sure to link the work item when creating the PR.

Every pull request has to be reviewed and approved by at least one **other**
developer. Follow the [Review Checklist](#review-checklist) when reviewing a PR.

### Create a Pull Request

Follow the instructions in the PR template.

### Review Checklist

Reviewers should use this checklist to help maintain a clean codebase that
follows established best practices of the Terraform IaC framework.

#### Review the changes made to the codebase

- Does the code work?
- Is all the code easily understood?
- Are all relevant config files created / updated?
- Do all modules reference the correct [version tag](#modules)?
- Are good names used for resources, modules, data sources and locals?
- Does the code have correct linting?
- Is there any commented out code that should be removed?
- Is there any redundant or duplicate code?

#### Review the documentation

- Is the PR description easily understood?
- Is the documentation up to date?

#### Review the CI pipeline results

- Is the Terraform code validated?
- Are all Checkov tests passed?
- Does the proposed Terraform plan match the expected changes?

### Release

In this Repo we aim to enable true continuous integration. We follow a "Scaled
Trunk-based" or "Feature Flow" branching strategy:

- **Short-lived feature branches** that merge into main
- **review and testing** as part of PR to main
- main branch is **always deployable**
- optional: deployment to production from regular **release branches** (extra layer of protection for PRD)

::: mermaid

gitGraph:
  commit id:"1"
  commit id:"2"
  branch feature/1-branch
  checkout feature/1-branch
  commit id:"4"
  checkout main
  commit id:"3"
  branch feature/2-branch
  checkout feature/1-branch
  commit type: HIGHLIGHT id:"1-branch PR review"
  commit id:"5"
  checkout main
  merge feature/1-branch id:"8"
  checkout feature/2-branch
  commit id:"6"
  commit id:"7"
  commit type: HIGHLIGHT id:"2-branch PR review"
  checkout main
  merge feature/2-branch id:"9"
  commit id:"10"
:::

## Developer Guidelines

This section is a collection of guidelines and tips to help developers
contributing to the Terraform Framework.

### Solutions

The Terraform code for new solutions should be added into a separate folder in
the `terraform` directory. The solution should only use one variable called
`configs_path`, which is the path to the configs directory, where the config
`yaml` files are located. This ensures that the DevOps pipeline templates work
and ensures that all necessary deployment metadata is located in one location.

### Modules

If a deployment of one component of the solution requires more than one
resource, it should be collected into a separate Terraform module, e.g. the
`uc_external_location` module encapsulates the external location module and the
set of permissions on that external location. This improves the readability of
the Terraform code and allows to quickly identify the single components of the
solution. Avoid nesting modules in other modules.

It can be convenient to develop new modules locally to avoid having to update
two repositories simultaneously. However, before merging into main, local
modules should be migrated to the tools repository, to allow reusability of
modules in other repositories in the project.

Version tags are maintained in the
[wind-da-platform-tools](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-tools)
repository that should be used to reference a specific version of a module. The
tag is specified in the source field of a module using the `ref` argument in the
source URL, e.g.:

```hcl
module "my_module" {
  source = "git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/my_module?ref=20230302.1"
  # (module arguments)
}
```

In this example, the version with the tag `20230302.1` will be used.

Similarly, you can reference a remote branch. This can be useful, when changing
or updating an existing module in the
[wind-da-platform-tools](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-tools)
repository. When merging to main, these references should be replaced with
proper version tags!

### Naming Conventions

This section collects the naming conventions used in the IaC framework and the
Wind Data Platform resources. As a general guideline, the [VDP naming
conventions](https://vattenfall.sharepoint.com/sites/VDPAzureWiki/SitePages/Vattenfall-Naming-Conventions.aspx?web=1)
should be followed. In addition, we use the following conventions:

| Type | Naming Convention | Example |
|:--|:--|:--|
| Terraform Variables | snake_case | my_var |
| Databricks Secrets | train-case | my-secret |
| Data Product Names | snake_case | my_data_product |
| Data Product Short-Names | snake_case (max. 12 characters) | data_prdct |
| Data Source Names | snake_case | my_data_source |
| Data Source Short-Names | snake_case (max. 12 characters) | data_src |

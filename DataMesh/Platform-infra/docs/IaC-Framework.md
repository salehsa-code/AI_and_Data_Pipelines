# Wind Data and Analytics Platform Terraform Framework

## Content

1. [General Description](IaC-Framework) (this document)
2. [IaC-Framework User Guide](iac-framework/IaC-Framework-User-Guide.md)
3. [Solutions](iac-framework/Solutions.md)

## Description

We decided to not implement a single Terraform configuration for the whole of
our infrastructure. Instead we are splitting it in multilple configurations,
refered to as Terraform *solutions*. Each solution covers a logical part of the
infrastructure, e.g. the Databricks Workspace Configuration
(`12-workspace_config`) or a Data Product (`21-data_product`). This approach
allows us to make changes to certain parts of the infrastucture without the risk
of breaking the configuration of other parts.

A solution consists of several Terraform modules that break down the
infrastructure into separate components, e.g. a storage account and storage
containers. The modules are sourced from the
[wind-da-platform-tools](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-tools)
repository and imported into the solution as `git` sources. Using this approach
enables reusability of modules in deployments accross different repositories
within the Wind Data and Analytics Platform Project.

The solutions are deployed via DevOps pipelines, following common pipeline
templates for the preparation, validation, build, and deployment steps. Each
solution is configured using `yaml` files and separate configurations for each
project environment need to be set. More detail on the
[Solutions](iac-framework/Solutions)  and their configuration can be found in
the dedicated sections.

![image](.img/solutions.drawio.png)

## Terraform state management

Terraform stores the current state of the infrastructure deployment in `JSON`
format. It is highly recommended to store the state remotely. The recommended
backend for remote state on Azure is blob storage ([Azure
documentation](https://learn.microsoft.com/en-us/azure/developer/terraform/store-state-in-azure-storage?tabs=azure-cli)).

Since each solution will have its own state, we include a
`<solution_name>.tfbackend` file with the backend configuration within the
config directory of each solution. Refere to the
[Configuration](./iac-framework/Solutions.md#terraform-backend-config)
section for details on how to use these files.

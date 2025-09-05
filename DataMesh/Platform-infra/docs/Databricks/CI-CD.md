# Databricks CI/CD

## Content

- [Databricks CI/CD](#databricks-cicd)
  - [Content](#content)
  - [How-To Deploy Jobs](#how-to-deploy-jobs)
    - [Job Validation](#job-validation)
  - [Configuration of a Job](#configuration-of-a-job)
  - [How-to Deploy a Data Contract](#how-to-deploy-a-data-contract)
  - [Table Deployments](#table-deployments)

## How-To Deploy Jobs

The deployment of Databricks Jobs is performed using [Databricks Asset
Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/).
A pipeline for the automatic deployment of Databricks Asset Bundles is located
at the [Azure
Pipelines](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_build?view=folders)
folder of your data product. Simply navigate to the `data_products` folder and
search for the subfolder of your data product. In this subfolder, the Asset
Bundles pipeline is stored under the name
`<data_product_name>-databricks_asset_bundles`. For example, the deployment
pipeline for operations data product is located at
`data_products/operations/operations-databricks_asset_bundles`.

Databricks Asset Bundles are stored in the data product repository under the
`databricks/jobs` folder. The Asset Bundles are configured using the
`databricks/databricks.yml` config file. The Deployment Pipeline will
automatically check out the Databricks Asset Bundles from that location.

The Asset Bundles Deployment Pipeline can be steered using parameters. You can
choose which environments to deploy to using the "Deploy to ENV" buttons.
Additionally, you can specify a branch to use as a source of the asset bundle
under the "Branch to check out" parameter. For example setting the branch to
`feature/branch` will try to check out this feature branch from the data product
repository and deploy the Asset Bundles defined there.

## Configuration of a Job

The general Asset Bundle configuration is located under
`databricks/databricks.yml` in the data product repository. Below is an example
configuration for an asset bundle. It can be used to deploy the jobs stored in
`databricks/jobs` to the DEV and PRD workspaces.

```yaml
bundle:
  name: example
  # Don't change below config
  terraform:
    exec_path: terraform

# Paths to include in the Asset bundle. The path is relative to the path of this file.
include:
  - jobs/*

# Target Environments
targets:
  dev:
    # mode - development or production. Should be set always to production mode.
    mode: production
    default: true
    # workspace where the DAB is deployed
    workspace:
      host: https://adb-4781705659802609.9.azuredatabricks.net

  prd:
    mode: production
    workspace:
      host: https://adb-1554493548803385.5.azuredatabricks.net
```

Jobs should be defined using the [YAML
configuration](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/settings#job)
that can be copied from the Databricks Web Application by going to a Job and
click on the "Switch to code version (YAML)" option in the ellipsis menu.

Variables can be used to look up parameters that change between workspaces like
cluster pool IDs or policy IDs.

Example:

```yaml
variables:
  pool_wdap_general_s:
    description: wdap-pool-general-s
    lookup:
      instance_pool: "wdap-pool-general-s"
  pool_wdap-memory-s:
    description: wdap-pool-memory-s
    lookup:
      instance_pool: "wdap-pool-memory-s"
  policy_job_cluster_s:
    description: job_cluster_policy_s
    lookup:
      cluster_policy: "Job Cluster S"

resources:
  jobs:
    dummy_job:
      name: dummy_job
      schedule:
        quartz_cron_expression: 0 0 12 * * ?
        timezone_id: UTC
        pause_status: UNPAUSED
      max_concurrent_runs: 1
      tasks:
        - task_key: dummy_task_1
          notebook_task:
            notebook_path: asset-bundles/notebooks/dummy_notebook
            base_parameters:
              param_one: "hello world!"
            source: GIT
          job_cluster_key: dummy_job_cluster
          libraries:
            - pypi:
                package: windef==0.4.2
        - task_key: dummy_task_2
          depends_on:
            - task_key: dummy_task_1
          notebook_task:
            notebook_path: asset-bundles/notebooks/dummy_notebook
            base_parameters:
              param_one: "good bye!"
            source: GIT
          job_cluster_key: dummy_job_cluster
          libraries:
            - pypi:
                package: windef==0.4.2
      job_clusters:
        - job_cluster_key: dummy_job_cluster
          new_cluster:
            spark_version: 14.3.x-scala2.12
            instance_pool_id: ${var.pool_wdap_general_s}
            policy_id: ${var.policy_job_cluster_s}
            driver_instance_pool_id: ${var.pool_wdap-memory-s}
            data_security_mode: SINGLE_USER
            runtime_engine: STANDARD
            num_workers: 1
      git_source:
        git_url: https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/dlh_jobs
        git_provider: azureDevOpsServices
        git_branch: main
      tags:
        group: dummy
      queue:
        enabled: true
      parameters:
        - name: log_to_azure
          default: "False"
      permissions:
        - user_name: bka27@eur.corp.vattenfall.com
          level: CAN_MANAGE
```

### Use Dynamic Source Branch

The pipeline allows to specify a branch to use as a source of the asset bundle.
This information can be leveraged in the Deployment of the Databricks Asset
Bundle. The source branch will pe passed as a variable called `git_branch` to
the Databricks CLI when deploying the Asset Bundle to the DEV or TST
environments. You can use this variable to set the git source branch in your
Asset Bundle:

```yaml
variables:
  git_branch:
    description: Branch used in git source.
    default: main

resources:
  jobs:
    my_job:
      # [...]
      git_source:
        git_url: https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/dlh_jobs
        git_provider: azureDevOpsServices
        git_branch: ${var.git_branch}
```


## How-to Deploy a Data Contract

For deploying the jobs associated with a data product, you simply need to locate
the relevant pipeline and execute it. You can find the corresponding deployment
pipeline under
`data-propducts/<your_product_name>/<your_product_name>-data_contract`

- `Branch Ref`: This parameter determines the branch / tag from which the data
  contract will be deployed. For example, using `main` will deploy all jobs
  present in the main branch at the time.
- `Deploy to [DEV|TST|ACC|PRD]`: This parameter decides the environment to which
  the data contract will be deployed.

## Table Deployments

Deploying explicit table definitions between environments can be complicated due to the need for
`ALTER TABLE` statements for changes like adding columns or altering data types. We aim to avoid
this complexity.

Instead, we utilize the Data Engineering Framework to generate DDLs from the data contract YAML
files, which must be up-to-date at all times. This allows us to make dynamic changes within the ETL
pipeline, enabling deployment between environments without the use of `ALTER TABLE` statements.

We will establish a regular process that ensures there's no inconsistency between the data contract
and what's deployed in the Unity Catalog. This way, we maintain the advantages of explicit table
definitions while simplifying the deployment process.

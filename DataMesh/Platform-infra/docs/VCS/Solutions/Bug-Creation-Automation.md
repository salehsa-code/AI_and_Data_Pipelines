# Bug Creation Automation

## Problem Description

When a Workflow in Databricks fails, it is important to create a bug in our
backlog to prevent it from going unnoticed. This process is manual and
time-consuming.

> Despite its name, this automation is not responsible for creating bugs in our
> code, but rather for automating the process of creating bugs in our backlog.

## Architecture

This solution runs as a cronjob on our VCS cluster. It is triggered on a day at
2am - if required, this could be configured on a per-tag level. When it runs, it
checks the status of all Workflows in Databricks since the last time it ran. If
it finds any failed Workflows, it creates a bug in our backlog with the details
of the failed Workflow. It adds the failed job runs with details as comment to
the work item. If the work item had the status "Done" it will be reopened.

The last time the solution ran is stored in an Azure Table, because we're
lacking permissions to write to the VCS cluster's filesystem or create other
persistent storage there. If no last run time is found, the solution will create
a new entry in the Azure Table with the current time and look back 24 hours in
the current run.

The solution scans for jobs with the defined tags in the Databricks instance,
the combination of tags is identifies the cronjob-instance and is therefore
unique per environment.

## How to Use

The solution can easily be extended to deploy more cronjobs for different tags.
This can be done by adding a new entry to the generators list in
`k8s\apps\<env>\bug-creation-automation\application-set.yml`

Here is a detailed description on the generator configuration:

| Parameter                         | Description                                                                                                                                                                                                                          |
| --------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **suffix**                        | Defines the suffix of the cronjob name                                                                                                                                                                                               |
| **devopsOrganization**            | Name of the organization in Azure DevOps that contains the Backlog                                                                                                                                                                   |
| **devopsProject**                 | Name of the project in Azure DevOps that contains the Backlog                                                                                                                                                                        |
| **devopsTeam**                    | Name of the team in Azure DevOps that contains the Backlog                                                                                                                                                                           |
| **devopsAreaPath**                | Area path in Azure DevOps where the bugs should be created                                                                                                                                                                           |
| **databricksWorkspace**           | Name of the Databricks workspace to scan for failed Workflows                                                                                                                                                                        |
| **databricksAppId**               | Service principal ID for the Databricks workspace, this is used to authenticate with the Databricks API and the SP needs at least `CAN_VIEW` permissions on the Jobs                                                                 |
| **databricksAppSecretSecretName** | Name of the secret in the `vap2-[dev\|prd]-argocd-kv` that contains the Service principal secret. Mind, that the secret must also be created in the environments secret store (see `k8s\apps\<env>\secret-store\secrets-store.yml`). |
| **databricksJobTags**             | List of tags to filter the Databricks jobs by. Must be in the format `key1:value1\|key2:value2`                                                                                                                                      |

In Azure DevOps the solution authenticates using the WDAP managed identity
vap2-dev-wind-devops-uami `5a5594d0-c5ed-4c46-99b5-6976c620ea2c`. The same MI is
used to authenticate with DEV, TST, ACC and PRD to save licenses for Azure
DevOps and because Azure DevOps does not really have a concept of environments.

# Azure Infrastructure Monitoring

In this section, the monitoring of the Azure infrastructure for the Wind Data and
Analytics Platform is described.

Default Azure logs and metrics are collected by creating diagnostic settings for
the monitored resources. These diagnostic settings are automatically deployed as
part of the IaC framework.

## Storage Accounts

For the data lake storage accounts, as well as the Unity Catalog metadata
storage account, diagnostic settings are deployed that collect logs and metrics
for the blob service endpoint. The following logs and metrics are collected:

| Name | Description |
| --- | --- |
| `StorageRead` | Read operation on objects. |
| `StorageWrite` |  Write operations on objects. |
| `StorageDelete` | Delete operations on objects. |

![datalke-monitoring](../.img/platform-observability/azure_datalake_monitoring.drawio.png)

## Azure Databricks Workspace Audit Logs

The Azure Databricks Workspaces are configured to expose verbose audit logs.
Diagnostic Settings are deployed to the workspaces to send audit logs to the
common Log Analytics Workspace. The following logs are collected:

| Name | Description |
| --- | --- |
| `Clusters` | Events related to clusters. |
| `DatabricksSQL` | Events related to Databricks SQL use. |
| `InstancePools` | Events related to node pools. |
| `Jobs` | Events related to jobs. |
| `MLFlowExperiment` | Events related to ML Flow experiments. |
| `Notebook` | Events related to notebooks. |
| `Repos` | Events related to Databricks Repos. |
| `Secrets` | Events related to secrets. |
| `Workspace`|  Events related to workspaces. |


![databricks-workspace-monitoring](../.img/platform-observability/azure_databricks_monitoring.drawio.png)

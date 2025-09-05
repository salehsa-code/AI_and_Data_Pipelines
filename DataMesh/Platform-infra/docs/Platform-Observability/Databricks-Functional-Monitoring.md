# Databricks Functional Monitoring

In this section, the monitoring of the Databricks ETL jobs for the Wind Data and
Analytics Platform is described.

## Workspace Log

Workspace audit logs are gathered from the Databricks Workspace via diagnostic
settings (see [Databricks Workspace Audit
Logs](./Azure-Infrastructure-Monitoring.md#azure-databricks-workspace-audit-logs)).
These logs provide crucial information about the status of ETL jobs running on
the platform.

### Job logs

The Databricks Job events contain information about specific job actions. In the
following, a description of the some useful job events is given. A full
description can be found
[here](https://learn.microsoft.com/en-us/azure/databricks/administration-guide/account-settings/audit-logs#--job-events).

| Action | Description | Parameters |
| --- | --- | --- |
| `runSucceeded` | job run ended successfully | `idInJob`, `jobId`, `jobTriggerType`, `orgId`, `runId`, `jobClusterType`, `jobTaskType`, `jobTerminalState`, `runCreatorUserName` |
| `runFailed` | job run ended with errors | `idInJob`, `jobId`, `jobTriggerType`, `orgId`, `runId`, `jobClusterType`, `jobTaskType`, `jobTerminalState`,  `runCreatorUserName`|
| `delete` | user deletes a job | `jobId` |

## Logging Service

Custom logs and metrics can be send from Databricks notebooks using the logging
service of the [Wind Data Pipeline
Framework](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/WDAP%20-%20WinDEF/20353/Wind-Data-Pipeline-Framework)
(WinDEF). The service makes use of a custom log handler for the Python logging
library. The technical documentation can be found
[here](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/WDAP%20-%20WinDEF/20348/logging).
These logs are intended to enrich the workspace logs and provide further insight
into the ETL processes on the platform.

![databricks-custom-monitoring](../.img/platform-observability/etl_monitoring.drawio.png)

### Delta Table Metrics

The modules in the WinDEF are configured to automatically emit metrics when
performing operations on delta tables. These metrics are stored in the
`FUNCTIONAL_METRICS_LOGS_CL` custom log table on the Log Analytics Workspace
with the following schema:

| Column | Description |
| --- | --- |
| `timestamp_s` | Datetime of the delta operation |
| `table_identifier_s` | Unity Catalog name of the table in the form of `<catalog>.<schema>.<table>` |
| `operation_type` | Type of delta operation, e.g., `MERGE` or `WRITE` |
| `metric_name` | Name of the logged metric |
| `metric_value` | Value of the logged metric |
| `user_name` | User name who initiated the operation |
| `job_id` | Id of the job that made the operation, `null` if not run in a job |
| `job_run_id` | Id of the job run that made the operation, `null` if not run in a job |
| `run_id` | Id of the run that made the operation, `null` if not run in a job |
| `notebook_id` | Id of the notebook that made the operation |
| `cluster_id` | Id of the cluster where the operation was performed |

### Custom Logs

Using the WinDEF logging service, also custom logs can be emitted, for details how
to implement the WinDEF logging services in your jobs, see the [technical
documentation](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/WDAP%20-%20WinDEF/20348/logging)

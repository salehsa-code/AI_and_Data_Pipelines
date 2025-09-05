# Environment Variables

## Overview

This document provides a list of environment variables that are used by the Wind
Data Engineering Framework.

These variables can usually also set via parameters on the corresponding
classes, see the documentation of that class for the corresponding argument
names. The order of precedence is `argument` > `environment variable` >
`default`.

## List of Environment Variables

| Variable Name                        | Description                                                                                                                                                                               | Default Value               |
| ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------- |
| `WINDEF_LOG_TO_AZURE`                | If set to `true`, the framework will log to Azure Log Analytics Workspace. This can be overwritten when instantiating a class, e.g. `DeltaManager(enable_logging_to_azure=[True\|False])` | `false`                     |
| `LOG_ANALYTICS_WORKSPACE_ID`         | Sets the Id of the Azure Log Analytics Workspace, where the `LogAnalyticsHandler` sends its logs to.                                                                                      | `None`                      |
| `LOG_ANALYTICS_WORKSPACE_SHARED_KEY` | Sets the shared key of the Azure Log Analytics Workspace. The shared key is used by the `LogAnalyticsHandler` to authenticate against the Azure Log Analytics Workspace.                  | `None`                      |
| `LOG_TYPE`                           | The log type of the `LogAnalyticsHandler` sets in which table the logs are written in the Azure Log Analytics Workdspace.                                                                 | `None`                      |
| `WINDEF__Q_SCHEMA_NAME`              | Configures the name of the quarantine schema for the validation.                                                                                                                          |                             |
| `WINDEF__Q_QUARANTINE_HEADER_TABLE`  | Configures the name of the Quarantine Header table for the validation.                                                                                                                    |                             |
| `WINDEF__Q_QUARANTINE_RECORDS_TABLE` | Configures the name of the Quarantine Records table for the validation.                                                                                                                   |                             |
| `WINDEF__PIPELINE_ID`                | WinDEF Pipeline Id of the current pipeline. This environment variable is automatically set by the pipeline when a run starts.                                                             | Set by the WinDEF Pipeline. |

## Environment Variables and Pipelines

In the context of pipelines, environment variables can be set as part of the
pipeline definition, as [described here](./Pipeline.md).

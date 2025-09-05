# Wind Data and Analytics Platform Observability Solution

The Observability and Monitoring solution consists of three parts, the [Azure
infrastructure
logging](./Platform-Observability/Azure-Infrastructure-Monitoring), the
[Databricks infrastructure
logging](./Platform-Observability/Databricks-Infrastructure-Monitoring), and the
[Databricks functional
logging](./Platform-Observability/Databricks-Functional-Monitoring). Each
solution collects logs and metrics of a specific part of the platform and sends
them to a common Log Analytics Workspace, where the logs are made available for
common monitoring.

## Log Analytics Workspace

The Azure Log Analytics Workspaces serves as a central hub for all monitoring
data. Here, all logs and metrics from the different parts of the platform
logging arrive and can be queried for monitoring, reporting and alerting
purposes.

![log-analytics-workspace](./.img/platform-observability/log-analytics-workspace.drawio.png)

## Monitoring and Reproting

For monitoring and reporing purposes, the observability solution can integrate
with Power BI. Data from the Log Analytics Workspace can be queried from Power
BI via the data access API endpoint.

## Alerts

Action Groups and Alerts will be available as part of the deployable
infrastructure for each data product or data source via the IaC Framework.

Action Groups define the audience for alerts and can be set up to send email
alerts to the target audience.

Scheduled query alerts can be defined on the Log Analytics Workspace. A custom
Kusto query is evaluated at a certain frequency. Based on that query, the alert
is triggered if a threshold value is reached and the action group is notified.

Each data product is responsible to set up their own alert rules and action
groups using via the configuration files in their repositories. The deployment
of these alerts is handled automatically by the IaC framework, based on the
configuration files.

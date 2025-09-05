# Scheduled Log Alert

This module deploys an alert that triggers on a scheduled custom query on a
log analytics workspace.

See
https://learn.microsoft.com/en-us/azure/azure-monitor/alerts/alerts-create-log-alert-rule
for more information

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| azurerm | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azurerm_monitor_scheduled_query_rules_alert_v2.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_scheduled_query_rules_alert_v2) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| action\_groups | List of action group resource Ids that are notified when alert is triggered. | `set(string)` | yes |
| description | Description of the alert rule. | `string` | yes |
| dimensions | Map of Dimensions columns to split the alert rule. The alert rule is evaluated for each dimension value separately. | <pre>map(object({<br>    name     = string<br>    operator = string<br>    values   = string<br>  }))</pre> | no |
| display\_name | Display name of the Alert rule. Will be send as part of the title when the alert triggers. | `string` | yes |
| enabled | Decides if this alert rule is active. | `bool` | no |
| evaluation\_frequency | Period in which the query is evaluated. Cannot be greater that `window_duration` times `criteria.number_of_evaluation_periods` | `string` | yes |
| identity\_id | Resource Id of the User Assigned Managed Identity to use to query the Log Analytics Workspace. | `string` | yes |
| location | Azure region, where the storage account is deployed. | `string` | yes |
| log\_analytics\_workspace\_id | Resource Id of the Log Analytics Workspace that is queried for the alert. | `string` | yes |
| metric\_measure\_column | Specifies the column containing the metric used for evaluation. | `string` | no |
| minimum\_failing\_periods\_to\_trigger\_alert | Specifies the number of violations to trigger an alert. Must be smaller or equal to `number_of_evaluation_periods` | `number` | no |
| name | Name of the action group | `string` | yes |
| number\_of\_evaluation\_periods | Specifies the number of aggregated look-back points. | `number` | no |
| operator | Operator for evaluation of data points against threshold. Can be `Equal`, `GreaterThan`, `GreaterThanOrEqual`, `LessThan`, or `LessThanOrEqual` | `string` | yes |
| query | Valid Kusto query that is evaluated by the alert rule. | `string` | yes |
| resource\_group\_name | Name of the resource group, where the storage account is deployed. | `string` | yes |
| resource\_id\_column | Specifies the column containing the resource ID. | `string` | no |
| severity | Alert severity: 4 - Verbose, 3 - Informational, 2 - Warning, 1 - Error, 0 - Critical | `number` | yes |
| threshold | Threshold at which the alert is triggered. | `number` | yes |
| time\_aggregation\_method | Aggegation method applied to the data points. Can be `Average`, `Count`, `Maximum`, `Minumum`, or `Total` | `string` | yes |
| window\_duration | Bin size of each evaluation period. | `string` | yes |

## Outputs

No outputs.

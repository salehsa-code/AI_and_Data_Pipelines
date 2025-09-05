# Diagnostic Settings

This resource configures diagnostic settings for any viable Azure resource to
send logs and / or metrics to a Log Analytics Workspace.

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
| [azurerm_monitor_diagnostic_setting.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_diagnostic_setting) | resource |
| [azurerm_monitor_diagnostic_categories.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/monitor_diagnostic_categories) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| diagnostic\_settings\_name | Name of the diagnostic settings. | `string` | yes |
| log\_analytics\_workspace\_id | Name of the Log Analytics Workspace where logs are sent to. | `string` | yes |
| logs | List of log categories to enable. Enable all viable logs with `allLogs`. | `set(string)` | yes |
| metrics | List of metric categories to enable. | `set(string)` | no |
| target\_resource\_id | Resource Id of the target resource. | `string` | yes |

## Outputs

No outputs.

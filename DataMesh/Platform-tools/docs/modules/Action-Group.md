# Action Group

This module deploys an action group and adds receivers for email alerts.

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
| [azurerm_monitor_action_group.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_action_group) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| email\_receiver | Map of e-mail receivers in the form `<name>`: `<e-mail>`. | `map(string)` | yes |
| enabled | Determines if the action group is active. | `bool` | no |
| name | Name of the action group | `string` | yes |
| resource\_group\_name | Name of the resource group, where the storage account is deployed. | `string` | yes |
| short\_name | Short Name of the action group. Can not be longer than 12 characters. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| id | Resource Id of the action group. |
| name | Name of the action group. |

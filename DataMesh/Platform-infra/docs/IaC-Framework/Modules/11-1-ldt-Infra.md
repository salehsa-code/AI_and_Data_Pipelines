
This is a terraform solution for the deployment of the LDT infrastructure. It
deploys the Event Grid Namespace and Event Hub Namespace, as well as a user
assigned identity used for the push delivery of events to the eventhubs. For
the MQTT message delivery, additional resources need to be deployed for each
datastream, these can be added as part of the 14 solution.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azapi | ~> 1.13.0 |
| azurerm | ~>3 |

## Providers

| Name | Version |
|------|---------|
| azurerm | ~>3 |
| terraform | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| eventgrid | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/eventgrid | 20240430.1 |
| eventgrid\_logs | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/diagnostic_settings | 20240116.2 |
| eventhub\_namespace | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/eventhub | 20240424.1 |

## Resources

| Name | Type |
|------|------|
| [azurerm_user_assigned_identity.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/user_assigned_identity) | resource |
| [azurerm_resource_group.wdap](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/resource_group) | data source |
| [terraform_remote_state.platform_infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the configs directory. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| eventgrid\_namespace\_id | Resource Id of the eventgrid namespace. |
| eventgrid\_namespace\_topic\_id | Resource Id of the eventgrid namespace. |
| eventhub\_namespace\_name | Name of the eventhub namespace. |
| resource\_group\_location | Location of the LDT resource group. |
| resource\_group\_name | Name of the LDT resource group. |
| user\_assigned\_identity\_id | Resource Id of the user assigned identities. |

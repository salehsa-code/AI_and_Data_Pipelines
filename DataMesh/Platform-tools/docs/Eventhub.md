 # Eventhub

 This module deploys one Event Hub Namespaces and one or more Event Hubs.

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
| [azurerm_eventhub_namespace.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/eventhub_namespace) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| allowed\_subnets | One or more Subnet Ids which should be allowed on Eventhub Namespace. | `set(string)` | no |
| capacity | The capacity of the Eventhub namespace; defines the Throughput. | `number` | yes |
| default\_action | The default action of 'Allow' or 'Deny' when no other rules match for this Eventhub Namespace. | `string` | no |
| identity\_ids | The User Assigned Identity Id's which should be associated with the Eventhub Namespace. | `list(string)` | no |
| ip\_rules | One or more IPs which should be allowed on Eventhub Namespace. | `set(string)` | no |
| location | The location where the Eventhub namespace should be created. | `string` | yes |
| name | The name of the Eventhub namespace. | `string` | yes |
| public\_network\_access\_enabled | Whether or not public network access is allowed for this Eventhub Namespace. | `bool` | no |
| resource\_group\_name | The name of the resource group in which to create the Eventhub namespace. | `string` | yes |
| sku | The SKU of the Eventhub namespace. Must be 'Standard' or 'Premium'. | `string` | yes |
| tags | The tags to associate with the Eventhub namespace. | `map(string)` | no |
| trusted\_service\_access\_enabled | Whether or not Trusted Service Access is enabled for this Eventhub Namespace. Eventgrid Namspaces are Trusted Services. | `bool` | no |

## Outputs

| Name | Description |
|------|-------------|
| name | Name of the Eventhub Namespace |

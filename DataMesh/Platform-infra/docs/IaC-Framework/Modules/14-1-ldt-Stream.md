This is a terraform solution for the depoloyment of the LDT data stream
resources.

The solution includes the entities on the MQTT broker (topic space, clients,
client group, permission binding), an Event Hub, where the MQTT messages are
delivered to, as well as a Namespace Topic subscription for the push delivery
towards the Event Hub and a Stream Analytics job for the event capture towards
a storage account. The stream analytics job is deployed with a system-assigned
managed identity, which is then added as a member of the Entra Id security
group to the required role assignments.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.1.0 |
| azapi | ~>1 |
| azuread | >= 2.48.0 |
| azurerm | ~>3 |

## Providers

| Name | Version |
|------|---------|
| azurerm | ~>3 |
| terraform | n/a |

## Modules

| Name | Source | Version |
|------|--------|---------|
| mqtt\_delivery | git::git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/wind-da-platform-tools//terraform/modules/mqtt_delivery | 20241007.4 |

## Resources

| Name | Type |
|------|------|
| [azurerm_client_config.current](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/client_config) | data source |
| [terraform_remote_state.ldt_infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |
| [terraform_remote_state.platform_infra](https://registry.terraform.io/providers/hashicorp/terraform/latest/docs/data-sources/remote_state) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the backend storage configs directory. | `string` | yes |

## Outputs

No outputs.

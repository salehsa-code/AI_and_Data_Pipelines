# MQTT Delivery

This module deploys all resources required to publish (and subscribe) messages
on an MQTT endpoint of an eventgrid namespace and then push them towards an
eventhub on a eventhub namespace and further to a landing area in a storage
account. The delivery to the eventhub is done via push delivery of the event
grid namespace topic, while the delivery from the event hub to the storage
account is done using event capture with a stream analytics job.

To distribute the required permissions on the event hub namespace and the
storage account, the system assigned managed identity of the stream analytics
job is added to an Entra Id security group with according role assignments.

## Requirements

| Name | Version |
|------|---------|
| azapi | >= 1.12.1 |

## Providers

| Name | Version |
|------|---------|
| azapi | >= 1.12.1 |
| azuread | n/a |
| azurerm | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azapi_resource.client](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/resource) | resource |
| [azapi_resource.client_group](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/resource) | resource |
| [azapi_resource.namespace_topic_subscription](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/resource) | resource |
| [azapi_resource.permission_binding](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/resource) | resource |
| [azapi_resource.topic_space](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/resource) | resource |
| [azuread_group_member.this](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group_member) | resource |
| [azurerm_eventhub.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/eventhub) | resource |
| [azurerm_stream_analytics_job.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/stream_analytics_job) | resource |
| [azurerm_stream_analytics_output_blob.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/stream_analytics_output_blob) | resource |
| [azurerm_stream_analytics_stream_input_eventhub_v2.this](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/stream_analytics_stream_input_eventhub_v2) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| clients | Map of clients that can access the MQTT topic. Each client is defined by an authentication name and a thumbprint for certificate authentication | <pre>map(object({<br>    authentication_name = string<br>    thumbprint          = string<br>  }))</pre> | yes |
| event\_hub | Configuration for the Event Hub. | <pre>object({<br>    name                   = string // Name of the Event Hub to be created<br>    namespace_name         = string // Namespace in which the Event Hub will be created<br>    partition_count        = number // Number of partitions in the Event Hub<br>    message_retention_days = number // Number of days to retain messages in the Event Hub<br>  })</pre> | yes |
| event\_sender\_group\_id | The object Id of the group that has permission to retrieve and send events. | `string` | yes |
| event\_subscription | Configuration for the event subscription. | <pre>object({<br>    user_assigned_identity_id = string // The principal Id of the User Assigned Identity for the subscription<br>    event_time_to_live        = string // The time-to-live for events in the subscription<br>    event_max_delivery_count  = number // The maximum number of tries to deliver an event<br>  })</pre> | yes |
| eventgrid\_namespace\_id | The resource Id of the Event Grid Namespace where the MQTT resources will be created. | `string` | yes |
| location | Azure region where the stream analytics job is deployed. | `string` | yes |
| mqtt\_topic | Configuration for the MQTT topic. | <pre>object({<br>    name      = string       // Name of the MQTT topic to be created<br>    templates = list(string) // List of MQTT topic templates<br>  })</pre> | yes |
| namespace\_topic\_id | The unique identifier of the Namespace Topic | `string` | yes |
| resource\_group\_name | Name of the Azure Resource Group where the resources will be created | `string` | yes |
| streaming\_job | Configuration for the Stream Analytics Job. | <pre>object({<br>    name                                     = string                         // Name of the Stream Analytics Job<br>    input_name                               = string                         // Name of the input source for the job (event hub)<br>    output_name                              = string                         // Name of the output sink for the job (blob storage)<br>    storage_account_name                     = string                         // Name of the storage account of the output<br>    storage_container_name                   = string                         // Name of the storage container of the output<br>    output_path                              = string                         // Path pattern for the output files<br>    streaming_units                          = optional(number, 3)            // Number of streaming units allocated for this job<br>    events_late_arrival_max_delay_in_seconds = optional(number, 60)           // The maximum delay in seconds for late-arriving events<br>    events_out_of_order_max_delay_in_seconds = optional(number, 50)           // The maximum delay in seconds for out-of-order events<br>    batch_min_rows                           = optional(number, 2000)         // The minimum number of rows to include in a batch<br>    batch_max_wait_time                      = optional(string, "00:05:00")   // The maximum amount of time to wait before outputting a batch hh:mm:ss<br>    date_format                              = optional(string, "yyyy-MM-dd") // The date format used in the output path pattern<br>    time_format                              = optional(string, "HH")         // The time format used in the output path pattern (currently only HH possible)<br>  })</pre> | yes |

## Outputs

No outputs.

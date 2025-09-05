# Eventgrid Namespace

 This module deploys an eventgrid namespace. This deployment is currently
 (2024-03-18) not supported in the native azurerm provider and therefore using
 the azapi provider. See
 https://github.com/hashicorp/terraform-provider-azurerm/issues/24079

## Requirements

| Name | Version |
|------|---------|
| azapi | >= 1.12.1 |

## Providers

| Name | Version |
|------|---------|
| azapi | >= 1.12.1 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azapi_resource.eventgrid_namespace](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/resource) | resource |
| [azapi_resource.namespace_topic](https://registry.terraform.io/providers/Azure/azapi/latest/docs/resources/resource) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| capacity | Capacity of the SKU for the eventgrid namespace. Integer between 1-20 Mb/s ingress. Egress equals ingress * 2. | `number` | no |
| identity\_ids | A list of user assigned identity IDs. | `list(string)` | no |
| ip\_rules | Inbound IP rules for the eventgrid namespace. | `list(string)` | no |
| location | Azure region where the resources will be created. | `string` | yes |
| name | Name of the eventgrid namespace. | `string` | yes |
| namespace\_topic\_name | Name of the eventgrid namespace topic | `string` | yes |
| namespace\_topic\_retention | Retention days of the eventgird namespace topic | `number` | yes |
| resource\_group\_id | The ID of the resource group in which to create the resources. | `string` | yes |
| tags | Tags to be applied to the resources. | `map(string)` | no |

## Outputs

| Name | Description |
|------|-------------|
| id | Resource Id of the eventgrid namespace. |
| name | Name of the eventgrid namespace. |
| topic\_id | Resource Id of the eventgrid namespace topic. |
| topic\_name | Name of the eventgrid namespace topic. |

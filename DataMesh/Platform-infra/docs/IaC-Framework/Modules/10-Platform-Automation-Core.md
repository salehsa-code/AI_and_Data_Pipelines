This is a terraform solution for the deployment of the core automation
infrastructure of the Wind Data Analytics Platform. It is meant to be deployed
manually and includes the deployment of Service Principals used for automation
purposes.

## Requirements

| Name | Version |
|------|---------|
| terraform | >= 1.7.0 |
| azuread | >= 2.48.0 |
| azurerm | ~>3 |

## Providers

| Name | Version |
|------|---------|
| azuread | >= 2.48.0 |
| azurerm | ~>3 |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [azuread_application.this](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/application) | resource |
| [azuread_group.this](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/group) | resource |
| [azuread_service_principal.this](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/resources/service_principal) | resource |
| [azuread_group.owners](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/data-sources/group) | data source |
| [azuread_service_principal.owners](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/data-sources/service_principal) | data source |
| [azuread_user.this](https://registry.terraform.io/providers/hashicorp/azuread/latest/docs/data-sources/user) | data source |
| [azurerm_user_assigned_identity.owners](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/data-sources/user_assigned_identity) | data source |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| configs\_path | Path to the lakehouse storage configs directory. | `string` | yes |

## Outputs

| Name | Description |
|------|-------------|
| security\_group\_ids | A map of security groups and their object Ids. |

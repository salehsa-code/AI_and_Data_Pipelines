# Workspace IP access list

This module deploys an IP access list on a Databricks workspace. An access list can be either an "ALLOW" or "BLOCK" list.

IP access lists must be enabled on the workspace, e.g. using terraform:

```terraform
resource "databricks_workspace_conf" "this" {
  custom_config = {
    "enableIpAccessLists" : true
  }
}
```

## Requirements

No requirements.

## Providers

| Name | Version |
|------|---------|
| databricks | n/a |

## Modules

No modules.

## Resources

| Name | Type |
|------|------|
| [databricks_ip_access_list.allowed-list](https://registry.terraform.io/providers/databricks/databricks/latest/docs/resources/ip_access_list) | resource |

## Inputs

| Name | Description | Type | Required |
|------|-------------|------|:--------:|
| enabled | Activate this IP access list. | `bool` | yes |
| ip\_addresses | List of IP addresses to add to access list. | `list(any)` | yes |
| list\_type | Type of the IP access list. Can be `ALLOW` or `BLOCK` | `string` | yes |
| name | Name of the IP access list. | `string` | yes |

## Outputs

No outputs.

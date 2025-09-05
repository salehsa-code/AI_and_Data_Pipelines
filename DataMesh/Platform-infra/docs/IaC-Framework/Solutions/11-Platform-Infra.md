# WDAP Core Infrastructure

In this Terraform solution, the platform infrastructure in Azure is deployed.
Storage accounts for the datalake layers and for the Databricks catalog data are
created and their firewall and access policies are configured.

> :warning: During initial deployment of this module, it is advised to set the
> `shared_access_key_enabled` parameter of all storage accounts to `true` to
> avoid a crash in the apply step due to a lack of access permissions. The
> shared access key can be disabled, once the required RBAC roles are in place,
> see below.

## Deployment Notes

After the initial deployment of this step, the "Storage Blob Data Contributor"
role needs to be set for the Unity Catalog Access Connector Managed Identity
(`vap2-<env>-winddata-dbrks-uami`) and the DevOps service connection. Once these
are assigned, a catalog and storage credentials targeting each storage account
have to be created in the unity catalog. The project admins and the DevOps
service connection should be added to the owner group of the catalog. Also make
sure that the correct subnets for the infra and databricks vnets are allowed in
the storage account firewall.

## Configuration

The platform infrastructure deployment requires a global configuration file
(`global.yml`), where the resource group name is stored, as well as
configuration files for the data lake storage accounts
(`datalake_storage_accounts.yml`) and the unity catalog storage account
(`unity_catalog.yml`). The storage account configuration files follow a similar
pattern and detailed information on the fields can be found in the documentation
of the [storage
account](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Platform%20Tools/4730/Storage-Account).
The unity catalog configuration also requires information on the [storage
container](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_wiki/wikis/Wind%20Data%20Platform%20Tools/4731/Storage-Container)
used for the unity catalog data. A log analytics workspace configuration
 (`log_analytics.yml`) is required. If the `resource_group_name` configured in
this file matches the `resource_group_name` in the `global.yml` file, then a log
analytics workspace is deployed to this resource group based on the
configuration in `log_analytics.yml`. If a different `resource_group_name` is
defined, the log analytics workspace is loaded as a data source instead. Alerts
and action groups are configured optionally using the `alerts.yml` and
`action_groups.yml` files.

> While the Key Vaults (atm and cmn) are deployed by Cloud Core, they are
configured in this deployment. Since there is no Terraform resource for KV
Network ACLs, we had to act as if the KV was created in this Deployment. This
requires a manual import before deploying an environment for the first time.
Find the code
[here](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-infra?path=/terraform/11-platform_infra/main.tf&version=GBmain&line=102&lineEnd=105&lineStartColumn=1&lineEndColumn=1&lineStyle=plain&_a=contents).
*With Terraform Version >=1.5 import blocks were added, which can be used to
automatically import resources into the state during the apply step. This
feature will be implemented for the KVs in the future, once we update to the new
version of Terraform.*

All applicable resources are tagged using either default tags obtained from the
resource group, or custom tags that can be configured in the respective YAML
file using the `tags` field. If the same key is defined in the custom and
default tags, the custom tags overwrite default tags. Tags are assigned to:

- Data Lake Storage Accounts
- Unity Catalog Storage Account
- Databricks Access Connector
- Log Analytics Workspace
- Managed Identities\*

\*: User Assigned Managed Identities currently only get the default tags. If
there is a need to add custom tags to MI, contact Data Kong team.

As a note, all workspaces in all environments are currently set to allow access
from the prod workspaces's subnets. This is to enable the self service data
replication of production data into other environments for development teams not
part of Data Kong. This also includes the silver storage account.

### Global Config

```yaml
resource_groups:            # Names of resource groups used in the platform
  winddata:                 # Name of the winddata resource group
  windanalytics:            # Name of the wind analytics resource group
user_assigned_identities:   # A map of user assigned identities created on the platform
  <identifier>: <name>      # The key is used internally in terraform, the value is used as the name for the uami
allowed_subnets:            # A map of subnet objects that are whitelisted for the storage account. See example structures below.
    # Configuration using vnet and resource group. Only works if deployment service principal has at leas read access on this resource.
    <subnet1_name>:         # Use the subnet name as key of the object
      vnet_name:            # VNet name of the subnet
      resource_group_name:  # Resource Group where the VNet is deployed
    # Configuration using resource Id. Use this when the service principal does not have read access on the subnet.
    <subnet2_name>:         # Use the subnet name as key of the object
      resource_id:          # Azure resource Id of the subnet.
key_vaults:                 # Confiugration for key vaults
  vaults:                   # A map of key vault objects
    <identifier>:           # The key is used internally in terraform
      name:                 # Name of the key vault
      resource_group_name:  # Resource group name of the key vault
      subnets:              # A list of subnets keys from the map defined above that are allowed network access to the key vault
  location:                 # Azure location of all key vaults
  ip_allow_list:            # A list of IP addresses or CIDR ranges that are allowed network access to the key vault
    - ...
```

### Storage Accounts

Configuration files for the storage accounts use this schema

```yaml
<identifier>:               # Terraform internal identifier for the storage account
  resource_group_name:      # Name of the storage account resource group. Needs to exist before deployment
  name:                     # Name of the storage account
  account_tier:             # Storage Account Tier, Standard or Premium
  account_replication_type: # Storage Account Replication Tier, e.g. LRS, ZRS, etc.
  is_hns_enabled:           # Decides if the Storage Account is deployed with the hierarchical namespace feature enabled, required for the use as data lake
  allowed_subnets:          # A list of subnets referencing the subnet object defined in the global.yml
  private_link_access:      # A list of private link endpoints that are allowed network access to the storage account
    - endpoint_resource_id: # Azure resource Id of the private endpoint
      endpoint_tenant_id:   # Azure tenant Id of the private endpoint. Usually this is the Vattenfall tenant.
```

### Logs and Alerts

Log Analytics

```yaml
workspace_name:             # Name of the log analytics workspace (LAW)
resource_group_name:        # Name of the resource group of the LAW
sku:                        # LAW SKU
retention_in_days:          # How long logs are kept on the LAW in days
diagnostic_settings_name:   # diagnostic settings name used for all resources, where diagnostic settings are deployed
```

Action Groups

```yaml
# A map of alert group objects
<name>:               # the key is used for names, must be max 9 characters
  email_receiver:     # A map of email alert receivers
    <identifier>:     # The key is used as the display name, the value must be a valid email address
```

Alerts

```yaml
# A map of alert objects
<name>:                         # the key is used for names
  evaluation_frequency: "P1D"   # how often is the query evaluated, cannot be greater than window_duration * number_of_evaluations
  window_duration: "P1D"        # what is the bin size of the query
  identity:                     # User Assigned Managed Identity used for the evaluation of alerts
    # You can use one of the following ways to set the identity
    key:                        # Key of the UAMI defined in global.yml. Use, if identity is part of this deployment
    id:                         # Azure Resource Id of an UAMI. Use, if identity is NOT part of this deployment
  severity: 1                   # alert severity from 4 - low to 0 - critical
  display_name:                 # Display Name of the alert. This will be displayed in the notification
  action_groups:                # A list of action groups that should be notified when this alert is triggered
    - ...
  description:                  # Description of the alert. This will be displayed in the notification
  criteria:                     # An alert criteria object. See https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs/resources/monitor_scheduled_query_rules_alert_v2 for more info
    query: |
      SecretRotation_CL
      | where status_s == "error"
    time_aggregation_method: "Count"  # How datapoints should be aggregated
    operator: "GreaterThanOrEqual"    # How aggregated value is evaluated
    threshold: 1                      # Threshold for sending alerts
```

> The User Assigned Managed Identity used for Alert evaluation requires at least
> the 'Log Analytics Reader' RBAC role.

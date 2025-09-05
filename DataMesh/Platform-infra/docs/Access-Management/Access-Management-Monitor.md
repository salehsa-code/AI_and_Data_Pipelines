# Access Management Monitoring

## Scope

This library scrapes permissions from various services and logs them to dynamic
targets. The following services are currently supported:

- Azure Platform (Resources, Key Vault ACLs, Storage Account ACLs)
- Azure DevOps (Repositories, Pipelines, Libraries)
- Databricks Unity Catalog (Catalogs, Schemas, Tables)
- Power BI (Workspaces, Reports, Datasets)

The permissions are logged to an Azure Log Analytics Workspace on a daily basis
and displayed in a [Power BI
Report](https://app.powerbi.com/groups/b3806f05-cf83-4dde-8af1-a716e71f4167/reports/f9fb7bb9-0f02-4f2d-93e6-054517369587/ReportSection755d2738e3b7c8fc0f38?language=en-US&experience=power-bi).

## Usage

The library is intended to be configured via environment variables. It can be
run on any compute. See the
[Configuration](#configuration) section for more details.

Once the environment variables are set, the library can be run using the
following command:

```python
from permissions_logger import PermissionsLogger

p = PermissionsLogger()
p.log_permissions()
```

## Configuration

Configure the library using environment variables. Envrionment variables can be
read from a `.env` file in the access management monitor directory.

> :warning: Never write secrets directly in the `.env` file and check them into
> the repository. See below how to instead automatically obtain secrets from a
> key vault.

<!-- -->
> :bulb: It is possible to automatically read secrets from key vaults. To
> do so, you have to set the value of the respective environment variable in the
> following format: `{{<key_vault_name>:<secret_name>}}`. The access management
> monitor is then trying to read the secret form the key vault and overwrite the
> environment variable.

### General

| variable name                         | description                                                                                                         | default |
| --------------------------------------| ------------------------------------------------------------------------------------------------------------------- | ------- |
| `amm_tenant_id`                       | The Tenant Id of the monitored tenant.                                                                              | `` |

### Logging

| variable name                         | description                                                                                                         | default |
| --------------------------------------| ------------------------------------------------------------------------------------------------------------------- | ------- |
| `logging_enabled`                     | Determines if logging is enabled.                                                                                   | `false` |
| `logging_target_enable_stream`        | Determines if the console is used as a logging target.                                                              | `false` |
| `logging_target_enable_log_analytics` | Determines if the Log Analytics Workspace is used as a logging target.                                              | `false` |
| `log_analytics_workspace_id`          | ID of the Log Analytics Workspace. Only required if `LOGGING_TARGET_ENABLE_LOG_ANALYTICS` is set to `true`.         |         |
| `log_analytics_workspace_shared_key`  | Shared Key of the Log Analytics Workspace. Only required if `LOGGING_TARGET_ENABLE_LOG_ANALYTICS` is set to `true`. |         |
| `log_type`                            | Name of the Table in Log Analytics Workspace.                                                                       |         |

### Databricks Unity Catalog

Required permissions for the Service Principal:

- Service Principal must be Owner of the Catalog(s). With "USE_CATALOG"
  privileges, the user only gets its own privileges.

| variable name                      | description                                                                               | default |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | ------- |
| `log_databricks_permissions`       | Determines, if permissions for Databricks are logged                                      | `false` |
| `databricks_config_path`           | Path to the Databricks configuration file. This configuration stores the UC Catalog names |         |
| `databricks_monitoring_app_id`     | The Application Id of the Service Principal authenticating with Databricks REST API       |         |
| `databricks_monitoring_app_secret` | The Secret of the Service Principal authenticating with Databricks REST API               |         |

### Power BI

Required permissions for the Service Principal:

- Member Permission on the Power BI Workspace(s)
- Permission to use the Power BI API

| variable name                      | description                                                                               | default |
| ---------------------------------- | ----------------------------------------------------------------------------------------- | ------- |
| `log_power_bi_permissions`         | Determines, if permissions for Power BI are logged                                        | `false` |
| `power_bi_monitoring_app_id`       | The Application Id of the Service Principal authenticating with Power BI REST API         |         |
| `power_bi_monitoring_app_secret`   | The Secret of the Service Principal authenticating with Power BI REST API                 |         |

### Azure DevOps

Required permissions for the Service Principal:

- Read Permission on all desired repositories, libraries and pipelines

| variable name                       | description                                                                               | default |
| ----------------------------------- | ----------------------------------------------------------------------------------------- | ------- |
| `log_devops_permissions`            | Determines, if permissions for Azure DevOps are logged                                    | `false` |
| `azure_devops_organization`         | The name of the Azure DevOps Organization                                                 |         |
| `azure_devops_project`              | The name of the Azure DevOps Project                                                      |         |
| `azure_devops_monitoring_app_id`    | The Application Id of the Service Principal authenticating with Azure DevOps REST API     |         |
| `azure_devops_monitoring_app_secret`| The Secret of the Service Principal authenticating with Azure DevOps REST API             |         |

### Azure Platform

Required permissions for the Service Principal:

- Reader Role on the Subscription(s)/ Resource Group(s)

| variable name                       | description                                                                                                               | default |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------- |
| `log_azure_permissions`             | Determines, if permissions for Azure Platform are logged                                                                  | `false` |
| `log_resource_group_permissions`    | Determines, if permissions for Azure Resource Groups are logged                                                           | `false` |
| `log_key_vault_permissions`         | Determines, if permissions for Azure Key Vaults are logged                                                                | `false` |
| `log_adls_permissions`              | Determines, if permissions for Azure Data Lake Storage are logged                                                         | `false` |
| `azure_resource_group_config_path`  | Path to the Azure Resource Group configuration file. This configuration stores the RG names and subscription information. |         |
| `azure_key_vault_config_path`       | Path to the Azure Key Vault configuration file. This configuration stores the KV names and subscription information.      |         |
| `azure_storage_account_config_path` | Path to the Azure Storage Account configuration file. This configuration stores the SA names and Depth.                   |         |

### Groups

| variable name                       | description                                                                                                               | default |
| ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------- |
| `log_group_memberships`             | Determines, if group memberships are logged                                                                               | `false` |

### Azure Platform Configuration

| variable name                          | description                                                               | default |
| -------------------------------------- | ------------------------------------------------------------------------- | ------- |
| `azure_platform_monitoring_app_id`     | The Application Id of the Service Principal authenticating with Graph API |         |
| `azure_platform_monitoring_app_secret` | The Secret of the Service Principal authenticating with Azure Graph API   |         |

## Development

It is easy to extend the library to support additional services. The following
steps are required:

1. Create a new service inheriting from the `Service` class
   - The service must implement the `add_permissions` method adding identities
     and their permissions to the `self.identities` defaultdict
2. Create a new handler, if required
   - Handlers interact with the services API and return the required
     information, new services can potentially use existing handlers
3. Add new configuration variables to the `.env.sample` file
4. Modify the `log_permissions` method in the `PermissionsLogger` class to log
   the new service
   - Add a check for the new configuration variables
   - Add a private method to log the new service that instantiates the service
     and calls the `add_permissions` method

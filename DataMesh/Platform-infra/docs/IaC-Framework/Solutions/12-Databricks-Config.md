# Databricks Catalogs

In the next solutions, the Databricks workspaces are configured. This solution
actually consists of two solutions, the first one `12_1-dbrks_catalog`
configures the Databricks catalogs and deploys commonly used external locations,
schemas and external volumes. This solution also sets permissions on these Unity
Catalog objects. The second part is `12_2-dbrks_workspace`. Currently, there are
two workspaces, `etl` and `analytics` - for each workspace the
`12_2-dbrks_workspace` solution is configured and deployed separately. For both
workspaces, an IP access list is placed on the workspaces and enabled, denying
access from outside the Vattenfall network. Additionally, workspace-binding of
the WDAP catalogs and external locations are configured for the workspaces, so
that access from outside the correct workspace is denied. For the `ATM` and
`CMN` key vaults, secret scopes are registered on the workspaces. Additionally,
a Key Vault backed secret scope is deployed, where external location paths are
stored for reference in notebooks. The secrets are set in the
`12_1-dbrks_catalog` solution, as well as in the downstream solutions
`14-data_source` and `21-data_product`. Cluster pools in T-shirt sizes are
created to be used in the cluster policies. Cluster policies and init scripts
are deployed to the workspaces set in their configuration files. SQL warehouses
are only deployed to the `analytics` workspace. A shared compute cluster is
deployed to the development workspaces. Permissions on the secret scopes,
cluster policies and SQL warehouses are granted.

After the initial deployment of this stage, the catalog mode for the WDAP
catalogs has to be changed from `OPEN` to `ISOLATED` in order for the
workspace-binding to take effect. This can be done via the Databricks UI by an
owner of the catalog.

## Configuration

Although this solution is split into two parts (`12_1-dbrks_catalog` and
`12_2-dbrks_workspace`), the configuration is stored in one place at
`config/<env>/12-dbrks_config`, because the two solutions actually share some
configuration. In the root of the config directory for each environment the configuration
files for the `12_1-dbrks_catalog`, as well as common configuration files for all
instances of `12_2-dbrks_workspace` are stored.

Information from the platform infrastructure deployment (`11-platform_infra`) is
read directly from the output of its remote state, e.g. the Ids and short names
of the storage accounts. The information required to import the remote state is
set in [`remote.yml`](../Solutions.md##remote-state-datasource-config).

The `catalogs.yml` file configures the Databricks catalogs used in WDAP,
including the definition of commonly used schemas and external volumes, as well
as permissions on all of these Unity Catalog objects. Descriptions of available
permissions (priviliges) and what exactly they grant is available in the
[azure databricks wiki](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/privileges).

For each workspace configured with the `12_2-dbrks_workspace`, there is a
folder under the `workspaces` folder containing specific configuration files for
this workspace. The `workspace.yml` configuration file contains required
information on the Databricks workspace such as the workspace configurations and
IP access lists. Workspace binding to the respective workspace is enabled for
the catalogs listed under the `catalogs` key.

The remaining config files, i.e. `cluster_pools.yml`, `config.yml`, `data_replication.yml`,
`init_scripts.yml`, `interactive_cluster_policies.yml`, `job_cluster_policies.yml`,
`spark_env.yml`, `secret_scopes.yml`, and `sql_warehouses.yml` are used to configure
the respective modules or to provide more specific config to `main.tf`. These config
files can be in the root of the directory and in the workspace specific directory.
The files located in the root directory will be used in all workspaces, while the workspace
specific files are used to extend or overwrite these common configurations.

### Catalogs and External Locations

Catalogs

```yaml
# A map of catalog objects
<identifier>:                   # The key is used as a terraform internal identifier
  name:                         # Name of the catalog
  user_groups:                  # A map of group names (or service principal Id) and permissions granted to the group
    <principal_name>:           # List of permissions
  schemas:                      # A map of schema objects
    <identifier>:               # The key is used as schema name
      grant_exclusive:          # Are grants exclusively set here, or can other deployments also set grants. If true, will overwrite existing grants.
      grants:                   # A map of group names or service principal Ids and permissions granted to the group
        <principal_name>:       # List of permissions
      external_volumes:         # A map of external volume objects
        <identifier>:           # The key is used as external volume name
          storage_account:      # Key of the storage account for the external volume (see 11 for keys)
          container_name:       # Name of the storage container for the external volume
          grant_exclusive:      # Are grants exclusively set here, or can other deployments also set grants. If true, will overwrite existing grants.
          grants:               # A map of group names or service principal Ids and permissions granted to the group
            <principal_name>:   # List of permissions
```

External Locations

```yaml
# A map of external location objects
<identifier>:                   # The key is used as a terraform internal identifier
  storage_account:              # Name of the storage account for the external location (see 11 for keys)
  container_name:               # Name of the storage cotnainer for the external location
  grant_exclusive:              # Are grants exclusively set here, or can other deployments also set grants. If true, will overwrite existing grants.
  grants:                       # A map of group names or service principal Ids and permissions granted to the group
    <principal_name>:           # List of permissions
```

### Workspace

```yaml
name:                           # Name of the Workspace
resource_group_name:            # Resource group name of the workspaces
catalogs:                       # List of catalog keys (see above) that are bound to the workspace
  - ...
external_locations:             # List of externalo location keys (see above) that are bound to the workspace
  - ...
config:                         # A map of workspace configurations. Key value pairs are set in the workspace config.
  key: value
workspace_groups:               # A map of groups and group members that are created as local workspaces groups. Workspace groups should have the prefix dwg_
  <group_name>:                 # Use the group name as key
    groups:                     # Groups that are added as members of the group
      - ...
    service_principals:         # Service Principals that are added as members of the group
      - ...
enabled_logs:                   # A list of diagnostic logs that are enabled on the workspace. See https://learn.microsoft.com/en-us/azure/databricks/administration-guide/account-settings/audit-logs
  - ...
```

### Compute

Cluster Pools

```yaml
# Default cluster pool options. Will be set for all cluster pools unless overwritten
default:
  # Any settings done for cluster pools can be configure here
# A map of cluster pool objects
<cluster_pool_name>:          # Key is used as cluster pool name
  # Settings defined here will overwrite settings in default
  # Possible Settings are:
  min_idle_instances:         # Number of idle instances kept in the pool at all times
  autoterminate_minutes:      # Time until idle instances are terminated
  enable_elastic_disk:        # Enable elastic disk for clusters
  preloaded_spark_versions:   # List of preloaded spark runtime versions. List must have exactly one entry
  max_capacity:               # Maximum number of clusters in the pool. Set to null to allow unlimited clusters
  spot:                       # Use spot instance for clusters
  node_type_id:               # Cluster type for clusters in this pool
```

Cluster Policies

```yaml
# Default cluster policy settings. Will be set for all cluster policies unless overwritten.
default:
  name: Default
  # Can use the same settings as cluster policy objects.
  policy_definition: # JSON string containting the policy definition.
# A map of cluster policy objects
<identifier>:                 # Key is used as terraform internal identifier
  name:                       # Name of the cluster policy
  groups:                     # A list of groups that can use this cluster policy
    - ...
  pools:                      # A list of cluster pools from which clusters can be chosen
  policy_definition:          # JSON string containting the policy definition. If set also in defaults, the policies will be merged. Fields defined in both will be overwritten by the actual policy.
```

> Additionally, all catalog names are added to the cluster policies as required
> environment variables, as well as all environment variables specified in the
> `spark_env.yml` config, see below.

Spark Env

```yaml
# A list of key-value pairs that are set as required environment variables
<env_name>: <env_value>
```

SQL Warehouses

```yaml
# A map of SQL warehouse objects
<warehouse_name>:             # Key is used as warehouse name
  cluster_size:               # Warehouse cluster size: '2X-Small', 'X-Small', etc.
  warehouse_type:             # Warehouse type: Standard, Pro, or Serverless
  min_num_clusters:           # Minimum number of clusters used for the warehouse
  max_num_clusters:           # Maximum number of clusters used for the warehouse
  auto_stop_mins:             # Minutes until an idle warehouse is terminated
  enable_photon:              # Enable photon optimization for the warehouse
  spot_instance_policy:       # Spot instance policy for this warehouse
  permissions:                # A map of permissions on the warehouse
    groups:                   # A map of permissions assigned to groups
      <group_name>:           # Permission for the particular group defined under the key
    service_principals:       # A map of permissions assigned to service principals
      <application_id>:       # Permission for the particular service principal defined under the key
  tags:                       # A map of tags applied to the warehouse
```

### Other

Secret Scopes

```yaml
# A map of secret scope objects
<secret_scope_name>:          # The key is used as the secrets scopes name
  permissions:                # A map of permissions on the secret scope. Note that Key-Vault-backed secret scope only support READ permissions.
    <principal_name>:         # Use the principal (group name or service principal app Id) as key and the assigned permission as value
  type:                       # type of the secret scope. kv - key-vault-backed secret scope; dbrks - Databricks backed secret scope
  key_vault:                  # when using the kv type, provide also a key vault object
    name:                     # Name of the key vault
    resource_group:           # Resource group of the key vault
```

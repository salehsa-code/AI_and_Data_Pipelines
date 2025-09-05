# Data Source

In this stage, the infrastructure for the data source is deployed.

> :bulb: This solution must be configured and deployed for each data source
> separately. The necessary pipeline definition and config files are
> automatically created in the bootstrap solution using templates, but should be
> adapted to match the requirements of the data source.

A storage container for the data source is deployed to the data lake bronze
storage account. In Databricks, an external location for the storage container
is created to grant access to the data. A schema is created in the sources
catalog. Permissions are granted to groups on the workspace, based on the
configuration from the data source repository. Additionally, the external
location path is stored in the external location path secret scope, to allow
referencing it in notebooks.

## Configuration

In the `config` directories for the data sources, only the configuration managed
by the Data Kong team, as well as their Terraform backend configurations are
stored. Additionally, information to import the remote states of the platform
infrastructure and workspace configuration deployments ([`remote.yml`](../Solutions.md##remote-state-datasource-config)) are stored
at the root directory.

The configuration managed by the Data Kong team includes permanent settings of
the data source. The configuration is stored in the `data_source.yml` file:

```yaml
"name": <name>                # name of the data source
"short_name": <short_name>    # short name of the data source
```

The config file is created during the initial bootstrap of the data source. The
`name` and `short_name` should not be changed, since all resources depend on it
and a change will lead to redeployment of all data source resources.

Additional configuration files for the ADLS gen2 filesystem and Unity Catalog
objects, i.e. `grants.yml` and `datalake_acls.yml` are stored in the sources
repository (`wind-da-data-sources`) and are checked out from there by the
deployment pipeline.

`grants.yml`: Defines the permissions granted on the data source resources. The
`grants.yml` file follows this structure:

```yaml
# A map of permission objects
"<group name>":                         # The key references the AD group name
  external_location:
    - "<permission>"                    # list of permissions granted for the data source's external location to the group
  schema:
    - "<permission>"                    # list of permissions granted for the data source's schema to the group
  databricks_directory: "<permission>"  # permission on the data source's Databricks directory
  secret_scope: "<permission>"          # permission on the data source's secret scope
```

For each group that should get permissions on the data source, such an entry has
to be created. Refer to
[this](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/privileges#--privilege-types-by-securable-object-in-unity-catalog)
documentation for all possible permissions on Unity Catalog objects. The fields
can be left empty, but need to be present for Terraform to be able to read the
config file. Under `external_location`, the permissions for the data source's
external location, i.e., the data source storage container, are configured. If
no permissions should be granted, put `{}`. Similarly, the permissions on schema
owned by the data source are configured under `schema`. Put `{}` if no
permissions should be granted. The `databricks_directory` field sets the
permissions on the Databricks directory of the data source. Possible permissions
are `"CAN_READ"`, `"CAN_RUN"`, `"CAN_EDIT"`, or `"CAN_MANAGE"`. If no
permissions should be granted, put `""`. Finally, under `secret_scope`,
permissions for the Databricks-backed secret scope are granted (see
`key_vault_acls.yml` for permissions on the Azure key vault-backed secret
scope). Possible permissions are `"READ"`, `"WRITE"`, or `"MANAGE"`. If no
permissions should be granted, put `""`.

`datalake_acls.yml`: This file defines the ACLs that are applied to the data
source's storage container on the ADLS storage account.

```yaml
principals:                               # A map of principal objects
  <principal_identifier>:                 # The key is used only internally in the ACL deployment. Should be descriptive for the principal, e.g. the principal name.
    principal_type: <principal_type>      # possible values are 'user' and 'group'. For service principals, specify 'user'.
    principal_id: <uuid-object-id>        # object Id of the principal
root:                                     # A nested map of ACL objects, starting at the container root
  assignments:                            # Assignments on the Container root
      <principal_identifier>: <rwx|rwx>   # ACL posix, defaults after "|" separator. Use the principal identifier declared above for the principals object
  children:                               # A list of child nodes for which ACLs should be specified
    - name: level_1_directory             # name of the directory, created if it doesn't exist
      assignments:
          <principal_identifier>: --x|--x
      children:                           # children of this directory, i.e. nested folders
        - name: level_1_directory_child
          assignments:
            <principal_identifier>: rwx|r-x
```

The configuration will be deployed with [this
script](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-infra?path=%2Fbuild-scripts%2Fdatalake-acls%2Fmain.py&version=GBmain&_a=contents)
in [this
pipeline](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-infra?path=/build-scripts/datalake-acls&version=GBmain&_a=contents).
The pipeline is created individually for each data product during the
bootstrap.
Principals are defined at the top of the configuration file, in the rest of
the file they can be referenced using the human-readable name instead of the
object Id. Each file defines its own principals to make sure they are not
forgotten to add, even though that might mean some repetition across files.

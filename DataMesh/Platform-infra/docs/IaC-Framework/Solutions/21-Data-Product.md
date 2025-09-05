# Data Product

In the final stage of the platform deployment, the infrastructure for the data
products is deployed.

> :bulb: This solution must be configured and deployed for each data product
> separately. The necessary pipeline definition and config files are
> automatically created in the bootstrap solution using templates, but should be
> adapted to match the requirements of the data product.

A storage container for the data product is deployed to the data lake storage
account, depending on the type of data product. Primary data products are
deployed to the silver storage account, while secondary data products are
deployed to the gold storage account. In Databricks, an external location for
the storage container is created to grant access to the data. A schema is
created in the data products catalog. If the product is configured to have its
own key vault, the key vault is deployed, permissions are set and a key
vault-backed secret scope is registered in Databricks. Permissions on the data
product resources are granted to groups on the workspace, based on the
configuration from the data product repository. Additionally, the external
location path is stored in the external location path secret scope, to allow
referencing it in notebooks.

## Configiuration

In the `config` directories for the data products, only the configuration
managed by the Data Kong team, as well as their Terraform backend configurations
are stored. Additionally, information to import the remote states of the
platform infrastructure and workspace configuration deployments ([`remote.yml`](../Solutions.md##remote-state-datasource-config))
are stored at the root directory.

The configuration managed by the Data Kong team includes permanent settings of
the data product. The configuration is stored in the `data_product.yml` file:

```yaml
name: <name>                # name of the data product
short_name: <short_name>    # short name of the data product
type: <primary/secondary>   # type of data product, i.e. primary or secondary
has_key_vault: true         # option to deploy a key vault with the data product
groups:
  <group_name>: <role>      # currently supports only Developer Role
tags:                       # key-value-pairs used to tag data product resources
  <key>: <value>
```

The config file is created during the initial bootstrap of the data product. The
`name` and `short_name` should not be changed, since all resources depend on it
and a change will lead to redeployment of all data product resources. The
`has_key_vault` option defines, if a key vault and key vault-backed secret scope
will be deployed for the data product. Key vault and secret scope ACLs are
however set by the data product itself, see below. If a key vault should be
deployed, `tags` should be set for `costallocation` and `contact`. The
`costallocation` tag is used to assign the resource costs to the respective cost
element, the `contact` tag is used to identify a technical contact for the Data
Kong team. Additional tags can be specified if needed. Once possible, the `tags`
field will also be used to tag Unity Catalog objects belonging to the Data
Product, however, this feature is currently not available.

The groups mapping in this file defines, which groups are added to the Workspace
group `dwg_dev_elt_data_product_engineer` which has permissions to the
interactive general clusters as well as cluster policies.

Additional configuration files for the ADLS gen2 filesystem, Unity Catalog
objects, permissions, and DevOps environment policies, i.e. `grants.yml`,
`devops_approvers.yml`, `key_vault_acls.yml` and a folder for `datalake_acls`
are stored in the repositories of the data products and are checked out from
there by the deployment pipeline.

`grants.yml`: Defines the permissions granted on the data product resources. The
`grants.yml` file follows this structure:

```yaml
"<group name>":                           # AD group name
  external_location:
    "<storage account short name>"        # short name of the data lake storage account
      - "<permission>"                    # list of permissions granted for this external location to the group
  schemas:
    "<catalog short name>":               # short name of the Databricks catalog
      - "<permission>"                    # list of permissions granted for this schema to the group
  databricks_directory: "<permission>"    # permission on the Databricks directory
  secret_scope: "<permission>"            # permission on the data product secret scope
```

For each group that should get permissions on the data product, such an entry
has to be created. Refer to
[this](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/privileges#--privilege-types-by-securable-object-in-unity-catalog)
documentation for all possible permissions on Unity Catalog objects. The fields
can be left empty, but need to be present for Terraform to be able to read the
config file. Under `external_location`, the permissions for the external
locations, i.e., the data product storage containers, are configured. If no
permissions should be granted, put `{}`. Similarly, the permissions on schemas
owned by the data product are configured under `schemas`. Put `{}` if no
permissions should be granted. The `databricks_directory` field sets the
permissions on the Databricks directory of the data product. Possible
permissions are `"CAN_READ"`, `"CAN_RUN"`, `"CAN_EDIT"`, or `"CAN_MANAGE"`. If
no permissions should be granted, put `""`. Finally, under `secret_scope`,
permissions for the Databricks-backed secret scope are granted (see
`key_vault_acls.yml` for permissions on the Azure key vault-backed secret
scope). Possible permissions are `"READ"`, `"WRITE"`, or `"MANAGE"`. If no
permissions should be granted, put `""`.

`devops_approvers.yml`: Defines the approval policies and approvers on the
DevOps deployment environment that was created for your data product. The
`devops_approvers.yml` file has this structure:

```yaml
approvers:
  - "<DevOps user>"                       # list of users that can approve deployments in this environment
timeoutMinutes: 60                        # minutes until the pipeline stops if no approval is given
minRequiredApprovers: 1                   # number of individual approvers for the pipeline to deploy
requesterCannotBeApprover: false          # if user who triggered the pipeline approve it
```

The list of DevOps users under `approvers` are given permission to permit or
reject deployment steps of pipelines within this environment. You can set
individual rules for each environment.

`datalake_acls`: Can contain one file per datalake layer (i.e. `products.yml`,
`sources.yml` , `derived.yml`). Only create the files for the storage layers
that are applicable for the data product. These files define the ACLs that are
applied to the containers of the data products' container in the corresponding
storage layer.

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
The pipeline is created individually for each data product during the bootstrap.

Principals are defined at the top of the configuration file, in the rest of the
file they can be referenced using the human-readable name instead of the object
Id. Each file defines its own principals to make sure they are not forgotten to
add, even though that might mean some repetition across files.

`key_vault_acls.yml`: Defines access control to the data product key vault and
key vault-backed secret scope. Note that setting up this file is ony required,
if a key vault is deployed for the data product, see data product configuration
above.

```yaml
<principal_name>:
  object_id: <principal-object-id>
  secret_scope: <true/false>              # option to give the principal read permission on the key vault-backed secret scope
  key_permissions: ["Encrypt", "Decrypt", "WrapKey", "UnwrapKey", "Sign", "Verify", "Get", "List", "Create", "Update", "Import", "Delete"]  # key permissions on the Azure key vault
  secret_permissions: ["Get", "List", "Set", "Delete"]  # secret permissions on the Azure key vault
  certificate_permissions: ["Get", "List", "Delete", "Create", "Import", "Update", "ManageContacts", "GetIssuers", "ListIssuers", "SetIssuers", "DeleteIssuers", "ManageIssuers"] # certificate permissions on the Azure key vault
```

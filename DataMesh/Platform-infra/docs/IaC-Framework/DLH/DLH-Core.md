# DLH

The main DLH solution covers the configuration of Unity Catalog
(UC) objects in the DLH catalogs.

The scope of this deployment is the setup of external locations and the
configuration of grants on external locations and schemas.

## Config Files

The config files are located in `config/<env>/666-dlh`, where `<env>` is one of
dev, tst, acc, prd.

### external_locations.yml

This config file contains the configuration for external locations. It follows
this structure:

```yaml
external_location_1:        # Name of the external location
  storage_account: ""       # Name of the storage account
  container_name: ""        # Name of the storage container
  catalog: ""               # Name of the associated catalog
  credential_name: ""       # Name of the Databricks Connect credential
  grant_exclusive: false    # Should grants on this external location be set exclusively?
  grants:                   # A map of principals and the granted permissions
    "group_name": ["READ_FILES"]
    "service_principal_app_id": ["READ_FILES"]
```

External locations are created on the level of storage containers.

Access can be granted on each external location to groups or service principals.
Each entry in the `grants` field has the principal identifier (group name for
groups; application Id for service principals) and a list of granted
permissions. See
[here](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/privileges#privilege-types)
for a full description of all available privileges. For the configuration file
you need to replace any space in the privilege name with an underscore, e.g.,
`CREATE TABLE` becomes `CREATE_TABLE`.

### schemas.yml

This config file contains the configurations for grants on UC schemas. It
follows the following structure:

```yaml
schema_name_1:  # Name of the schema to be configured
  grants:       # A map of principals and the granted permissions
    "group_name": ["SELECT"]
    "service_principal_app_id": ["SELECT"]
  tables: # A map of tables and the principals permissions
    table_name_1:
        "another_group_name": ["SELECT", "MODIFY"]

schema_name_2:  # Name of the next schema
  grants:       # A map of principals and the granted permissions
    "group_name": ["SELECT"]
    "service_principal_app_id": ["SELECT"]

# ...
```

Access can be granted on a schema level to groups or service principals. Each
entry in the `grants` field has the principal identifier (group name for groups;
application Id for service principals) and a list of granted permissions. See
[here](https://learn.microsoft.com/en-us/azure/databricks/data-governance/unity-catalog/manage-privileges/privileges#privilege-types)
for a full description of all available privileges. For the configuration file
you need to replace any space in the privilege name with an underscore, e.g.,
`CREATE TABLE` becomes `CREATE_TABLE`.

Access on table level can be granted as shown in the above example. If a schema
has the `tables` key defined, the permissions will be granted additionally to
schema level permissions, i.e. it is possible to grant `["SELECT"]` on schema
level and `["SELECT", "EXECUTE"]` on table level. Principals with table level
permissions do automatically get `USE_SCHEMA` on schema level.

It is possible to add schemas that do not yet exist in the catalog. In this
case, the pipeline will skip this schema, but not raise an error. This allows us
to pre-configure the access for schemas and once they are created, the pipeline
will update the permissions the next time it is run.

For example, we configure grants for the schema `silver_data`, because we are
planning to create this in the next sprint. Since the schema does not yet exist,
the IaC pipeline will skip configuration of grants for this schema. Once we
created the schema and run the pipeline, it will update the permissions we
configured earlier.

> The pipeline is set up to overwrite any permissions on the schemas that are
> not explicitly configured. Any manual changes outside of the configuration
> will be overwritten when the pipeline is executed.

### remote.yml

This config file contains information about remote Terraform states that are
used in the deployment. This should not be changed unless you need to access
other upstream Terraform states.

The file contains details how to locate and access an upstream Terraform state
file.

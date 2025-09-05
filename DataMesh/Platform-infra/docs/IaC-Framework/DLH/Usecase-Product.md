# Usecase Product

The usecase product solution deloys a usecase product's schemas and configures
grants on them.

## Config Files

The config files are located in `config/<env>/668-dlh/<usecase_product_name>`,
where `<env>` is one of dev, tst, acc, prd.

### usecase_product.yml

This config file contains general configuration for the usecase product, namely
the name, shortname and owners. It is automatically deployed by the bootstrap
solution.

### owned_schemas.yml

This config contains the owned schemas of a usecase product. It follows this
structure:

```yaml
<schema_name>:          # Name of the schema
  storage_account: ""   # Storage account name
  container_name: ""    # Storage container name
  location: ""          # Location on the storage container
```

For each schema, the managed schema location needs to be configured by providing
the storage account, storage container and storage location.

### grants.yml

This config contains the privileges granted for the schemas of a usecase
product. This config file is located in the usecase product's repository under
`config/<env>/` It follows this structure:

```yaml
schema_name_1:  # Name of the schema to be configured
  grants:       # A map of principals and the granted permissions
    "group_name": ["SELECT"]
    "service_principal_app_id": ["SELECT"]

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

Only schemas that are in the `owned_schema.yml` config file are considered,
other configurations are ignored.

> The pipeline is set up to overwrite any permissions on the schemas that are
> not explicitly configured. Any manual changes outside of the configuration
> will be overwritten when the pipeline is executed.

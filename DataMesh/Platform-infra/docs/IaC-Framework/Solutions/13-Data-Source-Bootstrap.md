# Data Source Bootstrap

> :warning: This solution should ony be deployed once per data source.

In this solution, configuration files and DevOps pipeline definitions for a data
source are pushed to the `wind-da-data-sources` repository on a new branch.
DevOps pipelines are registered and pipeline authorizations and permissions are
set.

## Configuration

The configuration of the data source bootstrap module makes an exception to the
DTAP structure of the `config` directory. Instead, the configuration for a
particular data source can be found in the
`config/repositories/13-data_source_bootstrap/<source_name>/` directory.

The general configuration files, that are shared between
`13-data_source_bootstrap` and `20-data_product_bootstrap` are located in the
`repositories` folder. The `devops.yml`, contains information on the DevOps
project and DevOps roles and `environments.yml` specifies environment specific
configurations like subscriptions Ids or service connections. Template files
that are used for the deployment are located in the
`repositories/13-data_source_bootstrap/templates/` folder.

Additionally, for each new data source, a folder needs to be created, where the
Terraform backend configuration file (`13-data_source_bootstrap.tfbackend`) and
the data source specific configuration file (`source.yml`) need to be added. In
the data source configuration file, the name and short name of the new data
source are set, which will be used to create the pipeline file and basic
configuration for the deployment of the data product itself (see
`14-data_source`). In this configuration file, you also specify the DevOps
groups and their roles that will be configured for the data product.

```yaml
name: "<data_source_name>"              # Used for Repository folder, schema and container in ADLS
short_name: "<data_source_short_name>"  # Short name for resources with strict name length - Max 12 characters
groups:                                 # Examples for DevOps Groups and their roles
  "<data_source_name>-reader":
    role: reader
  "<data_source_name>-contributor":
    role: contributor
  "<data_source_name>-owner":
    role: owner
```

The `name` and `short_name` of the data source are used to name various
resources belonging to the data source. Both names should use snake case. The
`short_name` is used in resources that have strict requirements on the maximum
length. It must be no longer than 12 characters.

The possible roles can be found in the `devops.yml` configuration file. For each
role, permissions on the `core` repositories are defined, as well as permissions
on the deployment pipelines.

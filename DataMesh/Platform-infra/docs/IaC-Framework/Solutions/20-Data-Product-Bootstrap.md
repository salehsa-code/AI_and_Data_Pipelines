# Data Product Bootstrap

> :warning: This solution should ony be deployed once per data product.

In this solution, a new DevOps repository for the data product is deployed, from
which the configuration for the actual data product deployments are read and a
default configuration is created in the repository. Additionally, a new
deployment pipeline for the data product is created in DevOps. New DevOps groups
are created for the data product and permissions on the new repository and
deployment pipeline are configured. Finally, new branch is opened in the
`wind-da-platform-infra` repository, including the configuration for the remote
state and the pipeline definition for the deployment of the data product
infrastructure.

## Configuration

The configuration of the data product bootstrap module makes an exception to the
DTAP structure of the `config` directory. Instead, the configuration can be
found in the `repositories/20-data_product_bootstrap/<product_name>/`
subdirectory.

The general configuration files, that are shared between
`13-data_source_bootstrap` and `20-data_product_bootstrap` are located in the
`repositories` folder. The `devops. yml`, contains information on the DevOps
project and DevOps roles and `environments. yml` specifies environment specific
configurations like subscriptions Ids or service connections. Template files
that are used for the deployment are located in the
`repositories/20-data_product_bootstrap/templates/` folder.

Additionally, for each new data product, a folder needs to be created, where the
Terraform backend configuration file (`20-data_product_bootstrap.tfbackend`) and
the data product specific configuration file (`data_product.yml`) need to be
added. In the data product configuration file, the name, short name and used
environments of the new data product are set, which will be used to create the
pipeline file and basic configuration for the deployment of the data product
itself (see `21-data_product`). In this configuration file, you also specify the
DevOps groups and their roles that will be configured for the data product.

```yaml
name: "<data_product_name>"             # Decides e.g., repo name, schema, ADLS container
short_name: "<data_product_short_name>" # Short name for resources with strict name length - Max 12 characters
repo_name: "<data_product_repo_name>"   # Use this, if the repo name should be different from the product name
groups:                                 # DevOps Groups and their roles
  "<data_product_name>-reader":
    role: reader
  "<data_product_name>-contributor":
    role: contributor
  "<data_product_name>-owner":
    role: owner
has_key_vault: <true/false>             # option to deploy a key vault with the data product
```

The `name` and `short_name` of the data product are used to name various
resources belonging to the data product. Both names should use snake case. The
`short_name` is used in resources that have strict requirements on the maximum
length. It must be no longer than 12 characters.

The possible roles can be found in the `devops.yml` configuration file. For each
role, permissions on the `core` repositories and the data product repository are
defined, as well as permissions on the deployment pipelines.

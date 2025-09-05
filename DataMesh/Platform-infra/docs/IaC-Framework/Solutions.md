# IaC Framework Solutions

## Concept

The Wind Data Platform infrastructure is deployed in several stages. Each stage
covers a logically separate part of the infrastructure and subsequent stages
depend on previous stages. The prefix in the stage names reflects the order of
the deployment, e.g. `11-platform_infra` should be deployed before
`12-workspace_config`.

The state of each stage is stored in a backend storage account. Information
from previous stages is accessed using their defined outputs taken from the
remote states.

In the figure below, the architecture of the Wind Data Platform is sketched. In
the next sections, each stage is described in more detail.

![architecture](../.img/architecture.drawio.png)

## Configuration of the IaC Framework

### Config Files

All deployments of the Wind Data and Analytics Platform IaC Framework are
configured using configuration files. These configuration files are in the
`YAML` format and are located in the `config` directory in the [WDAP infra
repository](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-infra).
This directory has folders for each of the dtap environments (`dev`, `tst`,
`acc`, `prd`). In each subdirectory, there are folders for the different
infrastructure solutions. The different configuration files for the terraform
solutions are explained in the respective sections in
[Solutions](./Solutions.md).

### Terraform backend config

In addition to the `YAML` files, there is one `<solution_name>.tfbackend` file
in each solution folder, where the configuration of the remote backend is
stored. See [Terraform State
Management](../iac-framework.md#terraform-state-management).

The backend config files all follow a structure similar to the one shown below:

```hcl
resource_group_name  = "<resource group name>"
storage_account_name = "<backend storage account name>"
container_name       = "tf-state"
key                  = "<unique state key>" # e.g. "dev/workspace_config/state.tfstate"
use_azuread_auth     = true
```

> Note that the backend configuration is set up so that Azure AD authentication
is used to access the storage account, so appropriate permissions (i.e., the
'Storage Blob Data Contributer' role) need to be set on the storage account.

### Remote State Datasource Config

Some solutions use the terraform state of another deployment as an additional
datasource. In those cases, there is a `remote.yml` configuration file in the
config directory.

```yaml
# A map of remote data source objects
<identifier>:             # Key is used as terraform internal identifier
  resource_group_name:    # Resource Group where remote state is stored
  storage_account_name:   # Storage account name where remote state is stored
  container_name:         # Storage container name where remote state is stored
  key:                    # Path to the remote state file
  use_azuread_auth:       # Use OAuth to authenticate with the storage account. Should be true unless key-based access is required.
```

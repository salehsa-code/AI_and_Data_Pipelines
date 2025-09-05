# Backend Storage

This Terraform solution holds the configuration of the backend storage account.
When it is first deployed, it needs to be bootstrapped using the
`bootstrap_backend_storage.sh` shell script. The script executes the Terraform
configuration locally and after deployment moves the state file to the newly
created storage account.

After the backend storage account is deployed, make sure that the deployment
principal is given the role of "Storage Blob Data Contributor" on this account
in order to create and update the state files.

**Important**, the resources deployed in this solution are used to store the
state files of all Terraform deployments for the data platform. Do not change or
delete these unless you know what you are doing!

## Configuration

The configuration for the backend storage deployment consists of the
configuration for the storage account (`storage_account.yml`) and one for the
storage container (`container.yml`).

`storage_account.yml` (see inline comments for description):

```yaml
storage_account:
  resource_group_name:      # Name of the storage account resource group. Needs to exist before deployment
  name:                     # Name of the storage account
  account_tier:             # Storage Account Tier, Standard or Premium
  account_replication_type: # Storage Account Replication Tier, e.g. LRS, ZRS, etc.
  is_hns_enabled:           # Decides if the Storage Account is deployed with the hierarchical namespace feature enabled, required for the use as data lake
  allowed_subnets:          # A map of subnet objects that are whitelisted for the storage account. See example structures below.
    # Configuration using vnet and resource group. Only works if deployment service principal has at leas read access on this resource.
    <subnet1_name>:         # Use the subnet name as key of the object
      vnet_name:            # VNet name of the subnet
      resource_group_name:  # Resource Group where the VNet is deployed
    # Configuration using resource Id. Use this when the service principal does not have read access on the subnet.
    <subnet2_name>:         # Use the subnet name as key of the object
      resource_id:          # Azure resource Id of the subnet.
  private_link_access:      # A list of private link endpoints that are allowed network access to the storage account
    - endpoint_resource_id: # Azure resource Id of the private endpoint
      endpoint_tenant_id:   # Azure tenant Id of the private endpoint. Usually this is the Vattenfall tenant.
```

`container.yml`:

```yaml
# A map of storage container objects
<container_name>: # Key of the object. Only used internally in terraform
  name: # Name of the storage container
```

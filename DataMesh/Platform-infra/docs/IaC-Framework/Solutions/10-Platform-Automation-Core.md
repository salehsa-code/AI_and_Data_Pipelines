# Platform Automation Core

This is a terraform solution for the deployment of the core automation
infrastructure of the Wind Data Analytics Platform. It is meant to be deployed
manually, since it requires permissions on Entra ID that our build service does
not have, but we have as a7 users - that means there is not Azure DevOps
pipeline to run this deployment. The solution includes the deployment of Service
Principals and Entra Id Groups used for automation purposes.

## Configuration

The configuration for this solution is stored in
`confgi/<env>/10-platform_automation_core/` and consists of the
`security_groups.yml` and `service_principals.yml` files.

`security_groups.yml`:

```yaml
# A map of group objects
<identifier>:             # The key is only used internally in terraform
  name:                   # Name of the Entra ID group
  owners:                 # Owners of the group. Owners can be of the kind `group`, `service_principal` and `uami` (User Assigned Managed Identity)
    groups:               # A list of groups. Each member of the group becomes owner, since groups cannot be directly be appointed Service Principal owner.
      - <entra_id_group_name>
      - ...
    service_principals:   # A list of service principals that become owners
      - <service_principal_name>
      - ...
    uamis:                # A list of user assigned managed identity objects that become owners.
      # Configuration using name and resource_group of the managed identity. This is the prefered method, but only works if the managed identity is in the same subscription as the service principal.
      - name: <uami_name>
        resource_group: <uami_resource_group_name>
      # Configuration using name and principal Id. This can be used in cases where the above method does not work.
      - name: <uami_name>
        principal_id: <uami_principal_id>
      - ...
  members:                # Optional. A list of entra Id users (use the full user name with email address) that are members of the group.
                          # If members is set, Terraform will overwrite any other group members, so set this only for groups that should be only managed by this solution.
    - ...
```

`service_principals.yml`:

```yaml
# A map of service principals objects
<identifier>:               # The key is only used internally in terraform
  name:                     # Name of the service principal
  owners:                   # Owners of the group. Owners can be of the kind `group`, `service_principal` and `uami` (User Assigned Managed Identity)
    groups:                 # A list of groups. Each member of the group becomes owner, since groups cannot be directly be appointed Service Principal owner.
      - <entra_id_group_name>
      - ...
    service_principals:     # A list of service principals that become owners
      - <service_principal_name>
      - ...
    uamis:                  # A list of user assigned managed identity objects that become owners.
      # Configuration using name and resource_group of the managed identity. This is the prefered method, but only works if the managed identity is in the same subscription as the service principal.
      - name: <uami_name>
        resource_group: <uami_resource_group_name>
      # Configuration using name and principal Id. This can be used in cases where the above method does not work.
      - name: <uami_name>
        principal_id: <uami_principal_id>
      - ...
```

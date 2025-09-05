# Secret Rotation

This is a python-based container app running as a scheduled job. It will
periodically check all secrets in the assigned key vaults for expiring secrets
and rotate them.

Secrets that should be rotated need to be valid, otherwise the secret rotation
will fail to rotate the secret. This is to ensure that no access to secrets can
be gained by users that should not have access to the secret.

Currently, the following secret types are supported by the automatic secret
rotation:

- Entra Id App Secrets
- Log Analytics Workspace Secrets
- Log only - no rotation, but logging of secret expiration

> :bulb: New secret types can be added if required. Please contact the
> Data Kong team with your request to align on the implementation.

## Secret Tags

### General Tags for all Secrets

1. `rotate_secret`: Determines whether the secret should be rotated or ignored.
    Values: "true" - otherwise ignored. *(Required)*
2. `object_type`: Stores the object type for each secret to determine handling.
    Values: *(Required)*
    - `azure_ad_app_secret`: For Azure AD application secrets.
    - `law_shared_key`: For Log Analytics Workspace Shared Key.
    - `log_only`: Only creates a log entry for expiring secret.

### Azure AD App Secret Specific Tags

1. `app_object_id`: Stores the object Id of the Azure AD application.
1. `credential_display_name`: Stores the credential display name.
1. `app_id`: The client Id (also known as application Id) of the Azure AD
   application.

### Log Analytics Workspace Specific Tags

1. `subscription_id`: Id of the Subscription the LAW is deployed to.
1. `resource_group_name`: Name of the Resource Group the LAW is deployed to.
1. `workspace_name`: Name of the LAW resource.
1. `workspace_id`: Id of the LAW resource.

### Only Log Expiring Secrets

No additional tags required.

## Technical Description

### Requirements

- Python 3.11

### Kubernetes Architecture

The secret rotator is an application with a cron job that runs the secret rotation
python package on a fixed schedule, e.g. once a day.

![architecture](/docs/.img/VCS/cronjob_base.drawio.png)

### Helm Chart

The Helm chart for the secret rotation app deploys the above described resources. It has the following parameters:

```yaml
imageTag: <string>                      # Tag of the container image
serviceAccountName: <string>            # Name of the Service Account with Workload Identity used for the secret rotation
key_vault_names: <string>               # A comma separated list of key vault names that should be checked
secretExpiryThreshold: <int>            # Number of days until expiry, when a secret should be rotated
rotationSchedule: <string>              # cron-string defining the schedule of the secret rotator
managedIdentityClientId: <string>       # client-id of the Managed Identity used in the Workload Identity
tenantId: <string>                      # Tenant Id
```

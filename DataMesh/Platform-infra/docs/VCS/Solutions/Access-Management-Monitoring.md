# Access Management Monitoring

This is a python-based container app running as a scheduled job. It will
periodically run the access management monitor app to scrape the permissions on
all configured resources and services and log them to a Log Analytics Workspace.
See the [Access Management
Monitor](../../Access-Management/Access-Management-Monitor.md) documentation for
more details.

## Technical Description

### Requirements

- Python 3.11
- (optional) ArgoCD with ApplicationSet in every namespace configured

### Kubernetes Architecture

An application set deploys applications with a cron job that runs the access
management monitoring on a fixed schedule, e.g. once a day. The application set
is configured to deploy an instance of the app from the `main` branch of the
connected repository, as well as temporary instances for each branch matching
the pattern `feature/k8s/amm/.*`. These temporary apps will be redeployed after each
commit on the given feature branch and deleted, if the feature branch is merged
or delete. Additionally, the cron job on the temporary app is suspended and can
only be triggered manually.

![architecture](/docs/.img/VCS/cronjob_base.drawio.png)

> :bulb: If ApplicationSet cannot be used, the access management
> monitoring can be deployed as a normal app.

### Helm Chart

The Helm chart for the access management monitoring app deployes the above described resources. It has the following parameters:

```yaml
imageTag: <string>                  # Tag of the container image
serviceAccountName: <string>        # Name of the Service Account with Workload Identity used for the secret rotation
schedule: <string>                  # cron-string defining the schedule of the access management monitoring scraper
managedIdentityClientId: <string>   # client-id of the Managed Identity used in the Workload Identity
```

# WDAP Service Accounts on VCS

We use [Service Accounts](https://kubernetes.io/docs/concepts/security/service-accounts/)
on the VCS AKS cluster for Center Court. The service accounts are configured as
[Workload Indentities](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview?tabs=dotnet)
and linked to user assigned identities on Azure using federated identity
credentials.

A service account can be linked to multiple managed identities. In this case the
client id of the managed identity that should be used must be specified in the
app when getting an access token.

## Workload Identities

The following Workload Identities are deployed:

| Service Account Name | Connected User Assigned Identity |
| --- | --- |
| `wdap-cicd-identity` | **`vap2-<env>-wind-cicd-uami`**, `vap2-<env>-wind-devops-uami` ,`vap2-<env>-wind-sr-uami`, `vap2-<env>-wind-acl-uami` |

## Using a Workload Identity in Azure Credentials

There are a few options to use a workload identity in an app for an Azure
credential. The `DefaultAzureCredential` will attempt to use the
`WorkloadIdentityCredential`. It is also possible to use the
`WorkloadIdentityCredential` directly or as part of a `ChainedTokenCredential`.

Alternatively, the Workload Identity can be used with the Az CLI using the
following command:

``` bash
az login \
  --service-principal \
  -u $AZURE_CLIENT_ID \
  -t $AZURE_TENANT_ID \
  --federated-token "$(cat $AZURE_FEDERATED_TOKEN_FILE)" \
  --allow-no-subscriptions
```

The `AZURE_FEDERATED_TOKEN_FILE`, `AZURE_CLIENT_ID` and `AZURE_TENANT_ID` are
automatically set in the container by Kubernetes. `AZURE_CLIENT_ID` is the
default managed identity of the service account. In case another managed
identity is required, the correct client id should be provided in above command.

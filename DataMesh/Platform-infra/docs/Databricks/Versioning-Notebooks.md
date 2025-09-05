# Versioning of Notebooks

As *Data Kongs* we have decided, that our approach for Notebook CI/CD is to use
version-controlled source code in a Databricks job. This new Databricks feature
is documented
[here](https://docs.databricks.com/en/workflows/jobs/how-to/use-repos.html).
Instead of deploying Notebooks between environments, this will allow us, to
point the job to a git ref (branch, tag, commit). Before it starts the job will
clone the repository and source the defined version of the Notebook(s).

~~To make full use of this feature, we're using the relatively new feature of
Azure DevOps, to add Service Principals and Databricks OAuth Authentication with
Azure DevOps.~~ Unfortunately OAuth Authentication with Azure DevOps for Service
Principals is not yet possible. We have tested all setups and made sure the
Service Principal has a Basic License & permissions on the project. We have
tested the OAuth token for the Service Principal with the Azure DevOps REST API
to confirm, that is has sufficient permissions. [This thread in the Databricks
forum](https://community.databricks.com/t5/data-engineering/how-to-use-databricks-repos-with-a-service-principal-for-ci-cd/td-p/11789/page/2)
describes the issue and might in the future be updated, when it is resolved.

Instead of OAuth Authentication, we opted for a DevOps PAT, as the only
alternative. A PAT is problematic for two reasons:

1. It can expire
2. It is bound to a user

## Defining the Job

To use a git source for a job, a `git_source` must be defined. Here is an
example:

```json
"git_source": {
    "git_url": "https://dev.azure.com/<org-name>/<project-name>/_git/<repo-name>",
    "git_provider": "azureDevOpsServices",
    "git_tag": "<tag-name>"
}
```

## Authentication with Azure DevOps

Service Principals can be added to an Azure DevOps Organization. The job will
use the `run_as` principals `git_credential`. Therefore, the Service Principal
must be added to the Organization, have permissions on the project and
repository AND have a Basic DevOps License.

The git credential for the Service Principal in Azure Databricks must be created
via the REST API. It would be preferable to use an OAuth Credential, but this is
currently not supported by Databricks. Therefore, a PAT must be used. Preferably
this is a PAT of a technical account (e.g. s7). Service Principals, Managed
Identities etc. can't create PATs in Azure DevOps.

```bash
# Variables
CLIENT_ID_DATABRICKS="<application-id>"
CLIENT_SECRET_DATABRICKS=<secret-to-everyone>
WORKSPACE=<workspace-identifier> # format: adb-123456789012345.6

# Get OAuth Token
TOKEN_ENDPOINT_URL="https://$WORKSPACE.azuredatabricks.net/oidc/v1/token"
TOKEN_DATABRICKS=$(curl -s --request POST \
    --url $TOKEN_ENDPOINT_URL \
    --user "$CLIENT_ID_DATABRICKS:$CLIENT_SECRET_DATABRICKS" \
    --data 'grant_type=client_credentials&scope=all-apis' |
    jq .access_token | tr -d '"'
)

# Create OAuth Credential for the Azure DevOps integration
# THIS DOES CURRENTLY NOT WORK, SEE INTRO
curl -s --request POST --header "Authorization: Bearer $TOKEN_DATABRICKS" "https://$WORKSPACE.azuredatabricks.net/api/2.0/git-credentials" --data '{
    "git_provider":"azureDevOpsServicesAad"
    }'

# Create PAT-Credential for the Azure DevOps integration
curl -s --request POST --header "Authorization: Bearer $TOKEN_DATABRICKS" "https://$WORKSPACE.azuredatabricks.net/api/2.0/git-credentials" --data '{
    "git_provider":"azureDevOpsServices",
    "git_username":"<username>",
    "personal_access_token":"<pat>"
}'
```

> Unless the Service Principal has an RBAC Assignment on the Databricks
> Workspace as "Contributor", the secret used, must be a Databricks native
> secret, that can be created from the Admin Settings in the GUI. Follow [This
> Databricks
> guide](https://docs.databricks.com/en/dev-tools/auth/oauth-m2m.html) for
> instructions on how to create secrets. This is a good alternative to an RBAC
> assignment, because it allows Service Principals, that are not Workspace
> Administrators to use this feature.

## Messages in the Context of Azure DevOps Authentication from Databricks

> Tested the git credentials by creating a repository with the Service Principal
> via REST API.

```bash
 curl -s --request POST --header "Authorization: Bearer $TOKEN_DATABRICKS" -d '{
   "url": "https://dev.azure.com/<organization>/<project>/_git/wind-da-data-sources",
   "provider": "azureDevOpsServices",
   "path": "/Repos/<directory>/<repo_name>"
 }' "https://$WORKSPACE.azuredatabricks.net/api/2.0/repos" | jq
```

### User without a DevOps License

```json
{
  "error_code": "BAD_REQUEST",
  "message": "Remote repo not found. Please ensure that:\n1. Your remote Git repo URL is valid.\n2. Your personal access token or app password has the correct repo access."
}
```

### Service Principal with OAuth git Credential and Entra Id Token

```json
{
  "error_code": "PERMISSION_DENIED",
  "message": "Invalid Git provider credentials. Go to User Settings > Git Integration to ensure that:\n1. You have entered a username with your Git provider credentials.\n2. You have selected the correct Git provider with your credentials.\n3. Your personal access token or app password has the correct repo access.\n4. Your personal access token has not expired.\n5. If you have SSO enabled with your Git provider, be sure to authorize your token."
}
```

### Service Principal with OAuth git Credential and Databricks Secret Token

```json
{
  "error_code": "PERMISSION_DENIED",
  "message": "Encountered an error with your Azure Active Directory credentials. Please try logging out of Azure Active Directory (https://portal.azure.com) and logging back in."
}
```

### Success Message

```json
{
  "id": 1234567890,
  "path": "/Repos/testrepo/sources",
  "url": "https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-data-sources",
  "provider": "azureDevOpsServices",
  "branch": "main",
  "head_commit_id": "a58fc8b2a9371845794baa5ba8d723d96816825e"
}
```

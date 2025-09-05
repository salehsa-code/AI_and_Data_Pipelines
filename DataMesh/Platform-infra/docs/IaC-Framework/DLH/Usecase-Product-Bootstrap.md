# Usecase Product Bootstrap

The usecase product bootstrap solution handles the initial deployment of DevOps
infrastructure for a new usecase product.

The scope of this deployment is the creation of a new DevOps repository, initial
setup of the new repository including baseline config files and permissions, and
the setup of DevOps build pipelines for the usecase product.

> :warning: This solution should ony be deployed once per usecase product.

## Config Files

The config files are located in
`config/repositories/667-dlh/<usecase_product_name>`.

### usecase_product.yml

This config file contains all the information required for the initial setup of
a new usecase product. It follows this structure:

```yaml
name: ""                # Name of the usecase product. Used for the repo name
short_name: ""          # Short Name of the usecase product. Used for DevOps environments
default_branch: "main"  # Default branch of the repository
owner:
  dev: ""               # Owner Principal of the UC objects. Should usually be the ETL principal
  tst: ""
  acc: ""
  prd: ""
etl_principal:
  dev:
    app_id: ""          # Application Id of the ETL principal
    secret_name: ""     # Name of the ETL principal secret in the ATM key vault.
  tst:
    app_id: ""
    secret_name: ""
  acc:
    app_id: ""
    secret_name: ""
  prd:
    app_id: ""
    secret_name: ""
permissions:            # Configuration for DevOps permissions
  <DevOps Group Name>:  # Name of the group.
    role: ""            # Name of the role.
```

Currently, three DevOps roles are defined in the IaC Framework "owner",
"contributor", and "reader". Each role gets read access on the WDAP core
repositories, additionally, these permissions are granted on the usecase product
repo and pipelines:

| Role        | Repository Permissions       | Pipeline Permissions             |
|-------------|------------------------------|----------------------------------|
| **Owner**   | Administer                   | ViewBuilds                       |
|             | GenericRead                  | EditBuildQuality                 |
|             | GenericContribute            | RetainIndefinitely               |
|             | ForcePush                    | ManageBuildQualities             |
|             | CreateBranch                 | UpdateBuildInformation           |
|             | CreateTag                    | QueueBuilds                      |
|             | ManageNote                   | ManageBuildQueue                 |
|             | RemoveOthersLocks            | StopBuilds                       |
|             | PullRequestContribute        | ViewBuildDefinition              |
|             |                              | OverrideBuildCheckInValidation   |
| **Contributor** | GenericRead              | ViewBuilds                       |
|             | GenericContribute            | QueueBuilds                      |
|             | CreateBranch                 | ManageBuildQueue                 |
|             | CreateTag                    | StopBuilds                       |
|             | ManageNote                   | ViewBuildDefinition              |
|             | PullRequestContribute        |                                  |
| **Reader**  | GenericRead                  | ViewBuilds                       |
|             |                              | ViewBuildDefinition              |

## Import existing Repo from vattenfallwind DevOps Org

Many of the usecase products have existing repositories in the vattenfallwind
DevOps organization. These can be imported to the VDP-DevOps organization and
onboarded to the usecase product bootstrap solution.

First import the repo to the new DevOps org:

1. Create a new empty repository in the VDP-DevOps org. Make sure to not deploy
   a readme or gitignore file - the repository must be completely blank.
2. Go to the repository you want to import on the vattenfallwind org and click
   on clone. Click on Generate Git Credentials, to get a token for the import.
![clone dialog](../../.img/screenshot_devops_clone.png)
3. Go back to the blank repository and select "Import a repository". Tick the
   "Requires Authentication" box and enter the URL and credentials obtained in
   the previous step.

Then import the git repository into the terraform state:

1. Prepare the config files like normal. See above for a description of the
   config files.
2. Make a plan using the deployment script, but do not deploy anything (answer
   no when prompted if you want to apply the plan).
3. Import the repository into the state using: `terraform import
   module.devops_repository.azuredevops_git_repository.this
   d5ac9cb0-65b2-46d5-b47e-ecc749e2f89d/<repo_id>` (the first UUID is the DevOps
   Org Id). You can obtain the `repo_id` by going to the repositories on the
   project settings page and clicking on the desired repo. The repo Id is
   displayed in the URL: ![devops_url](../../.img/devops_url_repo_id.png)
4. Proceed with the deployment as normal.
   - Make sure to disable any branch policies on the main branch for the
     deployment, so that terraform can directly push the new config files there.

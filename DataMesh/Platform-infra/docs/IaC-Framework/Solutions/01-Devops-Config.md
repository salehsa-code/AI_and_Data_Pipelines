# Azure DevOps Configuration

This Terraform solution holds the configuration of the core Azure DevOps
repositories. It allows you to manage branch policies and permissions for these
repositories. The main DevOps project environments used for deployments done by
the Data Kong team (`dev`, `tst`, `acc`, `prd`) are deployed as well.

## Configuration

The configuration files for the configuration of the core repositories can be
found in `config/repositories/core_repositories/`. Update the files for the different
repositories according to your needs. Add one file for each repository that
should be configured in this solution.

The general schema of the config files is:

```yaml
<repository_name>:    # Use the name of the repository as key
  branch_policies:    # Configration for branch policies.
    # See below
  permissions:        # Configuration for permissions on the repository.
    # See below
```

The following settings can be customized
using this terraform solution:

### Branch Policies

Branch policies are defined on a per branch basis. They follow this schema:

```yaml
branch_policies:
  <branch ref>: # Branch ref, e.g., 'refs/heads/main'
    # [branch policy options, see below]
```

**match_type**:

The match type to use when applying the policy. Supported values are 'Exact', 'Prefix' or 'DefaultBranch'.

```yaml
match_type: string [Exact|Prefix|DefaultBranch]
```

**comment_resolution**:

This policy, when enabled and set to blocking, requires all comments to be resolved before a Pull Request (PR) can be closed.

```yaml
enabled: bool
blocking: bool
```

**work_item_linking**:

This policy, when enabled and set to blocking, requires a work item to be linked before a PR can be closed.

```yaml
enabled: bool
blocking: bool
```

**min_reviewers**:

This policy, when enabled, requires a minimum number of reviewers to close a PR.

```yaml
enabled: bool
reviewer_count: int
submitter_can_vote: bool (Allow requesters to approve their own changes.)
last_pusher_cannot_approve: bool (Prohibit the most recent pusher from approving their own changes.)
allow_completion_with_rejects_or_waits: bool (Allow completion even if some reviewers vote to wait or reject.)
on_push_reset_approved_votes: bool (When new changes are pushed reset all approval votes (does not reset votes to reject or wait).)
```

**allowed_merge_types**:

This policy defines the allowed merge types for the branch. Can include any of the below defined merge types.

```yaml
[- squash]
[- rebase_and_fast_forward]
[- basic_no_fast_forward]
[- rebase_with_merge]
```

**build_validation**:

This policy defines a set of Pipelines to successfully run befoer a PR can be closed.

```yaml
<build_definition_name>:
    build_definition_name: string
    blocking: bool
    display_name: string
    valid_duration: int (Minutes)
    filename_patterns: list (allows wildcards, e.g. '/terraform/*)
```

### Permissions

The setting of permissions follows a role concept. Each DevOps team can be
assigned a role on the repository. The configuration follows this schema:

```yaml
permissions:
  <team name>:    # Use the DevOps team name as key
    role:         # Name of the role that should be assigned.
```

The possible roles to choose from are defined in the
`config/repositories/devops.yml`. The role definition has this schema:

```yaml
roles:                # A map of role objects
  <role_name>:        # Use the role name as key. This is the name you put in the config above.
    repositories:     # A list of repository permissions assigned to the role. See below for the distinction between 'core' and 'data_product' permissions.
      core:
        - string
      data_product:
        - string
    pipeline:         # A list of DevOps pipeline permissions assigned to the role for pipelines related to the deployed repository.
      - string
```

The roles distinguish between `core` and `data_product` permissions on the
repository. This is to set appropriate permissions for data product
repositories, while allowing those roles also some permissions on the core
repositories (usually read-only access). In the context of this deployment, the
`data_product` permissions are applied to the configured repositories.

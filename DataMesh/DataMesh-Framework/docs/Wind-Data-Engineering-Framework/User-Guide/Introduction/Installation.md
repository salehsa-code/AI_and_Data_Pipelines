# Installation

This section provides instructions on how to install the Wind Data Engineering Framework.

## Prerequisites

Before you can install the Wind Data Engineering Framework, you need to meet the following prerequisites:

- Access to the internal Artifactory repository.
  - The s1 user with access is defined in the `vap2-<env>-winddata-dbx-kv` key
    vaults, with the secrets `jfrog-user` and `jfrog-secret`.
  - On WDAP-clusters the key vault is defined as key vault backed secret scope
    under the name of `ss-kv-winddata-dbx` with read access for every user of
    the platform.
  - Additionally the secrets are available as environment
    varibles on WDAP-Clusters as `JFROG_USER` and `JFROG_SECRET`.
- To use the framework to its full extent, you need to be on a Databricks
  Workspace that is onboarded to a Metastore, because some features require
  Unity Catalog or use UC-specific syntax or features. Some features can be used
  regardless of UC.

## Installation from jFrog Artifactory

Installing WinDEF from the internal Artifactory repository on WDAP is easy. You can install the package using the following code in a Databricks notebook:

```bash
%pip install windef # specify a version if needed
```

:warning: **Note:**

Make sure to restart the python kernel after the installation. This is required,
because WinDEF installs some dependencies in other versions than the default
ones on the Databricks clusters.

```bash
dbutils.library.restartPython()
```

## Installation from Source

It can be advantageous to install WinDEF from source (a Databricks repository),
if you are actively developing the framework or if you want to use a version
that is not yet available in the Artifactory repository.

This can be done by cloning the repository and installing the package from the local source:

```bash
%pip install /path/to/windef  # e.g. /Workspace/Repos/a7bet60@eur.corp.vattenfall.com/wind-da-engineering-fw
```

> :warning: Mind, that you need to restart the python kernel after the
> installation, see [above](#installation-from-jfrog-artifactory).

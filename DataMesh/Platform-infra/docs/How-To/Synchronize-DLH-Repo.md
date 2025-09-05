# How to Synchronize the DLH-ETL Repo with the legacy Jobs Repo

## Prepare your local Repo

Clone the DLH-ETL repo

```sh
git clone git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/dlh-etl
```

Add the legacy Jobs Repo as a second remote repo

```sh
git remote add legacy vattenfallwind@vs-ssh.visualstudio.com:v3/vattenfallwind/WIND-DataAnalytics/jobs
```

Verify that both repos are configured as remote for your local repo:

```sh
git remote -v

    legacy  vattenfallwind@vs-ssh.visualstudio.com:v3/vattenfallwind/WIND-DataAnalytics/jobs (fetch)
    legacy  vattenfallwind@vs-ssh.visualstudio.com:v3/vattenfallwind/WIND-DataAnalytics/jobs (push)
    origin  git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/dlh-etl (fetch)
    origin  git@ssh.dev.azure.com:v3/VDP-DevOps/VAP2-WIND-DataAnalytics/dlh-etl (push)
```

## Synchronize Dev Branch

First, fetch the latest remote changes

```sh
git fetch legacy
git fetch origin
```

Create a new sync branch from the legacy dev branch

```sh
git checkout -b sync/20241029-dev legacy/dev
```

Push the sync branch to the new repo

```sh
git push origin
```

Open a PR for the sync branch to Dev and proceed like with a normal feature branch.

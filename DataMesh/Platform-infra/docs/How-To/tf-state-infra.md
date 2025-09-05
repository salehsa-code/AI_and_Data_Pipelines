# Deploying the infrastructure for the remote backend

The Terraform configuration for the storage account used to persist Terraform
states is in the [00-backend_storage](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-infra?path=/terraform/00-backend_storage) solution.

The deployment can be configured in `/config/<env>/00-backend_storage`, e.g.
[/config/dev/00-backend_storage](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics/_git/wind-da-platform-infra?path=/config/dev/00-backend_storage)

Deployment of the backend storage is only necessary once, when setting up a new
environment. All state files in one environment are stored on this central
storage account.

To deploy the infrastructure, run the following commands:

``` sh
cd terraform/00-backend_storage
bash bootstrap_backend_storage.sh <environment>
```

The script will deploy the resources required for the remote backend and store
the remote state in those resources.

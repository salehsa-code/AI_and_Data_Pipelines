# Onboarding

This document defines the steps required to onboard colleagues into the project.

## Requirements

Colleagues need access to the Vattenfall network, either via VPN or VM.

## Software

Software can be requested via the IT Service Portal (**ITSP**) *accessible via
edge browser on Vattenfall hardware*.

Colleagues require at least:

- Git for Windows
- Visual Studio Code

## Git

To clone a repository, use a ssh connection (see MS reference: [Use SSH key
authentication](https://learn.microsoft.com/en-us/azure/devops/repos/git/use-ssh-keys-to-authenticate?view=azure-devops)).
Or configure the proxy information on your machine.

## Developer VM

It is easiest to work on a Developer VM. This can be ordered by the PO and must
be deployed in `wind-dev-dlhinfra-we-rg`, since VDP does not support Developer
VMs anymore.

To install Python packages on the VM using poetry, you must set the
authentication:

```shell
# add a new source -- this will be stored in the pyproject.toml
poetry source add --priority=supplemental foo https://pypi.example.org/simple/
# add authentication -- this has to be done by every developer individually
poetry config http-basic.foo <username> <password>
```

## Permission

### Developer

Access to Azure development environment, including ADLS (**bypass Unity
catalog!**) `z_azu_vap2_devtst_dev_winddata_contrib__a`

Access to [DevOps
project](https://dev.azure.com/VDP-DevOps/VAP2-WIND-DataAnalytics) as
contributor `z_azu_vsts_VAP2-WIND-DataAnalytics_contrib__a`

#### Relevant VMs

Access to VMs is granted to members of this AD group: `o1_srv_<VM_Name>__a`.

Relevant VMs are:

- [sacicdd15376](https://portal.azure.com/#@Vattenfall.onmicrosoft.com/resource/subscriptions/45009243-9df4-49ec-8872-8beef91f7db9/resourceGroups/VAP2-DEV-WINDDATA-WE-RG/providers/Microsoft.Compute/virtualMachines/sacicdd15376/overview):
  DevOps Build Agent (DEVTST)
- [sacicda15493](https://portal.azure.com/#@Vattenfall.onmicrosoft.com/resource/subscriptions/36828e24-be68-454f-807c-de4bf8c899c5/resourceGroups/VAP2-ACC-WINDDATA-WE-RG/providers/Microsoft.Compute/virtualMachines/sacicda15493/overview):
  DevOps Build Agent (ACCPRD)

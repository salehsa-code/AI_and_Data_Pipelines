# Vattenfall Container Solutions

The Vattenfall Container Solutions (VCS) team is part of the Vattenfall IT. They
are responsible for the provisioning and management of containerized solutions
and Kubernetes services. In the cloud, they provide either access to a shared
Azure Kubernetes Services (AKS) cluster or can provision a dedicated cluster. In
both cases, a basic setup of the cluster and a user namespace is provided. The
basic setup includes a nginx traffic controller and an ArgoCD instance.

Additionally, repositories on a jFrog artifactory can be ordered by VCS, which
allow access to external package and container repositories mirrors.

## Center Court AKS cluster

For Center Court, dedicated AKS cluster were provisioned:

- cit-dev-vcs-wind-center-court-we-aks (DEV)
- cit-prd-vcs-wind-center-court-we-aks (ACC and PRD)

### Namespaces

Namespaces are a mechanism to isolate groups of resources in a Kubernetes
cluster. In WDAP we operate three namespaces:

- winddata-dev (on DEV cluster)
- winddata-acc (on ACCPRD cluster)
- winddata-prd (on ACCPRD cluster)

## jFrog

Currently in WDAP, there are two jFrog repositories in use:

### winddatacore

The `winddatacore` repository contains repositories used by the WDAP container
solutions.

| repository | type | comment |
| --- | --- | --- |
| `remote-dck-winddatacore-dockerhub` | container | Mirror of Dockerhub |
| `remote-dck-winddatacore-gcr` | container | Mirror of GCR |
| `local-dck-winddatacore` | container | Registry for our own container images |
| `remote-apt-winddatacore-debian` | debian | Mirror of Debian packge repository |
| `remote-apt-winddatacore-security` | debian | Mirror of Debian security packge repository |

The repository can accessed using the S1 user `s1vcswdap`.

### winddata

The `winddata` repository is shared with DLH. For our purposes it is used to
host the Wind Data Engineering Framework and to access pypi packages.

The repository can be accessed using the S1 user `s1winddata`

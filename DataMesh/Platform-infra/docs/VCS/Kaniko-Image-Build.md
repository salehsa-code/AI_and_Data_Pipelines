# Build Docker Images on K8S with Kaniko

We are using [Kaniko](https://github.com/GoogleContainerTools/kaniko) to build
container images from Dockerfiles on our DevOps repositories inside a container
on the VCS Kubernetes cluster. The process can be summarized as shown in the
following diagram:

::: mermaid
sequenceDiagram
    participant D as DevOps Repository
    participant K as Kaniko Container
    participant J as jFrog Artifactory

    K->>D: Clone Repository for build context
    K->>J: Pull base image
    opt Install Dependencies
        K->>J: Pull Debian packages
    end
    K->>J: Push Docker image
:::

The build context (Dockerfile) is cloned from the DevOps repository and stored in
a temporary volume on the VCS Kubernetes cluster. Kaniko is then initializing
the container image build by pulling the specified base image from the jFrog
artifactory. Additional modifications are then applied to the image and
dependencies can be installed from a remote Debian repository on jFrog. The
finished container image is then published to the local container repository on
the jFrog artifactory.

## Kaniko Pipelines

In order to align with the CICD processes in WDAP, containers can be build using
Azure DevOps CICD pipelines. The pipelines will create a Kaniko pod on the VCS
cluster, that builds and publishes the requested image.

### Setup a Kaniko Pipeline

Use the `azure-pipelines.kaniko-build.yml` pipeline template in `build-scripts\k8s\templates\` in your new pipeline.

For example:

```yaml
name: $(BuildDefinitionName)_$(Date:yyyy-MM-dd).$(Rev:r)

parameters:
- name: imageTag
    type: "string"
    default: ""
- name: branchName
    type: "string"
    default: "main"

stages:
- stage: build
    displayName: Build and Publish Container Image
    jobs:
    - template: ./templates/azure-pipelines.kaniko-build.yml
        parameters:
          poolName: WDAP-Build-Dev
          serviceConnection: vap2-devtst-winddata-deployment
          subscriptionName: "Vattenfall Common IT Services DEVTSTPOC"
          resourceGroup: cit-dev-vcs-wind-center-court-we-rg
          kubernetesCluster: cit-dev-vcs-wind-center-court-we-aks
          workloadIdentity: wdap-cicd-identity
          namespace: winddata-dev
          branchName: ${{ parameters.branchName }}
          imagePath: k8s/images/build-agent/
          dockerFile: python-311.Dockerfile
          imageName: build-agent
          imageTag: python-311-$(imageTagVar)
          managedIdentityClientId: "00000000-0000-0000-0000-000000000000"
          storageAccountName: vap2devwinddataappwesa
          appFiles:
            - path: k8s/kubectl
              name: kubectl
            - path: k8s/kubelogin
              name: kubelogin

```

The pipeline template uses the following parameters:

- `poolName`: Name of the DevOps Agent Pool.
- `serviceConnection`: Name of the Azure ARM Service Connection.
- `subscriptionName`: Name of the Subscription of the AKS cluster.
- `resourceGroup`: Resource Group of the AKS cluster.
- `kubernetesCluster`: Name of the AKS cluster.
- `workloadIdentity`: Name of the workload identity used for the init container.
- `namespace`: Namespace in the AKS cluster, where the Kaniko pod will be deployed.
- `branchName`: Branch name from where the container image will be cloned.
- `imagePath`: Relative path to the image build contex.
- `imageName`: Name of the container image.
- `imageTag`: Tag of the container image.
- `dockerFile` (optional): Name of the Dockerfile, defaults to 'Dockerfile'.
- `args` (optional): Additional build arguments passed to the image build.

### Installing binaries

Additionally, it is possible to download specific binaries from a storage
account. The following optional parameters are used to configure this
functionality.

- `managedIdentityClientId` (optional): Client Id of the managed identity used
  to access the storage account. This managed identity must be available as a
  workload identity for the init pod.
- `storageAccountName` (optional): Name of the storage account containing the app files.
- `storageContainerName` (optional): Name of the storage container containing the app files.
- `appFiles` (optional): A list of objects in the form `{"path":
  <path/to/binary>, "name": <name of the binary>}`. Each file will be downloaded
  from the storage account and copied to the build context directory, where it
  can be used when building the image.

For the existing Pipelines, the binaries are stored in the
`vap2devwinddataappwesa` storage account. To e.g., use an updated version of
the Terraform CLI in a container, the binary in the location
`bin@vap2devwinddataappwesa/terraform` has to be exchanged with the desired
version. Afterwards the images that should use the new version must be updated
with the related `container` pipeline, e.g. `build-container-terraform`,
specifying the desired environment as tag, e.g., `dev` or `prd`.

### Docker Images

Kaniko is able to build most Docker images. However, due to security
constraints, only resources from within the Vattenfall network or from trusted
sources can be accessed. Below you find some changes that might help you adapt
your Docker images.

We are able to use a mirror of the debian package repository located on jFrog. To use this, choose a base image using debian and then add these steps at the beginning of your Dockerfile:

```docker
# Copy Vattenfall SSL certificates pre-installed by the init container
COPY certs/ca-certificates.crt /kaniko/ssl/certs/ca-certificates.crt

# Set environment variables for Kaniko and other Services
ENV SSL_CERT_DIR=/kaniko/ssl/certs \
    REQUESTS_CA_BUNDLE=/kaniko/ssl/certs/ca-certificates.crt \
    CURL_CA_BUNDLE=/kaniko/ssl/certs/ca-certificates.crt \
    DOCKER_CONFIG=/kaniko/.docker/

# Remove default package repositories and install jFrog repository
RUN --mount=type=secret,id=jfrog,target=/kaniko/secrets \
cp /kaniko/ssl/certs/ca-certificates.crt /etc/ssl/certs/ca-certificates.crt \
&& rm /etc/apt/sources.list.d/debian.sources \
&& echo "deb [trusted=yes] https://$(cat /kaniko/secrets/jfrog-deb-user):$(cat /kaniko/secrets/jfrog-deb-secret)@registry-se.corp.vattenfall.com/artifactory/remote-apt-winddatacore-debian/debian bookworm main" >> /etc/apt/sources.list \
&& apt-get update -y \
&& apt-get upgrade -y
```

Additionally, you can add the Microsoft package repository, which is accessible from the AKS cluster, e.g. for az-cli:

```docker
# Add Microsoft package repository
RUN mkdir -p /etc/apt/keyrings \
&&  curl -sLS https://packages.microsoft.com/keys/microsoft.asc | \
    gpg --dearmor | \
    tee /etc/apt/keyrings/microsoft.gpg > /dev/null \
&&  chmod go+r /etc/apt/keyrings/microsoft.gpg \
&&  echo "deb [arch=`dpkg --print-architecture` signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/azure-cli/ $(lsb_release -cs) main" | \
    tee /etc/apt/sources.list.d/azure-cli.list; \
    apt-get update \
```

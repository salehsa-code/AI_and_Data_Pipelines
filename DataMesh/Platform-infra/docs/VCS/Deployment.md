# Deployment

## Concept

For the deployment of applications in the WDAP VCS namespaces, the *App-of-Apps*
pattern with ArgoCD is used. This approach allows us to orchestrate the
deployment of multiple applications in a scalable and organized manner.

![app-of-apps](/docs/.img/VCS/app_of_apps_complex.drawio.png)

ArgoCD manages a parent application - the *app-of-apps* - which is responsible
for deploying other applications from the `wind-da-infra` repository. This
repository contains the necessary configuration files for each application.

Each application specifies a Helm chart and the necessary parameters for its
deployment to the Center Court VCS cluster. The Helm charts are define the
Kubernetes resources used by the application.

Applications are defined separately for each environment (DEV, ACC, PRD). While
the same Helm charts are utilized across different environments, the parameters
for each environment might differ, e.g., because different identities are
required. This approach ensures consistency in application deployment while
allowing for environment-specific customizations.

## App Deployment Strategy

Below we highlight a deployment strategy that can be used for app development,
leveraging the most out of our CI/CD workflow and automation.

### Dev

:::mermaid
flowchart LR;
    subgraph ArgoCD
        direction LR
        AppSet--Dynamic Parameters-->Helm--compile-->Manifest
    end
    subgraph DevOps
        direction LR
        Branch1<--Trigger new App Instance-->AppSet
        Branch2<--Trigger new App Instance-->AppSet
    end
    subgraph K8S
        direction LR
        App-Branch1
        App-Branch2
    end
    ArgoCD--Deploy-->K8S
:::

In the development environment, the workflow starts with the creation of
application sets (AppSet) in ArgoCD. The AppSet represents a list of
applications with similar configuration. Each application corresponds to a
different feature branch (Branch1, Branch2) in the DevOps pipeline. The AppSet
deploys Helm charts which generate manifests. These manifests are a collection
of files that describe the resources to be deployed on the Kubernetes (K8s)
cluster. This way, the state of the cluster is managed declaratively. The
applications (App-Branch1, App-Branch2) are then deployed into the Kubernetes
cluster. This enables developers to test and iterate on their changes in a
controlled environment before they are merged into the main branch.

### Acc

:::mermaid
flowchart LR;
    subgraph ArgoCD
        direction LR
        AppSet--Dynamic Parameters-->Helm--compile-->Manifest
    end
    subgraph DevOps
        direction LR
        PR1<--Trigger new App Instance-->AppSet
        PR2<--Trigger new App Instance-->AppSet
    end
    subgraph K8S
        direction LR
        App-PR1
        App-PR2
    end
    ArgoCD--Deploy-->K8S
:::

In the acceptance environment, the workflow is similar to the development
environment. However, instead of feature branches, pull requests (PR1, PR2) are
used. A pull request represents a proposed change to the codebase. The
corresponding applications (App-PR1, App-PR2) are deployed to the Kubernetes
cluster. This allows for the proposed changes to be tested and reviewed before
they are merged into the main branch.

### Prd

:::mermaid
flowchart LR;
    subgraph ArgoCD
        direction LR
        App--Dynamic Parameters-->Helm--compile-->Manifest
    end
    subgraph DevOps
        direction LR
        main--Define PRD App-->App
    end
    subgraph K8S
        direction LR
        App-Prd
    end
    ArgoCD--Deploy-->K8S
:::

In the production environment, the main branch deploys the final, reviewed and
tested version of the application. The application is deployed using ArgoCD,
which again uses Helm to create a manifest. The application is then deployed
into the Kubernetes cluster. This ensures that the production environment is
always in sync with the main branch, reflecting the most recent, stable version
of the application.

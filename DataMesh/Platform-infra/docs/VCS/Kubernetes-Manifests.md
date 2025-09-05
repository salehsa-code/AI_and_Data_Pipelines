# Kubernetes Manifests

Kubernetes manifest files are `YAML` files that contain a detailed description
of the desired state of Kubernetes objects, such as deployments, services and
pods, and their respective configurations, such as container images, resource
requirements, and networking policies.

These manifest files are used by Kubernetes to create and manage these objects
in the cluster. Manifest files should be stored in the repository alongside the
container definition.

The following is a list of the most commonly used resources for our applications
in Kubernetes. For each resource, a brief description is given and a link to the
official documentation is provided:

- **Pod**: Pods are the smallest, most basic deployable objects in Kubernetes.
  They represent a single instance of a running process in a cluster. It
  consists of one or more containers with shared storage/network and a
  specification for how to run the containers.
  [Documentation](https://kubernetes.io/docs/concepts/workloads/pods/).
- **Job**: Jobs manage batch processing and ensure tasks run to completion. They
  are used to run one-time tasks in Kubernetes.
  [Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/job/).
- **CronJob**: CronJobs are used to run tasks on a schedule. Internally, a
  CronJob deploys Jobs in regular intervals.
  [Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).
- **Volume**: Volumes provide a way for containers to access and store data.
  They persist until the corresponding pod is deleted, meaning data persists
  after a pod restart. Secrets can be mounted to a pod from a Secrets Store
  using a special kind of Volume.
  [Documentation](https://kubernetes.io/docs/concepts/storage/volumes/).
- **Service Account**: Service Accounts are identities that can be used by
  processes running in a pod. A service account can be used as a Workload
  Identity, which connects to an Azure Managed Identity, allowing to securely
  access Azure Resources from the pod.
  [Documentation](https://kubernetes.io/docs/concepts/security/service-accounts/),
  [WorkloadIdentity](https://learn.microsoft.com/en-us/azure/aks/workload-identity-overview).
- **Service**: Services expose pods within the Kubernetes cluster internal
  network. They provide a static IP address and DNS name for the pod.
  [Documentation](https://kubernetes.io/docs/concepts/services-networking/service/).
- **Ingress**: Ingress provides access to a Service in a cluster from the
  outside, typically via HTTP. It is connected to an ingress controller - in VCS
  this is by default a nginx service that is deployed and managed by the VCS
  team.
  [Documentation](https://kubernetes.io/docs/concepts/services-networking/ingress/).

## Helm Charts

In WDAP, Helm charts are used to define the Kubernetes resources for any
application. A Helm chart is set of parametrizable Kubernetes manifests. Helm
charts can natively be installed using ArgoCD.

Helm uses the Go template language for templating the Kubernetes manifests. A
guide on how to start creating Helm templates can be found in the [official
documentation](https://helm.sh/docs/chart_template_guide/).

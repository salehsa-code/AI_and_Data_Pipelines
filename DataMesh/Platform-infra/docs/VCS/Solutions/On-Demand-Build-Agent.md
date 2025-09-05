# On-demand Self-hosted Build Agent

> :bulb: Currently, the self-hosted build agent solution is deployed
> using a static number of replicas. Once KEDA is fully functional on our AKS
> clusters, it will be switched to the described workflow.

This solution provides the capability of the platform to deploy on-demand build
agents for DevOps running on the Center Court AKS cluster.

The solution includes different KEDA scalers that watch an agent queue on Azure
DevOps and spin up container jobs that can fulfill the demand of the DevOps
pipeline, run it and terminate after the pipeline finished.

To run a DevOps pipeline using the on-demand self-hosted build agents, you need
to specify the pool name of the self-hosted agents and a capability matching the
agent type you want to use. For example, to run a terraform related pipeline on
the WDAP pool, add this to your pipeline jobs:

```yaml
jobs:
  - job: <name>
    displayName: <display name>
    pool:
      name: WDAP-Build-Dev
      demands: terraform
```

Currently we are supporting the following demands:

- `terraform`: For DevOps pipelines related to the platform infrastructure
  tasks, requiring Terraform.
- `python-311`: For DevOps pipelines using python 3.11

> :bulb: It is easy to add more images and scalers to serve other demands.
> Please approach the *Data Kong* team to align on your requirements.

## Technical Description

### Requirements

- KEDA v2.3+
- DevOps token with permission to manage agent queue

### Kubernetes Architecture

The On-demand DevOps build agent solution makes use of the KEDA scaled job. For
each `demand` a build agent needs to fulfill, a different KEDA scaled job is
configured, watching the agent queue for pipelines with these demands. When a
pipeline queues for a build agent, the KEDA scaled job that can fulfill this
demand will scale up and deploy a new job. The job pulls the correct image from
the container artifactory and starts a build agent.

The KEDA scaled jobs are deployed using a template Helm chart that is rolled out
using an application set.

:::mermaid
graph TD
appset[Application Set \n with list of demands]
subgraph app1[Build Agent App]
  KEDA1[KEDA scaled job \n for Python]
  job1[Python Job]
  KEDA1 --scale-->job1
end
subgraph app2[Build Agent App]
  KEDA2[KEDA scaled job \n for Terraform]
  job2[Terraform Job]
  KEDA2 --scale-->job2
end
appset --python demand--> app1
appset --terraform demand--> app2
:::

### Workflow

The sequence diagram below illustrates the workflow of creating an on-demand
build agent. The KEDA scaled job constantly monitors the assigned agent queue
and triggers new pods to start and register in the agent pool as workers. Once
the pipeline run completes and the agent is released, the KEDA scaled job
triggers the termination of the pod.

:::mermaid
sequenceDiagram
  participant PL as DevOps Pipeline
  participant AQ as Agent Queue
  participant KS as KEDA Scaled Job
  KS->>AQ: Monitors Queue
  PL->>AQ: Queue for Agent
  KS->>AQ: New Build in Queue
  create participant KP as Pod
  KS->>KP: Create new Instance
  KP->>AQ: Register in Pool
  AQ->>PL: Assign Agent
  Note over PL,KP: Pipeline Run completes
  PL->>AQ: Dequeue
  KS->>AQ: Job in Queue finished
  destroy KP
  KS->>KP: Terminate
:::

### Placeholder Agent

DevOps pipelines can only queue in an Agent Queue if there is at least on agent
in the pool that is capable of fulfilling the pipeline demands. However, we want
to be able to scale our running containers down to zero, so we don't have any
unutilized workloads on the K8S cluster. The solution to this is to deploy a
*placeholder agent* to the pool. The placeholder agent has the same capabilities
as the actual agents deployed by the KEDA scaler. The placeholder agent needs to
be deployed once and registered as an agent and then turned offline.

To deploy a placeholder agent, we have a deployment script that needs to be
executed manually once for each new agent type in a pool. The script can be
found in `utils/k8s/deploy_template_agent.sh`. To execute it you need to have
`kubectl` installed and configured for the center-court AKS cluster. See the
[VCS
documentation](https://vattenfall.sharepoint.com/sites/VCSUsergroup/SitePages/Wiki.aspx?OR=Teams-HL&CT=1707395772374&clickparams=eyJBcHBOYW1lIjoiVGVhbXMtRGVza3RvcCIsIkFwcFZlcnNpb24iOiIyNy8yNDAxMDQxNzUwMyIsIkhhc0ZlZGVyYXRlZFVzZXIiOmZhbHNlfQ%3D%3D#access-azure-cluster)
for details on how to set this up.

Run the script using bash:

```sh
bash ./deploy_template_agent.sh --agent <name of the agent> --pool <name of the agent pool> --tag <image tag of the container> --namespace <name of the K8S namespace>
```

> :bulb: Note that the script assumes that the capability assigned to the
> agent is the same as the agent name. If this is not the case, you need to
> modify the script accordingly.

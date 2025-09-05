# Clusters

This article defines how clusters are being used in WDAP.

## Cluster Layout

:::mermaid
graph LR
    A[User]
    B[Service User]

    C1[Job Cluster Policy S]
    E1[Worker Pool S]
    D1[Driver Pool S]
    F1[Node S]

    C2[Job Cluster Policy M]
    D2[Driver Pool M]
    E2[Worker Pool M]
    F2[Node M]

    C1 -- assigned -->  A
    E1 <-- allow list -->  C1
    D1 <-- allow list -->  C1
    F1 -->  E1
    F1 -->  D1

    C2 -- assigned -->  A
    D2 <-- allow list -->  C2
    E2 <-- allow list -->  C2
    E1 <-- allow list -->  C2
    F2 -->  E2
    F2 -->  D2

    AC[...]
    C1 -- assigned --> B
    C2 -- assigned --> B
    AC -- assigned --> B

:::
> Note: An "All Purpose Cluster" is accessible only in the Development
> environment, intended for shared use among developers working on
> development tasks.

As detailed in above graph, the users of the platform are being assigned
Cluster Policies in different T-Shirt sizes. Each Cluster Policy is
defining `instance_pool_id` and `driver_instance_pool_id` as an
allowlist which as a result specify the Pools for Driver and Worker
Nodes that can be used. The `Job Cluster Policy S` for example can use
drivers and workers from the `S`-Pool, while `Job Cluster Policy M`
uses drivers from the `M`-Pool and workers from either the `M` or `S`
Pool.

A Service User (Service Principal) is used to run automated workloads in
all environments. The Service Principal is assigned all Cluster Policies,
i.e., that it could also run Workloads on the L and XL pools.
The Service Principal is authorized to be used by the *Data Kong* team
and the DevOps service connection, that sets it as an owner to all
Jobs. Monitoring of Cluster Usage is in place to avoid the use of
excessively large clusters.

> :warning: Users require Permissions on the Pool AND the Cluster Policy for
> that pool, otherwise they won't be able to create clusters.

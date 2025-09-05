[[_TOC_]]

#Issue description
When a cluster is terminated, detached, or otherwise removed from an active session, it starts its garbage collection. This takes about 5 minutes to complete, which is not an issue on its own. However during this time the cluster is still regarded as available in the pool. If you immediately request a new cluster from the pool with the same specification, the cluster is attached with garbage coming along with it.

#Practical example of issue occuring
You run a notebook with a very heavy workload, the cluster runs out of available memory, and you terminate the session. You make a quick change and request a new session to make a new attempt, but you're given the same cluster back (which has not finished its gc), and you immediately run into memory issues again regardless of the impact of your change.

#Solutions
None as of writing.

#Workarounds
- Wait at least 5 minutes before requesting a new cluster
- Use a different cluster pool
- Make a change to your cluster configuration to force a new cluster.
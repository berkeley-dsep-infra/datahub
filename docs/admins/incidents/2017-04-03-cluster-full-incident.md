# 2017-04-03 - Custom autoscaler does not scale up when it should

## Summary

On April 3, 2017, as students were returning from spring break, the cluster wasn't big enough in time and several students had errors spawning. This was because the simple-autoscaler was 'stuck' on a populate call. More capacity was manually added, the pending pods were deleted & this seemed to fix the outage.

## Timeline

### Over spring break week

The cluster is scaled down to a much smaller size (7 machines), and the simple scaler is left running.

### 2017-04-03 11:32

Students report datahub isn't working on Piazza, and lots of Pods in PENDING state.

Doing a `kubectl --namespace=datahub describe pod <pod-name>` said the pod was unschedulable because there wasn't enough RAM in the cluster. This clearly implied the cluster wasn't big enough.

Looking at the simple scaler shows it was 'stuck' at a populate.bash call, and wasn't scaling up fast enough.

### 11:35

The cluster is manually scaled up to 30 nodes:

```bash
gcloud compute instance-groups managed resize gke-prod-highmem-pool-0df1a536-grp --size=30
```

At the same time, pods stuck in `Pending` state are deleted so they don't become ghost pods, with:

```bash
kubectl --namespace=datahub get pod | grep -v Running | grep -P 'm$' | awk '{print $1;}' | xargs -L1 kubectl --namespace=datahub delete pod
```

### 11:40

The nodes have come up, so a `populate.bash` call is performed to pre-populate all user container images on the new nodes.

Users in Pending state are deleted again.

### 11:46

The populate.bash call is complete, and everything is back online!

## Conclusion

Our simple scaler didn't scale up fast enough when a large number of students came back online quickly after a time of quiet (spring break). Took a while for this to get noticed, and manual scaling fixed everything.

## Action items

### Process

1. When coming back from breaks, pre-scale the cluster back up.
2. Consider cancelling spring break.

### Monitoring

1. Have monitoring for pods stuck in non-Running states

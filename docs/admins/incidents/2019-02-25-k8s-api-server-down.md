# 2019-02-25 - Azure Kubernetes API Server outage causes downtime

## Summary

On February 25, 2019, the kubernetes API server for data100 became unreachable, causing new resource creation requests to fail. When the hub pod was stopped, a new one did not get created leading users to see a proxy error message. The hub came back online after a new cluster was created, storage was migrated to the new cluster, and then DNS was updated.

## Timeline

### 2019-02-25 11:21a

The kubernetes API server became unavailable. The time of this event was determine post mortem via the cloud provider's monitoring metrics.

### 11:34

Infrastructure staff is notified in slack. It is determined that the hub proxy is up, but kubectl fails for all operations. The API server is unreachable.

### 11:57

A C ticket is created via the cloud provider's portal. There are no other reports on the cloud provider's status page. Infrastructure staff consider creating a new cluster and attaching storage to it.

### 12:28p

An email is sent to contacts with the cloud provider asking for the ability to escalate the issue. C tickets have 8 hour response times.

### 12:40

It is decided that rather than moving the nfs server from one cluster to another, the ZFS pool should be migrated to a new nfs server in the new cluster. The new cluster is requested.

### 12:43 - 12:49

Cloud provider responds and calls infrastructure staff.

### 13:00

The cluster is created and a new nfs server is requested in the cluster's resource group.

### 13:10

Data volumes are detached from the old server and moved from the old cluster's resource group to the new one.

## 13:20

The ZFS pool is imported into the new nfs server. helm is run to create the staging hub.

## 13:34

helm completes and the staging hub is up. DNS is updated. helm is run to create the prod hub.

## 13:41

prod hub is up and DNS is updated.

### 13:46

Cloud provider asks their upstream why the API server went down.

### 14:48

letsencrypt on prod can successfully retrieve an SSL certificate enabling students to connect.

## Conclusion

The managed kubernetes service went down for as yet unknown reasons. A new cluster was created and existing storage was attached to it.

## Action items

### Monitoring

1. Remotely monitor the API server endpoint and send an alert when it is down.

## Update

Cloud provider's response on 3/15/2019:

> After reviewing all the logs we have, our backend advised below.
>
> > We’ve identified that there were problems with the infrastructure hosting your cluster which caused the kubelet on the master stopped responding. There were alerts regarding this issue which were addressed by our teams. We’re working to reduce the impact of these events as much as possible.
>
> Please be advised this is not related with region stability
>
> Feel free to let me know if any further questions and thanks for your patience.

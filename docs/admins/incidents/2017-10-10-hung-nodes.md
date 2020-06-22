# 2017-10-10 - Docker dies on a few Azure nodes

## Summary

On Oct 10, 2017, some user pods were not starting or terminating correctly. After checking node status, it was found that all affected pods were running on two specific nodes. The docker daemon wasn't responsive on these nodes so they were cordoned off. User pods were then able to start correctly.

## Timeline

### 2017-05-09 10:45a

A report in the course Piazza said that two students couldn't start their servers. The /hub/admin interface was not able to start them either. It was reported that the students may have run out of memory.

### 12:29p

The user pods were stuck in Terminating state and would not respond to explicit delete. The pods were forcefully deleted with `kubectl --namespace=prod delete pod jupyter-<name> --grace-period=0 --force`. The user pods started correctly via /hub/admin.

### 13:27

It was reported in the course slack that another student's server wasn't starting correctly. After checking one of the pod logs, it was observed that the node hosting the pods, k8s-pool1-19522833-13, was also hosting many more pods stuck in a Terminating state. `docker ps` was hanging on that node. The node was cordoned.

### 13:42

It was reported in slack that the student's server was able to start.

By this time, the cluster was checked for all pods to see if any other nodes were hosting an unusual number of pods in Terminating. It was found that k8s-pool2-19522833-9 was in a similar state. All stuck pods on that node were forcefully deleted and the node was also cordoned. `docker ps` was hung on that node too. pool2-...-9 had a load of 530 while pool1-...-13 had a load of 476. On the latter, hypercube was at 766% cpu utilization while it was nominal on the former. Node pool1-...-13 was rebooted from the shell however it did not come back online. The node was manually restarted from the Azure portal but it still didn't come back.

A node previously cordoned on another day, pool1-...-14, was rebooted. It came back online and was uncordoned.

### 13:51

Some relevant `systemctl status docker` logs were captured from pool2-...-9:
```
Oct 10 20:55:30 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:30.790401257Z" level=error msg="containerd: start container" error="containerd: container did not start before the specified timeout" id=abd267ef08b4a4184e19307be784d62470f9a713b59e406249c6cdf0bb333260
Oct 10 20:55:30 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:30.790923460Z" level=error msg="Create container failed with error: containerd: container did not start before the specified timeout"
Oct 10 20:55:30 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:30.810309575Z" level=error msg="Handler for POST /v1.24/containers/abd267ef08b4a4184e19307be784d62470f9a713b59e406249c6cdf0bb333260/start returned error: containerd: container did not start before the specified timeout"
Oct 10 20:55:36 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:36.146453953Z" level=error msg="containerd: start container" error="containerd: container did not start before the specified timeout" id=2ba6787503ab6123b509811fa44c7e42986de0b800cc4226e2ab9484f54e8741
Oct 10 20:55:36 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:36.147565759Z" level=error msg="Create container failed with error: containerd: container did not start before the specified timeout"
Oct 10 20:55:36 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:36.166295370Z" level=error msg="Handler for POST /v1.24/containers/2ba6787503ab6123b509811fa44c7e42986de0b800cc4226e2ab9484f54e8741/start returned error: containerd: container did not start before the specified timeout"
Oct 10 20:55:36 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:36.169360588Z" level=error msg="Handler for GET /v1.24/containers/json returned error: write unix /var/run/docker.sock->@: write: broken pipe"
Oct 10 20:55:36 k8s-pool2-19522833-9 dockerd[1237]: http: multiple response.WriteHeader calls
Oct 10 20:55:36 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:36.280209444Z" level=error msg="Handler for GET /v1.24/containers/610451d9d86a58117830ea7c0189f6157ba9a9602739ee23723e923de8c7e23e/json returned error: No such container: 610451d9d86a58117830ea7c0189f6157ba9a9602739ee23723e923de8c7e23e"
Oct 10 20:55:39 k8s-pool2-19522833-9 docker[1237]: time="2017-10-10T20:55:39.095888009Z" level=error msg="Handler for GET /v1.24/containers/54b64ca3c1e7ef4a04192ccdaf1cb9309d73acebd7a08e13301f3263de3d376a/json returned error: No such container: 54b64ca3c1e7ef4a04192ccdaf1cb9309d73acebd7a08e13301f3263de3d376a"
```

### 14:00

```
datahub@k8s-pool2-19522833-9:~$ ps aux | grep exe | wc -l
520
datahub@k8s-pool2-19522833-9:~$ ps aux | grep exe | head -5
root        329  0.0  0.0 126772  9812 ?        Dsl  00:36   0:00 /proc/self/exe init
root        405  0.0  0.0  61492  8036 ?        Dsl  00:36   0:00 /proc/self/exe init
root        530  0.0  0.0 127028  8120 ?        Dsl  00:36   0:00 /proc/self/exe init
root        647  0.0  0.0 127028  8124 ?        Dsl  13:07   0:00 /proc/self/exe init
root        973  0.0  0.0  77884  8036 ?        Dsl  13:10   0:00 /proc/self/exe init
```

### 14:30

pool1-...-13 was manually stopped in the Azure portal, then manually started. It came back online afterwards and docker was responsive. It was uncordoned.

pool2-...-9 was manually stopped in the Azure portal.

### 14:45

pool2-...-9 completed stopping and was manually started in the Azure portal.

### 17:25

It was observed that /var/lib/docker on pool1-19522833-13/10.240.0.7 was on / (sda) and not on /mnt (sdb).

## Conclusion

Docker was hung on two nodes, preventing pods from starting or stopping correctly.

## Action items

### Process

1. When there are multiple reports of student servers not starting or stopping correctly, check to see if the user pods were run on the same node(s).
1. Determine how many nodes are not mounting /var/lib/docker on sdb1.

### Monitoring

1. Look for elevated counts of pods stuck in Terminating state. For example, `kubectl --namespace=prod get pod -o wide| grep Terminating`

# Summary

On January 26, 2018, a new version of the helm chart was being installed on the production hub. Though the pod prepuller worked fine on the staging cluster, the prepuller never successfully finished on prod. This caused the CI to error because helm ran for too long. Additionally, the hub was taking a very long time to check user routes. After users were deleted in the hub's orm and the hub was restarted, it came back up fairly quickly.

## Timeline

### 2018-01-26 15:00

The helm chart for datahub was upgraded to a beta of v0.6 to make use of a new image puller. This was merged into the staging branch, successfully tested on the staging, and passed CI checks on prod. It was then merged to prod.

### 15:15

helm times out because the prepuller never completes. It is determined that the master node on staging is cordoned while the master node on prod is not and has:

```
taints:
  - effect: NoSchedule
    key: node-role.kubernetes.io/master
    timeAdded: null
    value: "true"
``

The master is cordoned on prod and a new build is started in CI.

### 15:33

After CI times out again due to the prepuller, it is discovered that the master node has been uncordoned. Though the hub and proxy pods restart, the hub is taking a very long time to check user routes. It is slower than the most recent hub restart which was itself slow enough to warrant a new issue on jupyterhub, https://github.com/jupyterhub/jupyterhub/issues/1633.

### 13:40

It is decided that the most expedient way to get the hub up is to delete users from the orm.

### 13:50

The following command is run after the database is backed up:

`delete from users where users.id in (select users.id from users join spawners on spawners.user_id = users.id where server_id is null);`

deleting 4902 records. The hub pod is deleted and the hub comes up shortly after.

## Conclusion

At 5000, the hub takes long enough to restart to inconvenience the number of active users at any one time.

## Action items

### Process

1. The prepuller should be fixed so that helm does not time out.
1. The hub route checking should be parallelized so that startup is not slow.
1. The staging hub should be seeded with users so that scaling issues can be exposed prior to reaching production.

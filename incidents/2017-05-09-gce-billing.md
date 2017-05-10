# Summary

On May 9, 2017, the compute resources associated with the data-8 project at GCE were suspended. All hubs including datahub, stat28, and prob140 were not reachable. This happened because the grant that backed the project's billing account ran out of funds. The project was moved to a different funding source and the resources gradually came back online.

## Timeline

### 2017-05-09 16:51

A report in the Data 8 Spring 2017 Staff slack, #jupyter channel, says that datahub is down. This is confirmed. Attempting to access the provisioner via `gcloud compute ssh provisioner-01` fails with:

```ERROR: (gcloud.compute.ssh) Instance [provisioner-01] in zone [us-central1-a] has not been allocated an external IP address yet. Try rerunning this command later.```

### 17:01

The Google Cloud console shows that the billing account has run out of the grant that supported the data-8 project. The project account is moved to another billing account which has resources left.

The billing state is confirmed by `gcloud` messages:

```
Google Compute Engine: Project data-8 cannot accept requests to setMetadata while in an inactive billing state.  Billing state may take several minutes to update.
```

### 17:09

provisioner-01 is manually started. All pods in the datahub namespace are deleted.

### 17:15

datahub is back online. stat28 and prob140 hub pods are manually killed. After a few moments the hubs are back online. The autoscaler is started.

### 17:19

The slack duplicator is started.

### 2017-05-10 10:48

A report in uc-jupyter #jupyterhub says that try.datahub is down. This is confirmed and the hub in the tmp namespace is killed. The hub comes online a couple of minutes later.

## Conclusion

There was insufficient monitoring of the billing status.

## Action items

### Process

1. Identify channels for billing alerts.
1. Identify billing threshold functions that predict when funds will run out.
1. Establish off-cloud backups. The plan is to do this via nbgdrive.
1. Start autoscaler automatically. It is manually started at the moment.

### Monitoring

1. Setup scheduled billing reports and threshold alarms.
1. Setup hub monitoring!
1. The slack duplicator runs in one of the GCP clusters. When the clusters go down, slack messages aren't forwarded from the data8-sp17-staff slack to uc-jupyter.

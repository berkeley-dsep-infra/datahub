# How to deploy google filestore for this hub

1. create the filestore instance in the web UI
2. mount the filestore on nfsserver-01 (typically to the `/export/dlab-filestore` directory)
3. if necessary, create the `dlab-filestore/dlab` subdir in the root of that filestore share
4. chown -R 1000:1000 dlab-filestore
5. from this subdirectory, execute the following `gcloud` command to update the instance to ROOT_SQUASH:
```
gcloud filestore instances update <dlab filestore instance name> --zone=us-central1-b --flags-file=dlab-squash-flags.json

make sure that you are using the correct instance name for the update.

# when to update dlab-squash-flags.json

1. when creating a new filestore share to set ROOT_SQUASH
2. scaling up storage

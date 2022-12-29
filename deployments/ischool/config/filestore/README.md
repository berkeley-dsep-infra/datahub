# How to deploy google filestore for this hub

1. create the filestore instance in the web UI
2. mount the filestore on nfsserver-01 (typically to the `/export/ischool-filestore` directory)
3. if necessary, create the `ischool-filestore/ischool` subdir in the root of that filestore share
4. chown -R 1000:1000 ischool-filestore
5. from this subdirectory, execute the following `gcloud` command to update the instance to ROOT_SQUASH:
```
gcloud filestore instances update <ischool filestore instance name> --zone=us-central1-b --flags-file=ischool-squash-flags.json

make sure that you are using the correct instance name for the update.

# when to update ischool-squash-flags.json

1. when creating a new filestore share to set ROOT_SQUASH
2. scaling up storage

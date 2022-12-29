# How to deploy google filestore for this hub

1. create the filestore instance in the web UI
2. mount the filestore on nfsserver-01 (typically to the `/export/prob140-filestore` directory)
3. if necessary, create the `prob140-filestore/prob140` subdir in the root of that filestore share
4. chown -R 1000:1000 prob140-filestore
5. from this subdirectory, execute the following `gcloud` command to update the instance to ROOT_SQUASH:
```
gcloud filestore instances update <prob140 filestore instance name> --zone=us-central1-b --flags-file=prob140-squash-flags.json

make sure that you are using the correct instance name for the update.

# when to update prob140-squash-flags.json

1. when creating a new filestore share to set ROOT_SQUASH
2. scaling up storage

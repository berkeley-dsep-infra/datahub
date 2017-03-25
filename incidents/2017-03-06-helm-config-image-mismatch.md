## Summary ##

On the evening of Mar 6, the hub on prod would not come up after an upgrade. The upgrade was to accommodate a new disk for cogneuro that had been tested on dev. After some investigation it was determined that the helm's new config did not match the hub's image. After the hub image was rebuilt and pushed out, then tested on dev, it was pushed out to prod. The problem was fixed in about 40 minutes.

## Timeline ##

All times in PST

### 22:59 ###

dev changes are deployed but hub does not start correctly. The `describe` output for the hub shows repeated instances of:

Error syncing pod, skipping: failed to "StartContainer" for "hub-container" with CrashLoopBackOff: "Back-off 10s restarting failed container=hub-container pod=hub-deployment-3498421336-91gp3_datahub-dev(bfe7d8bd-0303-11e7-ade6-42010a80001a)

helm chart for -dev is deleted and reinstalled.

### 23:11 ###

dev changes are deployed successfully and tested. cogneuro's latest data is available.

### 23:21 ###

Changes are deployed to prod. The hub does not start properly. `get pod -o=yaml` on the hub pod shows that the hub container has terminated. The hub log shows that it failed due to a bad configuration parameter.

### 21:31 ###

While the helm chart had been updated from git recently, the latest tag for the hub did not correspond with the one in either prod.yaml or dev.yaml.

### 21:41 ###

The hub image is rebuilt and pushed out.

### 21:45 ###

The hub is deployed on -dev.

### 21:46 ###

The hub is tested on -dev then deployed on -prod.

### 21:50 ###

The hub is tested on -prod. Students are reporting that the hub had been down.

## Conclusion ##

When updates to the chart are pulled in that affect the run-time configuration of an image, we need to be referencing an image tag that know how to correctly process that new configuration.

## Action items ##

1. Determine why dev worked with outdated image but prod did not

2. Devise a way to ensure that helm configs coincide with image rebuilds and deploys. Can we assert mismatches during helm upgrade to abort early?

3. Get a deployment checklist in place to make sure we don’t accidentally miss any warning signs.

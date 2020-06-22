# 2017-03-06 - Non-matching hub image tags cause downtime

## Summary ##

On the evening of Mar 6, the hub on prod would not come up after an upgrade. The upgrade was to accommodate a new disk for cogneuro that had been tested on dev. After some investigation it was determined that the helm's config did not match the hub's image. After the hub image was rebuilt and pushed out, then tested on dev, it was pushed out to prod. The problem was fixed in about 40 minutes.

A few days later (March 12), similar almost outage is avoided when -dev breaks and deployment is put on hold. More debugging shows the underlying cause is that git submodules are hard to use. More documentation is provided, and downtime is averted!

## Timeline ##

All times in PST

### March 6 2017 22:59 ###

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

### March 12 19:57 ##

A new deploy is attempted on -dev, but runs into same error. Deployments are halted for more debugging this time, and more people are called on.

### 23:21 ##

More debugging reveals that the commit update looked like this:

```
diff --git a/chart b/chart
index e38aba2..c590340 160000
--- a/chart
+++ b/chart
@@ -1 +1 @@
-Subproject commit e38aba2c5601de30c01c6f3c5cad61a4bf0a1778
+Subproject commit c59034032f8870d16daba7599407db7e6eb53e04
diff --git a/data8/dev.yaml b/data8/dev.yaml
index 2bda156..ee5987b 100644
--- a/data8/dev.yaml
+++ b/data8/dev.yaml
@@ -13,7 +13,7 @@ publicIP: "104.197.166.226"

 singleuser:
   image:
-    tag: "e4af695"
+    tag: "1a6c6d8"
   mounts:
     shared:
       cogneuro88: "cogneuro88-20170307-063643"
```

Only the tag should've been the only thing updated. The chart submodule is updated to `c59034032f8870d16daba7599407db7e6eb53e04`, which is from February 25 (almost two weeks old). This is the cause of the hub failing, since it is using a really old chart commit with a new hub image.

## 23:27 ##

It is determined that incomplete documentation about deployment processes caused `git submodule update` to be not run after a `git pull`, and so the chart was being accidentally moved back to older commits. Looking at the commit that caused the outage on March 6 showed the exact same root cause.

## Conclusion ##

Git submodules are hard to use, and break most people's mental model of how git works. Since our deployment requires that the submodule by in sync with the images used, this caused an outage.

## Action items ##

### Process ###

1. Make sure we treat any errors in -dev exactly like we would in prod. Any deployment error in prod should immediately halt future deployments & require a rollback or resolution before proceeding.
2. Write down actual deployment documentation & a checklist.
3. Move away from git submodules to a separate versioned chart repository.

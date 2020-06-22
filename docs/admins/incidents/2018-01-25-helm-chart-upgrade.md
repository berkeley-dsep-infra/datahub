# 2018-01-25 - Accidental merge to prod brings things down

## Summary

On January 25, 2018, a new version of the helm chart was installed on the staging hub. It was not immediately merged to production because there were active labs throughout the day. While preparing another course's hub via Travis CI, the Data 8 change was accidentally merged from staging to production. This production hub went down because the new helm chart's jupyterhub image was broken.

## Timeline

### 2018-01-25 14:30

The helm chart for datahub was upgraded to a beta of v0.6 to make use of a new image puller. This was merged into the staging branch. After some initial debugging, the helm chart was installed successfully and the image puller worked correctly. However, the staging hub was not tested.

Since labs were scheduled throughout the day until 7p, it was decided to delay the upgrade of the production hub until after 7p.

### 15:30

While a different hub was being managed in Travis CI, the production hub for Data 8 was accidentally upgraded. This upgrade brought with it the faulty hub image from staging which wasn't working.

### 16:11

GSIs report in slack that the hub is down for lab users. It is confirmed that the hub process has crashed due to a shared C library included from a python library. It is decided that the quickest way to bring the hub back up is to downgrade the helm-chart back to v0.5.0.

### 16:35

The chart is installed into the staging repo, merged to staging, and checked on the staging hub. It is then merged into production and brought online there.

## Conclusion

A relatively large change was made to the hub configuration with insufficient testing on the staging server. This was compounded when the change was accidentally merged to production.

## Action items

### Process

1. Admins should refamiliarize themselves with the deployment policy to check the staging hub before changes are merged to production.
1. Determine if there is a way to block merges to production if the staging hub is not online.
1. Determine if there is a way to contextualize the Travis CI interface so that it is obvious which deployment is being managed.

---
title: Storage Retention Policy
---

## Policy

### Criteria

No non-hidden files in the user\'s home directory that have been
modified in the last 6 months.

### Archival

1.  Zip the whole home directory
2.  Upload it to Google drive of a
    [SPA](https://calnetweb.berkeley.edu/calnet-departments/special-purpose-accounts-spa)
    created for this purpose
3.  Share the ZIP file in the Google Drive with the user.

## Rationale

Today (6 Feb 2020), we have 18,623 home directories in datahub. Most of
these users used datahub in previous semesters, have not logged in for a
long time, and will probably never log in again. This costs us a lot of
money in disk space - we will have to forever expand disk space.

By cleaning it up after 6 months of non-usage, we will not affect any
current users - just folks who haven\'t logged in for a long time.
Archiving the contents would make sure people still have access to their
old work, without leaving the burden of maintaining it forever on us.

## Why Google Drive?

We can also perform access control easily with Google Drive.

## Alternatives

1.  Email it to our users. This will most likely be rejected by most
    mail servers as the home directory will be too big an attachment
2.  Put it in [Google Cloud Nearline
    storage](https://cloud.google.com/storage/archival/), build a token
    based access control mechanism on top, and email this link to the
    users. We will need to probably clean this up every 18 months or so
    for cost reasons. This is the viable alternative, if we decide to
    not use Google Drive

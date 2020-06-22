# JupyterHub db manual overwrite
## Summary ##
Datahub was reportedly down at 1am. Users attempting to log in to datahub were greeted with a proxy error. The hub pod was up but the log was full of sqlite errors. After the hub pod was deleted and a new one came up, students logging in to datahub found their notebooks were missing and their home directories were empty. Once this was fixed, some students still were being logged in as a different particular user. Finally, students with a '.' in their username were still having issues after everyone else was fine. This was all fixed and an all-clear signalled at about 2017-02-09 11:35 AM.


## Timeline ##
### 2017-02-09 00:25 - 00:29 AM ###

**Attempting to debug some earlier 400 errors, Trying to set base_url and ip to something incorrect to see if it will cause a problem.**

```bash
kubectl exec hub-deployment-something --namespace=datahub -it bash
apt-get install sqlite3
sqlite3
```
```sql
ATTACH 'jupyterhub.sqlite AS my_db;
SELECT name FROM my_db.sqlite_master WHERE type='table';
SELECT * FROM servers;
SELECT * FROM servers WHERE base_url LIKE '%<USER>%';
UPDATE servers SET ip='' WHERE base_url LIKE '%<USER>%';
UPDATE servers SET base_url='/<something-wrong> WHERE base_url LIKE '%<USER>%';
```
*Ctrl+D* (exit back into bash shell)

*checked datahub.berkeley.edu, and nothing happened to the account*
*saw that the sql db was not updated, attempt to run .save*
```
```bash
sqlite3
```
```sql
.save jupyterhub.sqlite
```

**This replaced the db with an empty one, since ATTACH was not run beforehand.**


### 0:25:59 AM ###


Following exception shows up in hub logs:

```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: proxies [SQL: 'SELECT proxies.id AS proxies_id, proxies._public_server_id AS proxies__public_server_id, proxies._api_server_id AS proxies__api_server_id \nFROM proxies \nWHERE proxies.id = ?'] [parameters: (1,)]
```

This continues for hub table as well, since those two seem to be most frequently used.

### 1:12 AM ###

Sam's roommate notices that he can log in to datahub but all his notebooks are gone. We notice that there are only ~50 users on the JHub admin panel when there used to be ~1000, so we believe that this is because the JHub sqlite user database got wiped/corrupted, then created an account for his roommate when he logged in, then created a new persistent disk since it lost track of his old one.

This is confirmed soon after:


```bash
$ kubectl --namespace=datahub get pvc | grep  <username>
claim-<username>-257     Bound     pvc-3b405e13-ddb4-11e6-98ef-42010af000c3   10Gi       RWO           21d
claim-<username>-51      Bound     pvc-643dd900-eea7-11e6-a291-42010af000c3   10Gi       RWO           5m
```

### 1:28 AM  ###


We shut down the hub pod by scaling the replicas to 0.

We then begin recreating the JHub sqlite database by taking the Kubernetes PVCs and matching them back with the user ids. We could do this because the name of the PVC contains a sanitized form of the username and the userid.

Here's the notebook that was used to recreate the db from PVCs: [pvc-sqlite.ipynb 2017-02-09-datahub-db-outage-pvc-recreate-script.ipynb](pvc-sqlite.ipynb 2017-02-09-datahub-db-outage-pvc-recreate-script.ipynb)


### 2:34 AM  ###

We recreate the sqlite3 database. Initially each user's cookie_id was set to a dummy cookie value.


### 2:42 AM ###


User cookie_id values are changed to null rather than dummy value. The sqlite file is then attached back to datahub. The number of users shown on admin page is back to ~1000. The hub was up, and a spot check of starting other user’s servers seem to work. Some users get redirected to one particular user, but deleting and recreating the affected user seems to fix this.


### 10:11 AM ###


Attempt to log everyone out by changing cookie secret in hub pod at /srv/jupyterhub/jupyterhub_cookie_secret. Just one character near the end was changed, and pod restarted. No effect. One character at the beginning of secret was changed next, and restarted - this caused actual change, and logged all users out.

People are still being redirected to one particular user's account when they log in. More looking around required.

### 10:17 AM ###


John Denero advises students to use ds8.berkeley.edu right now. ds8.berkeley.edu promptly starts crashing because it does not have resources for a data8 level class.


### 10:29 AM ###


All user pods are deleted, which finally properly logs everyone out. However, people logging in are still all getting the same user's pods.


### 10:36 AM ###


Notice that `cookie_id` column in the user database table is empty for many users, and the user that everyone is being logged in as has an empty `cookie_id` too and is the 'first' on the table when sorted in ascending by id. Looking at the JupyterHub code, `cookie_id` is always supposed to be set to a uuid, and never supposed to be empty. Setting `cookie_id` for users fixes their issues, and seems to spawn them into their own notebook.


### 10:45 AM ###


A script is run that populates `cookie_id` for all users, and restarts the hub to make sure there's no stale cache in RAM. All user pods are deleted again. Most users are back online now! More users start testing and confirming things are working for them.


### 10:53 AM ###


User with a '.' in their name reports that they're getting an empty home directory. More investigation shows two users - one with a '.' in their name that is newer, and one with a '-' in their name instead of '.' that is older. Hypothesis is that one of them is the 'original', but they're all attaching to a new one that is empty. Looking at pvcs confirms this - there are two PVCs for users with a . in their name who have tried to log in, and they differ only by ids.


There is some confusion about users ending up on prob140, because the data8.org homework link is changed to use that temporarily.


### 11:05 AM ###


Directly modifying the user table to rename the user with the '-' in the name to have a '.' seems to work for people.


### 11:15 AM ###


A script is run that modifies the database user table for all users with a '-' in their name, and the '-' is replaced with a '.'. The new users created with the '.' in their name are dropped before this.


### 11:17 AM ###


All clear given for datahub.berkeley.edu


### 11:19 AM ###


Locally verified that running .save <filename> on sqlite3 will overwrite the db file without any confirmation, and is most likely cause of the issue.
Conclusion
Accidental overwriting of the sqlite file during routine debugging operation led all tables being deleted. Users were getting new user ids when they were logging in now, causing them to get new disks provisioned - and these disks were empty. During reconstruction of the db, cookie_id was missing for several users, causing them all to log in to one particular user's notebook. Users with '.' in their name were also set up slightly incorrectly - their pods have '-' in them but the user name should have a '.'.


## Action items ##

### Upstream bug reports for JupyterHub ###

1. JupyterHub only uses a certain length of the cookie secret, and discards the rest. This causes confusion when trying to change it to log people out. [Issue](https://github.com/jupyterhub/jupyterhub/issues/986)
2. The cookie_id column in the users table should have UNIQUE and NOT NULL constraints. [Issue](https://github.com/jupyterhub/jupyterhub/issues/985)


### Upstream bug reports for KubeSpawner ###

1. Support using username hashes in PVC and Pod Names rather than user ids, so that pod and PVC names remain constant even when DB is deleted. [Issue](https://github.com/jupyterhub/kubespawner/issues/21)


### Upstream bug reports for OAuthenticator ###
1. Support setting id of user in user table to be same as ‘id’ provided by Google authenticator, thus providing a stable userid regardless of when the user first logged in. [Issue](https://github.com/jupyterhub/oauthenticator/issues/65)


### DataHub deployment changes ###
1. Switch to using Google Cloud SQL, which provides hosted and managed MySQL database
2. Perform regular and tested backups of the database
3. Start writing an operational FAQ for things to do and not do
4. Setup better monitoring and paging systems
5. Document escalation procedures explicitly

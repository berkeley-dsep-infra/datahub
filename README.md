testing

# Berkeley JupyterHubs 

Contains a fully reproducible configuration for JupyterHub on datahub.berkeley.edu,
as well as its single user image.

## Branches

The `staging` branch always reflects the state of the [staging JupyterHub](http://staging.datahub.berkeley.edu),
and the `prod` branch reflects the state of the [production JupyterHub](http://datahub.berkeley.edu).

## Setting up your fork and clones
First, go to your [github profile settings](https://github.com/settings/keys)
and make sure you have an SSH key uploaded.

Next, go to the [Datahub github repo](https://github.com/berkeley-dsep-infra/datahub/)
and create a fork.  To do this, click on the `fork` button and then `Create fork`.

Now clone the primary Datahub repo on your local device.  You can get the URL to do
this by clicking on the green `Code` button in the primary Datahub repo (*not* your fork)
and clicking on `ssh`:
```
git clone git@github.com:berkeley-dsep-infra/datahub.git
```

Now `cd` in to `datahub` and set up your local repo to point both at the primary
Datahub repo (`upstream`) and your fork (`origin`).  After the initial clone,
`origin` will be pointing to the main repo and we'll need to change that.
```
$ cd datahub
$ git remote -v
origin	git@github.com:berkeley-dsep-infra/datahub.git (fetch)
origin	git@github.com:berkeley-dsep-infra/datahub.git (push)
$ git remote rename origin upstream
$ git remote add origin git@github.com:<your github username>/datahub.git
$ git remote -v
origin	git@github.com:<your github username>/datahub.git (fetch)
origin	git@github.com:<your github username>/datahub.git (push)
upstream	git@github.com:berkeley-dsep-infra/datahub.git (fetch)
upstream	git@github.com:berkeley-dsep-infra/datahub.git (push)
```

Now you can sync your local repo from `upstream`, and push those changes to your
fork (`origin`):
```
git checkout staging && \
git fetch --prune --all && \
git rebase upstream/staging && \
git push origin staging
```


## Procedure

When developing for this deployment, always work in a fork of this repo.
You should also make sure that your repo is up-to-date with this one prior
to making changes. This is because other contributors may have pushed changes
after you last synced with this repo but before you upstreamed your changes.

```
git checkout staging && \
git fetch --prune --all && \
git rebase upstream/staging && \
git push origin staging
```

To create a new branch and switch to it, run the following command:
```
git checkout -b <branch name>
```

After you make your changes, you can use the following commands to see
what's been modified and check out the diffs:  `git status` and `git diff`.


When you're ready to push these changes, first you'll need to stage them for a
commit:
```
git add <file1> <file2> <etc>
```

Commit these changes locally:
```
git commit -m "some pithy commit description"
```

Now push to your fork:
```
git push origin <branch name>
```

Once you've pushed to your fork, you can go to the
[Datahub repo](https://github.com/berkeley-dsep-infra/datahub) and there
should be a big green button on the top that says `Compare and pull request`.
Click on that, check out the commits and file diffs, edit the title and
description if needed and then click `Create pull request`.

If you're having issues, you can refer to the [github documentation for pull
requests](https://help.github.com/articles/about-pull-requests/).
The choice for `base` in the GitHub PR user interface should be the staging
branch of this repo while the choice for `head` is your fork.

Once this is complete and if there are no problems, you can request that
someone review the PR before merging, or you can merge yourself if you are
confident. This merge will trigger a CircleCI process which upgrades the
helm deployment on the staging site. When this is complete, test your
changes there. For example if you updated a library, make sure that a new
user server instance has the new version. If you spot any problems you can
revert your change. You should test the changes soon after the merge since
we do not want unverified changes to linger in staging.

If staging fails, *never* update production. Revert your change or
call in help if necessary. If your change is successful, you will need
to merge the change from staging branch to production. Create another PR,
this time with the `base` set to prod and the `head` set to staging. This
PR will trigger a similar Travis process. Test your change on production
for good measure.

## SSL: LetsEncrypt Strategy
The Berkeley-based SPA email address, datahub-support@berkeley.edu, is the
contact email used to create the SSL certificate for the datahub at
[LetsEncrypt](https://letsencrypt.org/). The address is only used by LetsEncrypt
when there is a problem renewing the certificate.

The SPA email address is connected to anyone in ds-infrastructure@lists.berkeley.edu.

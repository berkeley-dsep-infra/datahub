# Berkeley JupyterHubs 

Contains a fully reproducible configuration for JupyterHub on datahub.berkeley.edu,
as well as its single user image.

## Branches

The `staging` branch always reflects the state of the [staging JupyterHub](http://staging.datahub.berkeley.edu),
and the `prod` branch reflects the state of the [production JupyterHub](http://datahub.berkeley.edu).

## Procedure

When developing for this deployment, always work in a fork of this repo.
You should also make sure that your repo is up-to-date with this one prior
to making changes. This is because other contributors may have pushed changes
after you last synced with this repo but before you upstreamed your changes.
When you are ready, [create a pull request](https://help.github.com/articles/about-pull-requests/).
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

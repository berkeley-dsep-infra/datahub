# Berkeley JupyterHubs

Contains fully reproducible configurations for local JupterHubs for use with 
students.

## Charts

We'll have a chart per hub we manage. This is to make it easy for us to
pin versions of upstream Charts we might be using - using `requirements.yaml`.

It also makes autodeployment easy!

## Branches

We'll have a `staging` branch that will always reflect the state of the
staging JupyterHubs. Same with a `prod` branch that will reflect the state
of the production JupyterHubs.

## Images

User images for each of the hubs are also managed in this repository.

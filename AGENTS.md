# Agent Instructions for UC Berkeley DataHub

This repository manages the configuration and deployment of multiple JupyterHubs for UC Berkeley using [Zero to JupyterHub (z2jh)](https://z2jh.jupyter.org/) and [`hubploy`](https://github.com/berkeley-dsep-infra/hubploy).

## Primary Roles & Tasks

### 1. Hub Administrator / DevOps
*   **Creating Hubs**: Follow [docs/tasks/new-hub.qmd](docs/tasks/new-hub.qmd). Use `cookiecutter template/` in the `deployments/` directory.
*   **Infrastructure**: Managed on Google Cloud Platform (GKE and Filestore).
*   **Secrets**: Files in `secrets/` folders are encrypted with `sops`. Use `sops` for editing.
*   **Deployment**: Triggered via GitHub PR labels (e.g., `hub: <hubname>`). Labels are defined in [.github/labeler.yml](.github/labeler.yml).
*   **Workflow**: Always deploy to the `staging` branch first, then merge `staging` to `prod`.

### 2. Course Staff / Instructor
*   **Configurations**: Hub-specific settings (RAM limits, admin lists, storage) are in `deployments/<hubname>/config/common.yaml`.
*   **User Images**: User environments are defined in *separate* image repositories. This repo's `hubploy.yaml` tracks image tags. 
*   **Testing**: Advise instructors to test packages via `!pip install --upgrade` in a notebook before requesting permanent image updates.

### 3. Documentation Contributor
*   **Tech Stack**: [Quarto](https://quarto.org/) for rendering `.qmd` and `.md` files in [docs/](docs/).
*   **Style Guide**:
    *   Use **backticks** (`path/`) for filesystem paths, program names, and commands.
    *   Use *asterisks* (*term*) for emphasis.
    *   Avoid colons `:` in headings.
    *   Use descriptive link text (avoid "click here").
    *   Always provide `alt text` for figures.

## Project Structure
*   [/deployments/](deployments/): Subdirectories for each hub (e.g., `data8`, `biology`).
    *   `config/`: YAML files for z2jh configuration (`common.yaml`, `staging.yaml`, `prod.yaml`).
    *   `secrets/`: SOPS-encrypted secrets.
    *   `hubploy.yaml`: Deployment metadata and image tags.
*   [/hub/](hub/): Helm chart for the JupyterHub.
*   [/support/](support/): Helm chart for support services (Prometheus, Grafana).
*   [/node-placeholder/](node-placeholder/): Helm chart for pre-warming GKE nodes.
*   [/docs/](docs/): Source for [docs.datahub.berkeley.edu](https://docs.datahub.berkeley.edu).

## Coding Standards & Environment
*   **Python**: Version 3.11+ (see [docs/.readthedocs.yaml](docs/.readthedocs.yaml)).
*   **Dependencies**: Install via `pip install -r dev-requirements.txt`.
*   **Tools**: `hubploy`, `chartpress`, `sops`, `kubectl`, `gcloud`, `quarto`, `cookiecutter`.

## Contribution Workflow

*   **Remotes**: 
    *   `upstream`: [berkeley-dsep-infra/datahub](https://github.com/berkeley-dsep-infra/datahub)
    *   `origin`: The developer's personal fork.
*   **Branching**:
    *   `main`: Often unused for direct deployment; check `staging`.
    *   `staging`: The primary development branch. PRs from forks should target `staging`.
    *   `prod`: Deployment to production. Merges should go `staging` -> `prod`.
*   **Pre-commit**: Always run `pre-commit install` after installing dependencies to ensure linting and formatting match project standards.

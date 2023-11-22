# Guide to Setting up JupyterHub Infrastructure

JupyterHub is a powerful multi-user platform that allows you to provide a collaborative environment for data science and code execution. In your school's JupyterHub deployment, you can accommodate a large number of active users while ensuring each user gets their personal space. This guide will walk you through the key components and configurations of your JupyterHub infrastructure.

## Overview

### User Base

- Your JupyterHub serves **10,000 to 11,000 active users**, making it a high-capacity platform for data science and coding.

### Personal Spaces

- JupyterHub ensures that **each user gets their personal space** where they can work independently.

### Code Execution

- JupyterHub provides an **authenticated way to perform multi-user arbitrary code execution**. You may currently use bcourses for this purpose.

### Web-Based Code Execution

- Users can execute code via web interfaces, which means **code execution doesn't rely on local memory**.

## Infrastructure

### Kubernetes Cluster

- JupyterHub runs on a **Kubernetes (K8) cluster**, ensuring scalability and resource management.

### Resource Allocation

- The Kubernetes cluster manages CPU and memory allocation, allowing for efficient resource usage.

### Autoscaling

- Utilize **Calendar Autoscale** to automatically adjust resources based on demand.

### Docker Images

- Docker images are used to package software and its dependencies. In your setup, **Docker images capture the environment** for JupyterHub.

### Supported Languages

- JupyterHub supports a variety of programming languages, including:
  - **Python**: Runs on Conda with the Conda ecosystem and Mamba package manager. It also supports PyPI packages.
  - **R**: Supports RStudio and RSPM for package management.
  - **Julia**: Provides support for Julia programming.

### NbGitPuller

- **NbGitPuller** is integrated, which allows users to easily access JupyterHub and pull repositories from GitHub, even if they are not familiar with Git.

## Administration

### API and Access Control

- JupyterHub offers an **API** for administrative tasks and **private access control** to manage user permissions.

## Network Layout

Your JupyterHub infrastructure is organized as follows:

1. **User** - Individual users who access JupyterHub.
2. **CHP (Configurable HTTP Proxy)** - The CHP directs individual users to their respective personal spaces.
3. **Hub** - Inside the hub, key components include:
   - **Authenticator**: Verifies user credentials and authentication.
   - **Spawner** - Manages user sessions, including the use of **KubeSpawner** for user environments.
   - **Proxy** - Handles routing and load balancing of user requests.
   - **SQLite Database** - Stores necessary information for user sessions.

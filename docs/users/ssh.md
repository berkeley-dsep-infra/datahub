# SSH & SFTP service

All the hubs offer experimental [SSH service](https://www.ssh.com/ssh/) for interactive use, and [SFTP](https://www.ssh.com/ssh/sftp/) for file transfer, via a deployment of the [jupyterhub-ssh](https://github.com/yuvipanda/jupyterhub-ssh).

SSH access provides the exact same environment - packages, home directory, etc - as web based access to JupyterHub. This allows for pedagogical uses where web based access & terminal based access are both used, and the same infrastructure (authentication, clusters, cloud resources, etc) used for both. SFTP also lets you copy files in / out of the same home directories, allowing for fast large amounts of file transfer for use in web based or ssh based uses.

## Accessing SSH

1. Create a **JupyterHub authentication token**, which you can use as the password. The URL to go to this depends on the hub you are trying to access, and is `https://<hub-url>/hub/token`. URLs for common hubs are provided here:

   - [datahub.berkeley.edu](https://datahub.berkeley.edu/hub/token)
   - [r.datahub.berkeley.edu](https://r.datahub.berkeley.edu/hub/token)
   - [eecs.datahub.berkeley.edu](https://eecs.datahub.berkeley.edu/hub/token)
   - [biology.datahub.berkeley.edu](https://biology.datahub.berkeley.edu/hub/token)
   - [prob140.datahub.berkeley.edu](https://prob140.datahub.berkeley.edu/hub/token)
   - [workshop.datahub.berkeley.edu](https://workshop.datahub.berkeley.edu/hub/token)
   - [julia.datahub.berkeley.edu](https://julia.datahub.berkeley.edu/hub/token
   - [highschool.datahub.berkeley.edu](https://highschool.datahub.berkeley.edu/hub/token
  
   **NOTE**: This token is **your password**, and everyone with it can access **all your files**, including any assignments you might have. If you are an **admin** on any of these hubs, then they can use it to access the space of **anyone else** on that hub, so please treat these with extreme care.
   
2. Open your terminal, and run the following:

   ```bash
   ssh <hub-username>@<hub-location>
   ```
   
   The `<hub-username>` is the same as your Calnet username in most places - the part before the `@` in your `berkeley.edu` email. For a small minority of users, this is different - you can confirm this in the JupyterHub control panel, on the top right.
   
   `<hub-location>` refers to the hub you are trying to log on to - so `datahub.berkeley.edu` or `r.datahub.berkeley.edu`, etc.
   
3. When asked for the password, provide the token generated in step 1.

4. This should give you an interactive terminal! You can do anything you would generally interactively do via ssh - run editors, fully interactive programs, use the commandline, etc. Some features - non-interactive command running, tunneling, etc are currently unavailable.

## Accessing SFTP

SFTP lets you transfer files to and from your home directory on the hubs. The steps are almost exactly the same as accessing SSH. The one difference is that the `port` used is `2222`, rather than the default port of `22`. If you are using a GUI program for SFTP, you will need to specify the port explicitly there. If you are using the commandline `sftp` program, the invocation is something like `sftp -oPort=2222 <hub-username>@<hub-location>`

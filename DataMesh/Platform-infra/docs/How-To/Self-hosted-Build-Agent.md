
# Self-hosted DevOps Build Agent

## Requirements

### Firewall

In order to install the self-hosted DevOps agent on a Linux VM within the VF network, you have to request a number of firewall changes.

- `dev.azure.com`
- `*.dev.azure.com`
- `login.microsoftonline.com`
- `management.core.windows.net`
- `vstsagentpackage.azureedge.net`

*If you require additional access, e.g. Databricks API, you should also request them now.*

### Agent Pool (optional)

On DevOps go to" Project Settings" &rarr; "Agent pools" and click on "Add pool". Choose "self-hosted" as pool type, enter a name and click "create".

On your new agent pool go to the "Agents" tab and click "New agent". Choose "Linux" and the matching architecture for your VM (usually `x64`), and download the build agent software.

### On the machine

While waiting for the firewall change request, create a system user that will run the self-hosted agent and move the agent files to the VM.

To create a system user called `build_agent`, run the following:

```sh
sudo -s useradd -r build_agent
```

Then become the `build_agent` user:

```sh
sudo -s su build_agent
```

This will create the home directory for the `build_agent` system user at `/home/build_agent`.

Go to the home directory (`cd ~`) and create a new folder for the agent files (`mkdir agent`).
From your local machine (VF laptop), copy the DevOps agent files to the build VM:

```bash
scp vsts-agent-linux-<version>.tar.gz <a2user>@<build-VM>:
```

*Mind the `:` at the end.*

Once the file is copied, move them from your home directory to the agent folder and unpack them:

```sh
cd /home/build_agent/agent
cp /home/<a2user>/vsts-agent-linux-<version>.tar.gz .
tar -xzvf vsts-agent-linux-<version>.tar.gz
```

### PAT

In DevOps create a PAT with "Agent Pools (read & manage)" and "Deployment Groups
(read & manage)" permissions.

The token is only used to establish the initial connection of the agent and must
not be managed afterwards.

---

## Setup

### VSTS Agent config

Become the `build_agent` user:

```sh
sudo -s su build_agent
```

As `build_agent` user, go to the agent directory and run the config script (`./config.sh`).

In the config dialog, enter the following information:

- Enter the DevOps server URL: `https://dev.azure.com/<organization>`
- Authentication type: press enter (defaults to PAT)
- Enter your PAT
- Enter the name of Agent Pool
- Enter a name for your Agent (this will be displayed in the Agent Pool)
- Use the default working directory

Confirm that the agent is registered to DevOps. You should see it under Agents in your Agent pool.

Become your a2 user again (type `exit` in the console) and go to the agent directory.
Install the agent as `systemd` service for the `build_agent` user by running

```sh
sudo -s ./svc.sh install build_agent
```

Then start the service:

```sh
sudo -s ./svc.sh start
```

The agent should be shown as "online" in your DevOps agent pool.

### Additional software

If you need to install additional software, make sure to do that as `build_agent` user, or that the software is available for that user.

You also might need to update the `.path` file in the agent folder. Check the current content of the `.path` file (`cat .path`). It should include:

- `/home/build_agent/bin` (for local binaries)
- `/home/build_agent/.local/bin` (for python packages)

If you need additinal locations in your `PATH`, make sure they are also included.

To update the `.path` file, you can do so manually or safe the current `PATH` using the `env.sh` script. For the new path to be imported to the Agent, you need to restart the service:

```sh
sudo -s ./svc.sh stop
sudo -s ./svc.sh start
```

## TL;DR

- Make Firewall change request for your build machine to:
  - `dev.azure.com`
  - `*.dev.azure.com`
  - `login.microsoftonline.com`
  - `management.core.windows.net`
  - `vstsagentpackage.azureedge.net`
- create `build_agent` system user
  - `sudo -s useradd -r build_agent`
- configure DevOps agent as `build_agent` user
  - `./config.sh`
  - you need: devops server URL, valid PAT, Agent pool name, Agent name
- (optinal) install additional software and update PATH
- install and start agent as `systemd` service with your a2 account
  - `sudo -s ./svc.sh install build_agent`
  - `sudo -s ./svc.sh start`

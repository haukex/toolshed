Hauke's Development Environment
===============================

These are my notes on how I like to set up my development environment.

## Rationale

- I try to make sure that all of my projects work purely from the command line.
  I currently like VSCode because it is a responsive editor that matches my personal preferences
  fairly well and simply leverages all of those command-line tools.
  - (Just to name a counterexample: PyCharm is a nice IDE, but at the time I was using it, its
    Python linter appeared to only be available built in to the IDE, not from the command line,
    which I felt locked me in to that IDE too much.)
- At the time of writing, I am beginning to enjoy [Development Containers](https://containers.dev/)
  and am currently planning to transition most of my development into them, so more and more of
  my projects should eventually be getting `.devcontainer/devcontainer.json` files.
  As far as I can tell at the moment, they are primarily used on GitHub Codespaces. However:
  - Container definitions (`Dockerfile`s and `devcontainer` definitions) are mostly shell scripts
    that install stuff in a VM/container. If one doesn't want to be dependent on those tools, one
    can always just read the files and install the requirements oneself.
  - DevPod is a nice open-source alternative for running the same Development Containers,
    including on a *local* Docker.
    - At the time of writing, I haven't been using DevPod very long, but it seems good so far.
      Notes:
      - Container initialization seems to be a bit slow sometimes?
      - [`/workspaces` permissions](https://github.com/loft-sh/devpod/issues/1107) - Workaround
        is to run ``sudo chown -R `id -u` /workspaces/*`` after building the container.
      - [Rebuild does not run dotfiles](https://github.com/loft-sh/devpod/issues/1279) - Workaround
        is that after a Rebuild, close VSCode, then use DevPod's "Open" to re-open it.
      - [Where are the build logs?](https://github.com/loft-sh/devpod/issues/1278) - Not super
        important, but could help with debugging.

## Windows

Focus: **Limited Administrator rights**, i.e. a few installations may require Administrator rights,
but otherwise, everything should work without them.

### Putty

- Install <https://www.chiark.greenend.org.uk/~sgtatham/putty/> with Pagent and plink
  - As per [the documentation](https://the.earth.li/~sgtatham/putty/0.81/htmldoc/Chapter9.html#pageant-cmdline-openssh),
    the OpenSSH installation that is integrated with Windows (`C:\Windows\System32\OpenSSH`), which
    you may need to install as a Windows "feature", can be configured to use Pagent as follows:
    - Set up a shortcut for autostart as appropriate in
      `C:\Users\USERNAME\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`, e.g.:
      `"C:\Program Files (x86)\putty\pageant.exe" --openssh-config "C:\Users\USERNAME\.ssh\pageant.conf" --encrypted "C:\Users\USERNAME\.ssh\KEYFILE1.ppk" ...`
    - In `C:\Users\USERNAME\.ssh\config`, add a line `Include pageant.conf`
  - Note: In an older version of my development environment, I tried to set up everything to use
    the `ssh.exe` from Git Bash, but note that its `ssh-agent` is *not* compatible with the Windows
    native version or with Pagent, plus using it was a bit of a pain (unlocking the key required me
    to start up Git Bash once after every boot, and DevPod didn't work with it either).
    - To delete the `SSH_AUTH_SOCK` variable set up in those old instructions,
      Windows+R and `rundll32.exe sysdm.cpl,EditEnvironmentVariables`
  - Note the permissions of `~/.ssh/` should be restricted to just the users'.
- From here on out, every program should use only `C:\Windows\System32\OpenSSH\ssh.exe` or Putty.

### Git Bash

- <https://git-scm.com/downloads> installs well without Admin rights
- Use recommended/default settings **except as noted below**: Vim editor, default branch name
  `main`, "Git from the command line and also from 3rd-party software", "Use the native Windows
  Secure Channel library", "Checkout as-is, commit Unix-style line endings" (`autocrlf=input`),
  "Use Windows' default console", use "Git Credential Manager"
  - **Use (Tortise)Plink**, point to your `plink.exe`
- After installation, make sure that `which ssh` returns the Windows native `ssh.exe`,
  *not* `/usr/bin/ssh` or anything else. You may need to add that to `PATH`:
  `export PATH="/c/Windows/System32/OpenSSH${PATH:+:${PATH}}"`

### WSL2

- Unless you already have WSL2 set up, in a PowerShell Console with Admin rights, follow the
  ["Manual installation steps for older versions of WSL"](https://learn.microsoft.com/en-us/windows/wsl/install-manual)
  - Including the download and installation of the "WSL2 Linux kernel update package"
    (may need Admin rights)
  - *But don't* install the Linux distro from the Microsoft Store, instead use e.g.
    `wsl --install -d Ubuntu-24.04`
  - If `wsl --update` and/or `wsl --install -d ...` give an unexplained error message,
    try adding the option `--web-download`.
- The `wsl --install -d ...` command must (also) be run by the non-admin user.
- Reboots may be required.

### Docker Desktop

- <https://www.docker.com/>
- Requires Admin rights to install/update.
  - Configure Docker to use WSL2.
- All users who want to use Docker must be a member of the local `docker-users` group.
  - Opening the Computer Management to edit groups requires Admin rights.
- In case of problems, uninstall (requires Admin), reboot, and reinstall.
  - There is also a tool `C:\Program Files\Docker\Docker\resources\com.docker.diagnose.exe`
    that can be run from the command line (with the `check` argument)
- Turn off "Send usage statistics".

### DevPod

- <https://devpod.sh/>
- Requires Admin rights to install.
- Don't forget to configure your dotfiles repo if you have one
  ([GitHub docs](https://dotfiles.github.io/),
  [DevPod docs](https://devpod.sh/docs/developing-in-workspaces/dotfiles-in-a-workspace)).
- Docker must be running for DevPod to work.

### VSCode

- Install from Microsoft Store or <https://code.visualstudio.com/>
- Change the setting `telemetry.telemetryLevel` to `off`.
- My personal user settings are in this repository in `vscode-user-settings-win.bak.jsonc`
  (backup script is `bak-vscode-user-sett-win.py` also in this repo).
- It's also possible to run VSCode on a server entirely and access it via a browser.
  e.g. `code serve-web --host 127.0.0.1 --port 8000`
  (may need to open port 8000 in the firewall, and/or if using port forwarding, bind to `0.0.0.0`)


Author, Copyright, and License
------------------------------

Copyright (c) 2024 Hauke Daempfling <haukex@zero-g.net>
at the Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB),
Berlin, Germany, <https://www.igb-berlin.de/>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.

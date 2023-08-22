My Notes on JavaScript Development
==================================

Node.js and TypeScript
----------------------

### Linux

- Follow the instructions at <https://github.com/nvm-sh/nvm>, *for example*
  `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash`
  - As per the instructions, re-start the shell session for the new env vars
- `nvm install --lts`
  - On Ubuntu 18.04, `nvm install --lts v16` (because newer node versions need `GLIBC_2.28`)
- `nvm install-latest-npm`
- `nvm alias default node`

### Windows

- Download the Node.js binary release (64-bit .zip) from <https://nodejs.org/en/download>
  and unpack, e.g. to `~/code/node-v...-win-x64`
- Add the directory with the `npm` and `node` binaries to `PATH` via e.g. putting
  this in your `~/.profile`: `export PATH="$HOME/node-path${PATH:+:${PATH}}"`

### Common

- `npm install -g typescript`

#### TypeScript Project

<https://www.typescriptlang.org/docs/>

- To initialize a `tsconfig.json` in the current directory:
  `tsc --init`
 (see also <https://github.com/tsconfig/bases/blob/main/bases/recommended.json>)

Visual Studio Code
------------------

<https://code.visualstudio.com/> or via Microsoft Store

To connect to a VS Code Server (such as an Ubuntu VM):
- In VSCode, in the Remote-SSH settings,
  - The *absolute* path to the `~/.ssh/config` must be set
  - And the permissions of `~/.ssh/` must be restricted to just the users'
  - In order to re-use a `ssh-agent` that was started in Git Bash as per
    <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/working-with-ssh-key-passphrases#auto-launching-ssh-agent-on-git-for-windows>,
    the "Remote.SSH" Path setting must be set to the `ssh.exe` from
    Git, e.g. `C:\Users\USER\AppData\Local\Programs\Git\usr\bin\ssh.exe`
    (the `ssh.exe` in `C:\Windows\System32\OpenSSH` is not compatible and
    running it breaks a running `ssh-agent`'s socket)
    - Alternatively (untested by me), it should be possible to configure the Windows OpenSSH version to
      access Pageant: <https://the.earth.li/~sgtatham/putty/0.78/htmldoc/Chapter9.html#pageant-cmdline-openssh>
      (and for Git for Windows to use that OpenSSH or even Plink instead of its own too)


Author, Copyright, and License
------------------------------

Copyright (c) 2022-2023 Hauke Daempfling <haukex@zero-g.net>
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

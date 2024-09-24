My Notes on JavaScript/TypeScript Development
=============================================

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
  (though most of my projects now include `typescript` as a project requirement,
  so `npm ci` will install it locally there)

#### TypeScript Project

<https://www.typescriptlang.org/docs/>

- To initialize a `tsconfig.json` in the current directory: `tsc --init`
  (see also <https://github.com/tsconfig/bases/blob/main/bases/recommended.json>)


Author, Copyright, and License
------------------------------

Copyright (c) 2022-2024 Hauke Daempfling <haukex@zero-g.net>
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

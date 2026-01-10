Hauke's Notes on Git
====================

Attributes
----------

- GitHub language stats: <https://github.com/github/linguist/blob/master/docs/overrides.md>,
  in particular `linguist-detectable`, `linguist-generated`, and `linguist-vendored`.
  - For example, in this repo I have `*.md linguist-detectable`, or if I have "archived"
    code files that I haven't deleted yet, `-linguist-detectable`.
- Mark a file as binary (e.g. to prevent EOL warnings): `-text`
- Mark a file so it isn't diffed: `-diff`
- Enable `$Id$` to be replaced by the object blob: `ident`

Filter
------

- Examples:
  - <https://github.com/IGB-Berlin/igb-fuchs/blob/main/dev/git_commit_filter.pl>
    - Set up via <https://github.com/IGB-Berlin/igb-fuchs/blob/main/dev/setup_git_filter.sh>
  - <https://github.com/haukex/de-en-dict/blob/main/git_commit_filter.pl>
    - Set up via <https://github.com/haukex/de-en-dict/blob/d2057c33/Makefile#L21>
  - For both of the above, setting up via `git config --worktree` would probably be better
- Other, older examples:
  - <https://github.com/haukex/htools/blob/master/htmlrescache>
  - <https://github.com/haukex/htools/blob/master/zip2pl>

LFS
---

- `git lfs install`
- `git lfs track '*.pdf' '*.png' '*.jpg' '*.zip'`
  - This sets up `.gitattributes` entries like `*.pdf filter=lfs diff=lfs merge=lfs -text`
- `git lfs clone ...` (deprecated?)
- Pruning:
  - `git config --worktree lfs.pruneremotetocheck github` (default `origin`)
  - `git lfs prune --recent --verify-remote`
- For large files that should still be diffed as text files (example using large CSV files):
  - Run `git config --worktree diff.lfstext.textconv cat`
  - In `.gitattributes`: `*.csv filter=lfs diff=lfstext merge=lfs -text`
- If there's a file that shouldn't be added to LFS (again example using CSV files):
  - In `.gitattributes`: `small.csv !filter !diff !merge text`

Credentials
-----------

- <https://github.com/haukex/dotfiles/blob/main/Git-Credentials.md>
  (is in that repo for historical reasons, I could probably merge it into this one someday)

GitHub
------

- Skipping checks: Put e.g. `[skip actions]` anywhere in the message
  ([reference](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/skip-workflow-runs))

See Also
--------

- <https://github.com/haukex/dotfiles/blob/main/.gitconfig>
- <https://github.com/haukex/dotfiles/blob/main/git_mysync.py>


<!-- spell: ignore lfstext pruneremotetocheck textconv worktree -->

Author, Copyright, and License
------------------------------

Copyright (c) 2025 Hauke Daempfling <haukex@zero-g.net>
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

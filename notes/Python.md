My Notes on Python
==================

In this directory, `requirements.txt` is not the list of requirements
for this project, instead it is my notes on all the Python modules
I find interesting / useful.

Compiling Python from Source on Linux
-------------------------------------

These instructions are for installing Python versions into `/opt`.

### Build Dependencies

Hint: Look at the output of `make` to see if modules aren't getting built.

    sudo apt build-dep python3 python3-tk
    sudo apt install build-essential pkg-config libssl-dev libsqlite3-dev libgdbm-dev \
        libgdbm-compat-dev libc6-dev libbz2-dev libreadline-dev uuid-dev lzma-dev liblzma-dev \
        libffi-dev tk-dev libncurses-dev sqlite3

### Download & Install

Download the XZ tarball from <https://www.python.org/downloads/source/>

Now **either** use the `linux-py-install.sh` script from this repository, **or** use the following:

#### Manual Install

Needed in some cases, such as if individual steps fail, you need to specify additional options,
or you want the installation to be owned by your user instead of `root`.

The following two steps are *only* needed if your user should be the owner:

    sudo mkdir -v /opt/python3.11.10
    sudo chown -c `id -u`:`id -g` /opt/python3.11.10

General steps follow:

    umask 022  # in case you have a more restrictive umask set

    tar xJvf Python-3.11.10.tar.xz
    cd Python-3.11.10

    ./configure --prefix=/opt/python3.11.10 --enable-optimizations
    make
    # On 3.9 & 3.10: `make test TESTOPTS="-x test_socket"` (b/c the test hangs)
    make test
    sudo make install   # `sudo` not needed if you did the `chown` step above

    sudo ln -snfv /opt/python3.11.10 /opt/python3.11
    sudo /opt/python3.11/bin/python3 -m pip install --upgrade --upgrade-strategy=eager pip wheel

### Other notes

Creating local symlinks to multiple Python versions:

    for V in $(seq 9 14); do ln -snfv /opt/python3.$V/bin/python3.$V ~/.local/bin/; done

Examples for `~/.profile` or `~/.bashrc`:

    test -d /opt/python3 && PATH="/opt/python3/bin${PATH:+:${PATH}}"

    export PYTHONPATH="$HOME/code/igbdatatools${PYTHONPATH:+:${PYTHONPATH}}"

If a default `venv` is needed (e.g. you installed as `root`),
do e.g. `/opt/python3.13/bin/python -m venv ~/.venvs/default`
and then add this to `.bashrc`: `source ~/.venvs/default/bin/activate`

If building on an old Ubuntu LTS like 18.04 (bionic), see <https://github.com/python/cpython/issues/98973>:
the `./configure` step needs to be prefixed with `TCLTK_LIBS="-ltk8.6 -ltcl8.6" TCLTK_CFLAGS="-I/usr/include/tcl8.6"`
for tkinter to work (look for `checking for stdlib extension module _tkinter... yes`)

### Documentation

Example to download and extract docs from <https://docs.python.org/3/download.html>

    wget https://docs.python.org/3/archives/python-3.13-docs-html.tar.bz2
    tar xjvf python-3.13-docs-html.tar.bz2
    # tar has 0660/0770 perms, fix that:
    find python-3.13-docs-html -type d -exec chmod -c 755 '{}' + -o -exec chmod -c 644 '{}' +

Windows Notes
-------------

Getting `python3` to reference `python` on Win 10 (because `python3.exe`
opens the Store), shown from *Git Bash*:

    rm -v "$HOME/AppData/Local/Microsoft/WindowsApps/python3.exe"
    cd "$HOME/AppData/Local/Programs/Python/Python313/"
    cp python.exe python3.exe

In addition, an alias per Python version can be set up via e.g. (again *Git Bash*):

    for PV in $(seq 9 14); do echo -e \#\!"/bin/bash\n~/AppData/Local/Programs/Python/Python3$PV/python \"\$@\"" >~/bin/python3.$PV; done

In Windows 10, environment variables can be added for the current user via the
Control Panel, in User Accounts you can find a setting "Change my environment
variables", or you can press Windows+R and then enter:

    rundll32.exe sysdm.cpl,EditEnvironmentVariables

To apply execute permissions to files on Windows:

    git ls-files --stage
    git update-index --chmod=+x <filenames>

You can add `make` to Git Bash as follows:

- Download `make-*-without-guile-w32-bin.zip`
  from <https://sourceforge.net/projects/ezwinports/files/>
- Unpack and merge into `Git/mingw64/`
  (e.g. `$HOME/AppData/Local/Programs/Git/mingw64`)
  without overwriting any files

Windows Embeddable Python with Tk
---------------------------------

**Note** using [PyInstaller](https://pyinstaller.org/) may be easier depending on the project.
(e.g. `pyinstaller --onefile --name exename path/to/__main__.py`, possibly with `--noconsole`
or `--hide-console minimize-early`)

1. Download and extract the embeddable version of Python

   1. In all of the following commands, make sure to be running
      the `python.exe` from this version

2. As per https://stackoverflow.com/a/48906746 do this:

   1. In `python3*._pth`, uncomment the `import site` command.
   2. As per https://pip.pypa.io/en/stable/installation/
      download https://bootstrap.pypa.io/get-pip.py and run it

3. As per https://stackoverflow.com/a/44169516 do this:

   1. Your local Windows Python installation should be the same version
      as the embeddable Python.
   2. Copy the following items over into the root directory of the
      embeddable Python:
      - directory `tcl`
      - directory `Lib/tkinter`
      - from the `DLLs` folder: `_tkinter.pyd`, `tcl86t.dll`, `tk86t.dll`, `zlib1.dll`

4. To add `igbdatatools` support:

   1. Download https://github.com/haukex/igbdatatools/archive/refs/heads/main.zip
   2. Unpack this to, for example, `igbdatatools-HASH` in the root directory
      of the embeddable Python
   3. Modify `python3*._pth` and add the directory name (just `igbdatatools-HASH`)
      after the dot `.` (because embeddable Python doesn't use PYTHONPATH)
   4. Can comment out `pyicu` from `requirements.txt` if not needed
   5. Install `requirements.txt` modules (`..\python.exe -m pip install ...`)

Python Versions
---------------

Some of the reasons I require the latest Python versions,
(basically just a few select highlights from the changelogs that I like):

- Python 3.10
  - newer typing features like union type operator
  - `zip(..., strict=True)` (`more_itertools.zip_equal` has been deprecated)
  - `PYTHONWARNDEFAULTENCODING`
- Python 3.11
  - `datetime.fromisoformat` is more flexible (e.g. supports trailing `Z`)
  - `contextlib.chdir`
  - `typing.Self`
  - Python 3.11.1 for `http.server` security updates
- Python 3.12
  - `NamedTemporaryFile(delete=True, delete_on_close=False)`


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


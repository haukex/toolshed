My Notes on Python
==================

In this directory, `requirements.txt` is not the list of requirements
for this project, instead it is my notes on all the Python modules
I find interesting / useful.

Installing Python on Linux
--------------------------

    sudo apt-get install build-essential pkg-config libssl-dev libsqlite3-dev libgdbm-dev libgdbm-compat-dev \
        libc6-dev libbz2-dev libreadline-dev uuid-dev lzma-dev liblzma-dev libffi-dev tk-dev libncurses5-dev
    sudo apt-get build-dep python3 idle-python3.11

    umask 022
    sudo mkdir -v /opt/python3.11.2
    sudo chown -c `id -u`:`id -g` /opt/python3.11.2

    wget https://www.python.org/ftp/python/3.11.2/Python-3.11.2.tar.xz
    tar xJvf Python-3.11.2.tar.xz

    cd Python-3.11.2
    ./configure --prefix=/opt/python3.11.2 --enable-optimizations
    make && make test && make install

    sudo ln -snfv /opt/python3.11.2 /opt/python3

    # in ~/.profile:
    test -d /opt/python3 && PATH="/opt/python3/bin${PATH:+:${PATH}}"

    which python3
    which pip3
    which idle3
    python3 --version

    python3 -m pip install --upgrade pip wheel
    # see requirements.txt for how to install those

    # to add something to PYTHONPATH in .profile:
    export PYTHONPATH="$HOME/code/igbdatatools${PYTHONPATH:+:${PYTHONPATH}}"

    # https://docs.python.org/3/download.html
    wget https://docs.python.org/3/archives/python-3.11.2-docs-html.tar.bz2
    tar xjvf python-3.11.2-docs-html.tar.bz2
    mv python-3.11.2-docs-html /opt/python3/html
    find /opt/python3/html -type d -exec chmod 755 '{}' + -o -exec chmod 644 '{}' +

If building on an old Ubuntu LTS like 18.04 (bionic), see <https://github.com/python/cpython/issues/98973>:
the `./configure` step needs to be prefixed with `TCLTK_LIBS="-ltk8.6 -ltcl8.6" TCLTK_CFLAGS="-I/usr/include/tcl8.6"`
for tkinter to work (look for `checking for stdlib extension module _tkinter... yes`)

An alternative I haven't tested yet: <https://launchpad.net/~deadsnakes/+archive/ubuntu/ppa>
(`sudo add-apt-repository ppa:deadsnakes/ppa`)

Windows Notes
-------------

During Git install, I usually choose `autocrlf=input`.

Getting `python3` to reference `python` on Win 10 (because `python3.exe`
opens the Store), shown from Git Bash:

    rm "$HOME/AppData/Local/Microsoft/WindowsApps/python3.exe"
    cd "$HOME/AppData/Local/Programs/Python/Python312/"
    cp python.exe python3.exe

In addition, an alias per Python version can be set up via e.g.:

    for PV in 8 9 10 11 12 13; do echo -e \#\!"/bin/bash\n~/AppData/Local/Programs/Python/Python3$PV/python \"\$@\"" >~/bin/python3.$PV; done

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

Windows Embeddable Python
-------------------------

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

Some of the reasons I require the latest Python versions:

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


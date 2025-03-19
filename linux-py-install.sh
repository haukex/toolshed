#!/bin/bash
set -euo pipefail

# handle command line args
usage() { echo "Usage: $0 PYTHON_TXZ" 1>&2; exit 1; }
[[ $# -eq 1 ]] || usage
python_txz="$( realpath "$1" )"
test -f "$python_txz" || usage

# extract Python version from filename (fairly strict filename format requirement here)
py_ver="$( perl -wMstrict -Mvars='$r' -se \
    '$r=~/^Python-(3\.\d+\.\d+(?:(?:a|b|rc)\d+)?)\.tar\.xz$/ or die "Failed to parse $r\n"; print $1' \
    -- -r="$( basename "$python_txz" )" )"
py_ver2="$( echo "$py_ver" | cut -d. -f1,2 )"

# set up temporary working directory
temp_dir="$( mktemp --directory )"
trap 'set +ex; popd >/dev/null; sudo rm -rf "$temp_dir"' EXIT
pushd "$temp_dir" >/dev/null
#echo "Temporary working dir $(pwd -P)"

# installation target directory
targ_dir="/opt/python$py_ver"
if test -d "$targ_dir"; then
    echo "Target directory $targ_dir already exists"
    exit 1
fi

# the name of the link that will point to this installation
link_name="/opt/python$py_ver2"
test -e "$link_name" && echo "NOTE: Link $link_name already exists, points to $( readlink $link_name ) (consider deleting after install)"

# preparation done, begin installation
echo "Will install Python Version $py_ver ($py_ver2) from $python_txz to $targ_dir with link $link_name"
set -x

umask 022
tar xJf "$python_txz"
cd "Python-$py_ver"
./configure --prefix="$targ_dir" --enable-optimizations
make
make test
#TODO: If `make test` fails, the temporary directory is removed, and we can no longer re-run the tests or force install
sudo make install
sudo "$targ_dir/bin/python3" -m pip install --root-user-action=ignore --upgrade --upgrade-strategy=eager pip wheel
sudo ln -snfv "$targ_dir" "$link_name"

echo -e "\n=====> \e[1;32mSuccessfully installed Python $py_ver\e[0m <====="

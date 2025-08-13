#!/bin/bash
set -euo pipefail

# handle command line args
usage() { echo "Usage: $0 PYTHON_TXZ" 1>&2; exit 1; }
[[ $# -eq 1 ]] || usage
python_txz="$( realpath "$1" )"
test -f "$python_txz" || usage

# extract Python version from filename (fairly strict filename format requirement here)
py_ver="$( perl -wMstrict -Mvars='$r' -se \
    '$r=~/^Python-(3\.\d+\.\d+(?:(?:a|b|rc)\d+)?)\.tar\.xz$/ and print $1 or die "Failed to parse $r\n"' \
    -- -r="$( basename "$python_txz" )" )"
py_ver2="$( echo "$py_ver" | cut -d. -f1,2 )"

# set up temporary working directory
temp_dir="$( mktemp --directory )"
trap 'set +ex; popd >/dev/null; rm -rf "$temp_dir"' EXIT
pushd "$temp_dir" >/dev/null

# installation target directory
targ_dir="/opt/python$py_ver"
if test -d "$targ_dir"; then
    echo "Target directory $targ_dir already exists"
    exit 1
fi

# the name of the link that will point to this installation
link_name="/opt/python$py_ver2"
test -e "$link_name" && prev_link_targ="$( readlink "$link_name" )" || prev_link_targ=""

# which tests to exclude
# test_smtpnet has just been failing way too often on me, so exclude it.
test_excludes=("smtpnet")
# For me, test_socket hangs on 3.9 and 3.10
[[ "$py_ver2" =~ ^3\.(9|10)$ ]] && test_excludes+=("socket")

# preparation done, begin compilation
set -x
umask 022
tar xJf "$python_txz"
cd "Python-$py_ver"
./configure --prefix="$targ_dir" --enable-optimizations
make

# tests
# NOTE doing Ctrl-C on the tests kills this script too (temp dir is cleaned up)
if ! make test TESTOPTS="$(printf -- "-x test_%s " "${test_excludes[@]}")"; then
	# make test failed
	set +x
	read -rp "make test failed, force installation anyway? (y/N) " answer
	if [[ ! "$answer" =~ ^[yY] ]]; then
		# user said not to force installation
		trap '' EXIT
		echo
		echo "Tried to install Python $py_ver ($py_ver2) from $python_txz to $targ_dir with link $link_name"
		echo -e "=====>\e[1;31m make test failed! \e[0m<=====\n"
		echo "Keeping temp working dir: $(pwd -P)"
		echo "I didn't get to perform the following steps:"
		# the following is copy & pasted from below
		echo "$ sudo make install"
		echo "$ sudo '$targ_dir/bin/python3' -m pip install --root-user-action=ignore --upgrade --upgrade-strategy=eager pip"
		echo "$ sudo ln -snfv '$targ_dir' '$link_name'"
		echo "$ rm -rf '$temp_dir'"  # from trap EXIT above
		test -n "$prev_link_targ" && echo "Consider doing: sudo rm -rf '$prev_link_targ' (the previous target of $link_name)"
		exit 1
	# else answer began with Y, so fall through to installation
	fi
	set -x
# else make test succeeded
fi

# finish installation
# NOTE how the following commands are copied to the `echo`s above!
sudo make install
sudo "$targ_dir/bin/python3" -m pip install --root-user-action=ignore --upgrade --upgrade-strategy=eager pip
sudo ln -snfv "$targ_dir" "$link_name"

set +x
echo
echo "Installed Python $py_ver ($py_ver2) from $python_txz to $targ_dir with link $link_name"
echo -e "=====>\e[1;32m Successfully installed Python $py_ver \e[0m<=====\n"
# the following is also copied to the above 1:1
test -n "$prev_link_targ" && echo "Consider doing: sudo rm -rf '$prev_link_targ' (the previous target of $link_name)"


#!/bin/bash
set -euxo pipefail
script_dir="$( CDPATH='' cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" && pwd )"
#                        \^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^/
# or just this part to change the cwd to the script's directory ^^^
echo "script_dir=$script_dir"

temp_dir="$( mktemp --directory )"
trap 'set +ex; popd >/dev/null; rm -rf "$temp_dir"' EXIT
pushd "$temp_dir" >/dev/null

# NOTE only one "trap ... EXIT" per script!
#temp_file="$( mktemp )"
#trap 'set +ex; rm -f "$temp_file"' EXIT

# Arrays:
some_array=( "foo" "bar" "quz" )  # or e.g. `gz_files=(*.gz)`
echo "${some_array[@]}" len=${#some_array[@]}

# Sources:
# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
# https://stackoverflow.com/a/246128
# https://stackoverflow.com/a/29835459

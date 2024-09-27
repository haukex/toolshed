#!/bin/bash
set -euxo pipefail
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
#              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
# or just this part to change the cwd to the script's directory
echo "SCRIPT_DIR=$SCRIPT_DIR"

TEMPDIR="$( mktemp --directory )"
trap 'set +e; popd >/dev/null 2>&1; rm -rf "$TEMPDIR"' EXIT
pushd "$TEMPDIR" >/dev/null

# NOTE only one "trap ... EXIT" per script!
#TEMPFILE="$( mktemp )"
#trap 'rm -f "$TEMPFILE"' EXIT

# Arrays:
SOME_ARRAY=( "foo" "bar" "quz" )
echo "${SOME_ARRAY[@]}"

# Sources:
# https://vaneyckt.io/posts/safer_bash_scripts_with_set_euxo_pipefail/
# https://stackoverflow.com/a/246128

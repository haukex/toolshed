#!/bin/bash
set -euo pipefail

usage() { echo "Usage: $0 [-b] [-p OTHER_PATH] SOME_PATH" 1>&2; exit 1; }

other_path=..
bool_opt=
while getopts "p:b" opt; do
    case "${opt}" in
        p)
            other_path="${OPTARG}"
            test -d "$other_path" || usage
            ;;
        b) bool_opt=1 ;;
        *) usage ;;
    esac
done
shift $((OPTIND-1))

[[ $# -eq 1 ]] || usage
some_path="$1"
test -d "$some_path" || usage

echo "some_path=$some_path"
echo "other_path=$other_path"
echo "bool_opt=$bool_opt"

set -x

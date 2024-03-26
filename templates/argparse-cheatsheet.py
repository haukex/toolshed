#!/usr/bin/env python3
import argparse
from igbpyutils.file import autoglob, cmdline_rglob

def main():
    parser = argparse.ArgumentParser(description='Template')
    parser.add_argument('-v', '--verbose', help="more output", action="store_true")

    # the following defaults `foo` to `None` and doesn't generate a short equivalent to `--no-foo` (e.g. `-X`):
    parser.add_argument('-x', '--foo', help="Foo?", action=argparse.BooleanOptionalAction)
    # the following defaults bar to `False` (won't be `None`):
    parser.add_argument('-y', '--bar', help="Bar On", action="store_true")
    parser.add_argument('-Y', '--no-bar', help="Bar Off", dest="bar", action="store_false")
    # and for a fully tri-state-able option (that defaults to `None`):
    parser.add_argument('-z', '--quz', help="Quz On", action="store_true", default=None)
    parser.add_argument('-Z', '--no-quz', help="Quz Off", dest="quz", action="store_false", default=None)
    parser.add_argument('--ignore-quz', help="No Quz", dest="quz", action="store_const")

    subparsers = parser.add_subparsers(dest='cmd', required=True)

    parser_demo = subparsers.add_parser('demo', help='Demo')
    parser_demo.add_argument('-a', '--add', help="add stuff to list", action="append", default=[])
    parser_demo.add_argument('-c', '--choice', help="choice of 'one' or 'two'", required=True, choices=['one','two'])
    parser_demo.add_argument('-f', '--float', help="a float (default: 10e6)", type=float, default=10e6)
    parser_demo.add_argument('something', choices=['foo', 'bar', 'quz'])  # required by default
    parser_demo.add_argument('paths', metavar='PATH', help="files/dirs to process (recursive)", nargs="*")

    args = parser.parse_args()
    if args.choice != 'one':
        parser.error("In this demo you must choose 'one'")

    paths = list( cmdline_rglob(autoglob(args.paths)) )

    if args.verbose: print(f"{args=} {paths=}")  # call main function here

    parser.exit(0)

if __name__=='__main__': main()

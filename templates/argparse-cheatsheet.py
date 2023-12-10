#!/usr/bin/env python3
import argparse
from igbpyutils.file import autoglob, cmdline_rglob

def main():
    parser = argparse.ArgumentParser(description='Template')
    parser.add_argument('-v', '--verbose', help="more output", action="store_true")
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

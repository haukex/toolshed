#!/usr/bin/env python
import argparse
from igbpyutils.file import autoglob, cmdline_rglob
# see also: https://igbpyutils.readthedocs.io/en/stable/file.html#igbpyutils.file.open_out

def _arg_parser():
    # NOTE the first 'prog' argument here vvvvv is optional and defaults to sys.argv[0]
    parser = argparse.ArgumentParser('argparse-cheatsheet', description='Template')
    # more details can be added to the above via `epilog='...'`
    parser.add_argument('-v', '--verbose', help="more output", action="store_true")

    # the following defaults `foo` to `None` and doesn't generate a short equivalent to `--no-foo` (e.g. `-X`):
    parser.add_argument('-x', '--foo', help="Foo?", action=argparse.BooleanOptionalAction)
    # the following defaults bar to `False` (won't be `None`):
    parser.add_argument('-y', '--bar', help="Bar On", action="store_true")
    parser.add_argument('-Y', '--no-bar', help="Bar Off", dest="bar", action="store_false")
    # and for a fully tri-state-able option (that defaults to `None`):
    parser.add_argument('-z', '--quz', help="Quz On", action="store_true", default=None)
    parser.add_argument('-Z', '--no-quz', help="Quz Off", dest="quz", action="store_false", default=None)
    parser.add_argument('--ignore-quz', help="No Quz", dest="quz", action="store_const", const=None)

    subparsers = parser.add_subparsers(dest='cmd', required=True, help="CMD -h for help")

    parser_demo = subparsers.add_parser('demo', help='Demo')
    parser_demo.add_argument('-a', '--add', help="add stuff to list", action="append", default=[])
    parser_demo.add_argument('-c', '--choice', help="choice of 'one' or 'two'", required=True, choices=['one','two'])
    parser_demo.add_argument('-f', '--float', help="a float (default: 10e6)", type=float, default=10e6)
    parser_demo.add_argument('something', choices=['foo', 'bar', 'quz'])  # required by default
    parser_demo.add_argument('paths', metavar='PATH', help="files/dirs to process (recursive)", nargs="*")  # or nargs="+"; always a list
    # Note: nargs="?" makes positional arguments optional (and doesn't result in a list)
    # note this can be combined with fileinput: set nargs="*" and use `for line in fileinput.input(args.files)`
    # but note fileinput is a little tricky with encoding on <3.10: https://github.com/haukex/pytoa5/blob/011cb0ea/toa5/to_csv/__init__.py#L74

    return parser

def main(argv=None):
    parser = _arg_parser()  # feel free to inline (unless the object is needed elsewhere, like for docs)

    args = parser.parse_args(argv)  # argv=None means sys.argv[1:]
    if args.choice != 'one':
        parser.error("In this demo you must choose 'one'")

    paths = list( cmdline_rglob(autoglob(args.paths)) )

    # call main function here (this is just an example)
    if args.verbose:
        print(f"{args=} {paths=}")

    parser.exit(0)

if __name__=='__main__':
    main()

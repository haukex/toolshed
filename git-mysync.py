#!/usr/bin/env python3
"""This script checks a set of git repositories for synchronization with the server.

Author, Copyright, and License
------------------------------
Copyright (c) 2023 Hauke Daempfling (haukex@zero-g.net)
at the Leibniz Institute of Freshwater Ecology and Inland Fisheries (IGB),
Berlin, Germany, https://www.igb-berlin.de/

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see https://www.gnu.org/licenses/
"""
import sys
import argparse
import subprocess
import re
from pathlib import Path
from warnings import warn
from igbpyutils.error import init_handlers
from colorama import just_fix_windows_console, Fore, Style
# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

DEFAULT_CONFFILE = '~/.git-mysync'

init_handlers()
just_fix_windows_console()
parser = argparse.ArgumentParser(description='My Git Sync Checker')
parser.add_argument('-c', '--conffile', help=f"alternate config file (default: {DEFAULT_CONFFILE})")
parser.add_argument('-g', '--addgit', help="additional git repo(s) to check", action="append")
parser.add_argument('-f', '--fetch', help="do a git fetch first", action="store_true")
parser.add_argument('-l', '--changes', help="show local changes and stash", action="store_true")
parser.add_argument('-v', '--verbose', help="be more verbose", action="store_true")
args = parser.parse_args()

conffile = Path( args.conffile if args.conffile else DEFAULT_CONFFILE ).expanduser()
paths = args.addgit if args.addgit else []
try:
    with conffile.open(encoding='UTF-8') as fh:
        for line in fh:
            if line.lstrip().startswith('#') or not line.strip(): continue
            paths.append(line.rstrip())
    if args.verbose: print(f"{Style.DIM}# read config file: {conffile.resolve(strict=True)}{Style.RESET_ALL}")
except FileNotFoundError:
    warn(f"configuration file {conffile!r} not found!")
if not paths:
    raise RuntimeError('No git repositories to check!')
paths = [ Path(x) for x in paths ]

# https://git-scm.com/docs/git-status#_porcelain_format_version_2
head_re  = re.compile(r'''^# branch.head (.+)$''', re.MULTILINE)
upstr_re = re.compile(r'''^# branch.upstream (.+)$''', re.MULTILINE)
ahead_re = re.compile(r'''^# branch.ab \+(\d+) -(\d+)$''', re.MULTILINE)
stash_re = re.compile(r'''^# stash (\d+)$''', re.MULTILINE)

badcount = 0
localchanges = 0
for pth in paths:
    out = f"{pth if args.verbose else pth.name} "
    print(out, end='', flush=True)
    if args.fetch:
        print(f"fetch-", end='', flush=True)
        try:
            rv = subprocess.run( ['git','fetch','--quiet'],
                cwd=pth.expanduser(), encoding='UTF-8', capture_output=True, check=True )
            if rv.stderr: raise subprocess.SubprocessError(f"stderr={rv.stderr!r}")
        except subprocess.SubprocessError as ex:
            print(f"\r{Fore.RED}{out}fetch-ERROR: {ex}{Style.RESET_ALL}")
            badcount += 1
            continue
        else:
            out += f"fetch-ok "
            print(f"{Fore.GREEN}ok{Fore.RESET} ", end='', flush=True)
    try:
        rv = subprocess.run(
            ['git','status','--porcelain=v2','--branch','--ahead-behind','--show-stash'],
            cwd=pth.expanduser(), encoding='UTF-8', capture_output=True, check=True )
        if rv.stderr: raise subprocess.SubprocessError(f"stderr={rv.stderr!r}")
    except subprocess.SubprocessError as ex:
        print(f"\r{Fore.RED}{out}git-status ERROR: {ex}{Style.RESET_ALL}")
        badcount += 1
        continue
    if not ( m := head_re.search(rv.stdout) ):
        raise RuntimeError(f"failed to find branch.head in output {rv.stdout=}")
    head = m.group(1)
    print(f"{head=} ", end='', flush=True)
    if m := stash_re.search(rv.stdout):
        stash = int(m.group(1))
    else: stash = 0
    lines = [ x for x in rv.stdout.splitlines() if x.strip() and not x.startswith('#') ]
    if lines or stash:
        lochg = f"{Style.RESET_ALL}{Fore.YELLOW}" \
            + ( f" {len(lines)} local change{'' if len(lines)==1 else 's'}" if lines else '' ) \
            + ( f" {stash} stash entr{'y' if stash==1 else 'ies'}" if stash else '' ) \
            + f"{Fore.RESET}"
        localchanges += 1
    else: lochg = f'{Style.RESET_ALL}'
    if m := upstr_re.search(rv.stdout):
        upstr = m.group(1)
        if m := ahead_re.search(rv.stdout):
            ahead = int(m.group(1))
            behind = int(m.group(2))
            if ahead==0 and behind==0:
                print(f"\r{Fore.GREEN}{out}{head=} {upstr=} up-to-date{lochg}")
            else:
                print(f"{upstr=} {Fore.RED}we are {ahead=} {behind=}{lochg}")
                badcount += 1
        else:
            raise RuntimeError(f"found branch.upstream but not ahead/behind info {rv.stdout=}")
    else:
        print(f"\r{Fore.RED}{out}{head=} No upstream{Style.RESET_ALL}")
        badcount += 1
    if args.changes:
        subprocess.run( ['git','status','--short'], cwd=pth.expanduser(), check=True )
        # git stash list seems to break the color codes on the windows console, so work around by capturing...
        rv2 = subprocess.run( ['git','stash','list'],
            cwd=pth.expanduser(), encoding='UTF-8', capture_output=True, check=True )
        if rv2.stderr: print(rv2.stderr, end='', file=sys.stderr)
        if rv2.stdout: print(rv2.stdout, end='')

loch = f"{localchanges} repo{'' if localchanges==1 else 's'} with local changes{Fore.RESET}" if localchanges else ''
if badcount:
    if localchanges: loch = f" {Fore.YELLOW}and {loch}"
    print(f"{Fore.RED}# {badcount} issue{'' if badcount==1 else 's'}{Fore.RESET}{loch}")
else:
    if localchanges: loch = f", {Fore.YELLOW}but {loch}"
    print(f"{Fore.GREEN}# All OK:{Fore.RESET} Everything up-to-date{loch}")
sys.exit(badcount)

#!/usr/bin/env python
"""Script to generate hashes for files on a WebDAV server.

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
import csv
import hashlib
import argparse
from pathlib import PurePosixPath
from collections.abc import Generator
from webdav4.client import Client, DEFAULT_CHUNK_SIZE  # https://skshetry.github.io/webdav4/reference/client.html
import keyring

def get_pw(service :str, username :str):
    password = keyring.get_password(service, username)
    if not password:
        raise KeyError(f"please first store the password with the command: python -m keyring set \"{service}\" \"{username}\"")
    return password

def hash_webdav(davurl :str, username :str, remoteroot :str) -> Generator[tuple[PurePosixPath, int, bytes], None, None]:
    client = Client(davurl, auth=(username, get_pw(davurl, username)), timeout=10)
    listq = [remoteroot]
    while listq:
        curdir = listq.pop()
        for ent in client.ls(str(curdir)):
            assert isinstance(ent, dict)
            if ent["type"] == "file":
                # note: AFAICT, Nextcloud's etags are based on mtime, inode, dev, and size; not content
                # https://github.com/nextcloud/server/blob/5cf42ff2/lib/private/Files/Storage/Local.php#L556
                h = hashlib.sha512()
                with client.open(ent['name'], 'rb', chunk_size=DEFAULT_CHUNK_SIZE) as fh:
                    while buf := fh.read(DEFAULT_CHUNK_SIZE):
                        assert isinstance(buf, bytes)
                        h.update(buf)
                yield PurePosixPath(ent['name']).relative_to(remoteroot), ent['content_length'], h.digest()
            elif ent["type"] == "directory":
                listq.append(ent["name"])
            else:
                raise TypeError(f"unhandled remote filetype: {ent!r}")

def main():
    parser = argparse.ArgumentParser(description='Hash a WebDAV Directory')
    parser.add_argument('url', help="server URL")
    parser.add_argument('username', help="username")
    parser.add_argument('root', help="the root directory to hash")
    parser.add_argument('outfile', help="the output CSV file")
    args = parser.parse_args()

    with open(args.outfile, 'x', encoding='UTF-8', newline='') as fh:
        csvwr = csv.writer(fh, strict=True)
        csvwr.writerow(["name","size","checksum"])
        for name, size, hsh in hash_webdav(args.url, args.username, args.root):
            csvwr.writerow((name,size,hsh.hex()))

    parser.exit(0)

if __name__=='__main__':
    main()

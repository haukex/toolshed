#!/usr/bin/env python
"""Script to copy PuTTY settings from "Default Settings" to other session profiles.

For example, you can make a change to the color settings in the Default Settings and then copy
those colors over to all of the other session profiles.

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
from typing import Any
from winreg import OpenKeyEx, HKEY_CURRENT_USER, KEY_WRITE, QueryInfoKey, EnumKey, EnumValue, SetValueEx
from urllib.parse import unquote
from igbpyutils.iter import is_unique_everseen

DEFAULT_KEY = 'Default%20Settings'
EXCLUDE_VALS = ('HostName','PortNumber','UserName','Protocol')

with OpenKeyEx(HKEY_CURRENT_USER, r'SOFTWARE\SimonTatham\PuTTY\Sessions') as mainkey:
    def get_sess_as_dict(sessionkey):
        with OpenKeyEx(mainkey, sessionkey) as key:
            sessvalues = [ EnumValue(key, vi) for vi in range(QueryInfoKey(key)[1]) ]
        sessvalues.sort()
        assert all(is_unique_everseen( x[0] for x in sessvalues ))  # no duplicate names
        sessdict :dict[str, tuple[Any, int]] = { name: (data, typ) for name, data, typ in sessvalues }
        return sessdict
    sessions = [ EnumKey(mainkey, si) for si in range(QueryInfoKey(mainkey)[0]) ]
    sessions.sort()
    sessions.remove(DEFAULT_KEY)
    defaults = get_sess_as_dict(DEFAULT_KEY)
    for sesskey in sessions:
        sessname = unquote(sesskey)
        values = get_sess_as_dict(sesskey)
        assert tuple(values.keys()) == tuple(defaults.keys())
        for k in defaults:
            if k in EXCLUDE_VALS:
                continue
            if values[k] != defaults[k]:
                assert values[k][1] == defaults[k][1]  # assume they'll have the same type
                if input(f"{sessname!r} {k!r}: {values[k][0]!r} => {defaults[k][0]!r}? [yN] ").lower().startswith('y'):
                    with OpenKeyEx(mainkey, sesskey, access=KEY_WRITE) as wrkey:
                        SetValueEx(wrkey, k, 0, defaults[k][1], defaults[k][0])
